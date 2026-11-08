
import requests
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://127.0.0.1:5000/students"

TOTAL_REQUESTS = 10000
CONCURRENT_USERS = 50

def send_request():
    start = time.perf_counter()

    try:
        response = requests.get(URL, timeout=15)
        elapsed = time.perf_counter() - start

        return {
            "success": response.status_code == 200,
            "status": response.status_code,
            "error": response.text[:200] if response.status_code != 200 else "",
            "time": elapsed
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "status": "Connection Error",
            "error": str(e),
            "time": time.perf_counter() - start
        }


results = []
test_start = time.perf_counter()

with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
    futures = [
        executor.submit(send_request)
        for _ in range(TOTAL_REQUESTS)
    ]

    for future in as_completed(futures):
        results.append(future.result())

total_time = time.perf_counter() - test_start

print("\n--- Workload Test Diagnostics ---")
print("Total Requests:", TOTAL_REQUESTS)
print("Successful:", sum(r["success"] for r in results))
print("Failed:", sum(not r["success"] for r in results))

print("\nStatus Code Distribution:")
print(Counter(str(r["status"]) for r in results))

print("\nFirst 5 Failed Requests:")
for r in [x for x in results if not x["success"]][:5]:
    print("Status:", r["status"])
    print("Error:", r["error"])
    print("---")

print("\nTotal Test Duration:", round(total_time, 2), "seconds")
response_times = [r["time"] for r in results]

print("\n--- Performance Metrics ---")
print("Average Response Time (ms):",
      round(sum(response_times) / len(response_times) * 1000, 2))
print("Minimum Response Time (ms):",
      round(min(response_times) * 1000, 2))
print("Maximum Response Time (ms):",
      round(max(response_times) * 1000, 2))
print("Requests per Second:",
      round(TOTAL_REQUESTS / total_time, 2))