# DevOps AI Agent

## Overview
The DevOps AI Agent is a Python-based system designed to monitor system metrics, detect performance issues (e.g., CPU spikes), analyze logs using Google's Gemini AI, perform automated remediation, log incidents, and send notifications via Slack. It includes a Streamlit-based dashboard for real-time metrics visualization, log viewing, AI-driven log analysis, and manual remediation.

The system integrates with Prometheus for metrics collection, Docker for log fetching and container management, SQLite for incident logging, and Slack for notifications. It is designed to help DevOps teams monitor and maintain system health efficiently.

## Features
- **System Monitoring**: Tracks CPU, memory, disk, and network usage via Prometheus.
- **CPU Spike Detection**: Detects high CPU usage (threshold: 80%) and triggers log analysis.
- **Log Analysis**: Uses Gemini AI to analyze logs and identify issues like infinite loops or memory leaks.
- **Automated Remediation**: Restarts the `stress-test` Docker container if specific issues are detected.
- **Incident Logging**: Stores incident details (timestamp, CPU usage, analysis, action) in a SQLite database.
- **Slack Notifications**: Sends alerts with analysis and remediation details.
- **Streamlit Dashboard**: Displays real-time metrics, logs, Gemini analysis, and manual remediation controls.

## Project Structure
- `main_controller.py`: Orchestrates the agent, continuously monitoring metrics, analyzing logs, and handling remediation and notifications.
- `main_agent.py`: A simplified, single-run version of the agent for testing CPU spike scenarios.
- `monitor.py`: Fetches system metrics (CPU, memory, disk, network) from Prometheus and checks for CPU spikes.
- `log_fetcher.py`: Retrieves logs from the `stress-test` Docker container.
- `analyzer.py`: Analyzes logs using Gemini AI to identify performance issues.
- `remediation.py`: Performs automated remediation (e.g., restarting the `stress-test` container).
- `incident_logger.py`: Logs incidents to a SQLite database (`incidents.db`).
- `notifier.py`: Sends notifications to a Slack webhook.
- `dashboard.py`: Streamlit-based dashboard for metrics, logs, analysis, and manual remediation.
- `config.py`: Configuration file with Prometheus URL, CPU threshold, container name, Gemini API key, and Slack webhook URL.
- `list_models.py`: Lists available Gemini models.
- `check_models.py`: Lists Gemini models and their supported methods.
- `requirements.txt`: Lists dependencies (`google-generativeai`).
- `logs.txt`: Placeholder for storing logs (currently empty).

## Prerequisites
- Python 3.8+
- Docker (with a running `stress-test` container)
- Prometheus server running at `http://localhost:9090`
- Node Exporter for collecting system metrics in Prometheus
- SQLite (included with Python)
- Slack webhook for notifications
- Google Gemini API key

## Setup
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd devops-ai-agent
   ```

2. **Install Dependencies**
   Create a virtual environment and install required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Sensitive Data**
   The Gemini API key and Slack webhook URL are stored in `config.py`. Replace the placeholder values in `config.py` with your actual credentials:
   ```python
   GEMINI_API_KEY = "your_gemini_api_key"
   SLACK_WEBHOOK_URL = "your_slack_webhook_url"
   ```
   **Security Note**: Avoid hardcoding sensitive data in production. Consider using a secure vault or environment-specific configuration.

4. **Configure Prometheus**
   Ensure a Prometheus server is running at `http://localhost:9090`. Configure Node Exporter to collect system metrics (e.g., CPU, memory, disk, network) and ensure Prometheus scrapes these metrics.

5. **Set Up Docker**
   Ensure the `stress-test` Docker container is running and has logs accessible at `/app/app.log`. Verify Docker commands can be executed by the user running the scripts.

6. **Start the Streamlit Dashboard (Optional)**
   ```bash
   streamlit run dashboard.py
   ```

## Usage
- **Run the Main Controller**
   Start the continuous monitoring agent:
   ```bash
   python main_controller.py
   ```
   The agent will:
   - Monitor CPU, memory, disk, and network usage every 60 seconds.
   - Detect CPU spikes (>80%) and fetch logs from the `stress-test` container.
   - Analyze logs with Gemini AI.
   - Restart the container if an infinite loop or memory leak is detected, or flag for manual review.
   - Log incidents to `incidents.db`.
   - Send Slack notifications with analysis and actions.

- **Run the Single-Run Agent**
   Test the agent with a simulated CPU spike:
   ```bash
   python main_agent.py
   ```

- **Access the Dashboard**
   Open the Streamlit dashboard in your browser (default: `http://localhost:8501`) to:
   - View real-time system metrics.
   - Display the latest 50 lines of `/var/log/syslog`.
   - Run Gemini log analysis.
   - Manually restart a Docker container.

- **List Gemini Models**
   Check available Gemini models:
   ```bash
   python list_models.py
   ```

- **Check Model Capabilities**
   View supported methods for Gemini models:
   ```bash
   python check_models.py
   ```

## Security Notes
- **Hardcoded Credentials**: The Gemini API key and Slack webhook URL are hardcoded in `config.py`, `main_agent.py`, `dashboard.py`, `list_models.py`, and `check_models.py`. In production, use a secure method (e.g., a secrets manager) to manage these credentials.
- **Docker Commands**: Ensure the `stress-test` container exists and is accessible. Secure Docker commands to prevent unauthorized access.
- **Prometheus**: The `monitor.py` script disables SSL verification for testing. In production, enable SSL and secure the Prometheus endpoint.

## Future Improvements
- Enhance error handling for network failures or missing containers.
- Implement log rotation for `logs.txt` and `incidents.db`.
- Support multiple containers for log fetching and remediation.
- Add more remediation strategies (e.g., scaling resources, killing processes).
- Enhance the dashboard with charts for historical metrics.
- Integrate additional monitoring tools (e.g., Grafana).

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs, features, or improvements.
