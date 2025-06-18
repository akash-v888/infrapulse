import requests
import time
from db import init_db, log_health_check
from email_alert import send_email

time.sleep(2)

init_db()

# http://13.218.57.145/health
HEALTHCHECK_URL = "http://13.218.57.145/health"
EMAIL_SENDER = "aviswa259@gmail.com"
EMAIL_RECIPIENT = "aviswa259@gmail.com"

try:
    start = time.time()
    response = requests.get(HEALTHCHECK_URL, timeout=5)
    elapsed_ms = int((time.time() - start) * 1000)

    if response.status_code == 200 and response.json().get("health") == "pass":
        print(f"Health check passed ({elapsed_ms} ms)")
        log_health_check("pass", response_time_ms=elapsed_ms)
    else:
        print("Health check failed: unexpected response")
        log_health_check("fail", response_time_ms=elapsed_ms, error_message="Unexpected response")
        send_email("InfraPulse Health Alert", "Unexpected health check response", EMAIL_SENDER, EMAIL_RECIPIENT)

except Exception as e:
    print(f"Health check failed: Exception occurred - {e}")
    log_health_check("fail", response_time_ms=0, error_message=str(e))
    send_email("InfraPulse Health Alert", f"Exception occurred:\n\n{e}", EMAIL_SENDER, EMAIL_RECIPIENT)
