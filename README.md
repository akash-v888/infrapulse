# InfraPulse

InfraPulse is a lightweight infrastructure health monitoring system built with Python, SQLite, and Grafana. It performs periodic HTTP health checks on a target service, logs the results to a local SQLite database, and visualizes the data through a Grafana dashboard. The system also sends email alerts when failures occur.

## Features

- Scheduled HTTP health checks via cron
- Response time logging with status (pass/fail)
- SQLite-backed time-series log of health checks
- Grafana dashboard for real-time monitoring and analytics
- Email alerts on health check failure or unexpected responses
- Dockerized Grafana instance with SQLite plugin integration

## Technologies Used

- Python 3
- SQLite3
- Grafana + frser-sqlite-datasource plugin
- Docker
- Crontab (Linux task scheduling)
- SMTP (for email notifications)

## Project Structure

```
infrapulse/
├── scripts/
│   ├── monitor.py          # Performs health check, logs result, sends alerts
│   ├── db.py               # Initializes and writes to the SQLite database
│   └── email_alert.py      # Sends alert emails
├── grafana-data/           # Persistent volume for Grafana and database
├── Dockerfile              # (Optional) if customizing Grafana further
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/infrapulse.git
   cd infrapulse
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Email Alerts**
   Update credentials and addresses in `scripts/email_alert.py`.

4. **Start Grafana with SQLite Plugin**
   ```bash
   docker run -d \
     -p 80:5000 \
     -v $PWD/grafana-data:/var/lib/grafana \
     -e "GF_INSTALL_PLUGINS=frser-sqlite-datasource" \
     --name grafana \
     grafana/grafana
   ```

5. **Verify Dashboard Setup**
   - Access Grafana at `http://<your-server-ip>/`
   - Add a data source using the SQLite plugin, pointing to `/var/lib/grafana/health_checks.db`
   - Build a dashboard with your preferred visualizations

6. **Enable Periodic Health Checks**
   Add this line to your crontab (`crontab -e`):
   ```
   * * * * * /usr/bin/python3 /home/ec2-user/infrapulse/scripts/monitor.py >> /home/ec2-user/monitor.log 2>&1
   ```

## Customization

- **Health Check Target**: Update `HEALTHCHECK_URL` in `monitor.py`
- **Sleep Interval**: Add a delay if needed (e.g., `time.sleep(2)`)
- **Email Alerts**: Modify messaging or add logic for escalations

