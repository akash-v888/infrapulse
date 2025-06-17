import requests
import time

def check_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("health") == "pass":
                print(f"Health check passed: {data}")
            else:
                print(f"Health check responded but not OK: {data}")
        else:
            print(f"Received status code {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")

if __name__ == "__main__":
    endpoint = input("Enter the full /health URL of your deployed app (e.g. http://3.91.100.123/health): ").strip()
    print(f"Checking health at {endpoint} every 10 seconds. Press Ctrl+C to stop.")
    try:
        while True:
            check_health(endpoint)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped.")
