import os
import time
import requests
import google.generativeai as genai
from prometheus_api_client import PrometheusConnect

genai.configure(api_key="AIzaSyCajPD9uYRvQA4Q_oJX6hqKbu5OJK1cJ2g")
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

print("✅ Script started successfully.")
def check_cpu_spike(threshold=80.0, duration=120):
    print("📡 Checking CPU usage from Prometheus...")
    print("⚠️ Simulating CPU spike... Returning True.")
    return True  # Simulate spike for testing
def get_logs():
    print("📄 Fetching logs from 'stress-test' container...")
    try:
        logs = os.popen("docker exec stress-test cat /app/app.log").read()
        print("🪵 Logs fetched:\n" + logs[:300])
        return logs
    except Exception as e:
        print("❌ Error retrieving logs:", e)
        return "Error retrieving logs."
def analyze_logs(log_text):
    print("🧠 Sending logs to Gemini (flash model)...")
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(log_text)
        print("🧠 Gemini response received.")
        return response.text
    except Exception as e:
        print("❌ Gemini error:", e)
        return "Gemini analysis failed."
def remediate():
    print("🔁 Restarting 'stress-test' container...")
    try:
        os.system("docker restart stress-test")
        print("✅ Container restarted successfully.")
        return "Container restarted successfully."
    except Exception as e:
        print("❌ Error restarting container:", e)
        return "Failed to restart container."
def notify(message):
    print("📢 Sending Slack notification...")
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code == 200:
            print("✅ Slack notification sent.")
        else:
            print(f"❌ Slack error: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Slack request failed:", e)
def main():
    print("🚀 DevOps AI Agent started.")

    if check_cpu_spike():
        print("⚠️ CPU spike detected! Continuing to log analysis...")

        logs = get_logs()
        analysis = analyze_logs(logs)
        print("🧠 Gemini Analysis:\n", analysis)

        if any(word in analysis.lower() for word in ["infinite loop", "outofmemory", "memory leak"]):
            action = remediate()
        else:
            action = "No automatic action taken. Manual review required."

        print("📣 Final Action:", action)

        notify(f"""
🚨 *CPU Spike Detected!*
📋 *Gemini Analysis:* {analysis}
⚙️ *Action Taken:* {action}
        """)
    else:
        print("✅ No CPU spike detected. Exiting.")

# ▶️ Run the agent
if __name__ == "__main__":
    main()
