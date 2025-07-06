import time
from monitor import (
    check_cpu_spike,
    get_memory_usage,
    get_disk_usage,
    get_network_rx
)
from log_fetcher import fetch_logs
from analyzer import analyze_logs
from remediation import remediate
from notifier import send_notification
from incident_logger import log_incident

def main():
    print("🚀 DevOps AI Agent running...")

    while True:
        # Fetch system metrics
        memory = get_memory_usage()
        disk = get_disk_usage()
        network = get_network_rx()
        print(f"📊 System Metrics → Memory: {memory:.2f}%, Disk: {disk:.2f}%, Network RX: {network:.2f} MB/s")

        if check_cpu_spike():
            print("⚠️ CPU spike detected!")
            logs = fetch_logs()
            analysis = analyze_logs(logs)
            print("🧠 LLM Analysis:", analysis)

            if "infinite loop" in analysis.lower() or "memory leak" in analysis.lower():
                action = remediate()
                status = "✅ Auto-remediation performed."
            else:
                action = "❗ Manual review required."
                status = "⏸ Awaiting human action."

            # ✅ Record to local SQLite DB
            current_cpu = 85.0  
            log_incident(current_cpu, analysis, action)

            message = f"""
🚨 *CPU Spike Detected*
🧾 *Analysis*: {analysis}
🔧 *Action Taken*: {action}
📊 *Status*: {status}
💾 *Memory*: {memory:.2f}%
🗄 *Disk*: {disk:.2f}%
📶 *Network RX*: {network:.2f} MB/s
"""
            send_notification(message)
            print("📤 Slack alert sent.")
            time.sleep(300)
        else:
            print("✅ System normal.")
            time.sleep(60)

if __name__ == "__main__":
    main()
