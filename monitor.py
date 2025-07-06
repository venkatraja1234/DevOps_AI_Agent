from prometheus_api_client import PrometheusConnect
from config import PROMETHEUS_URL, CPU_THRESHOLD

# Connect to Prometheus

prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)


def get_cpu_usage():
    try:
        query = '100 - (avg(rate(node_cpu_seconds_total{mode="idle",job="node_exporter"}[30s])) * 100)'
        result = prom.custom_query(query)

        # 🔍 Debug print
        print("📊 Raw Prometheus result:", result)

        if result and 'value' in result[0]:
            usage = float(result[0]['value'][1])
            print(f"✅ Parsed CPU Usage = {usage}%")
            return usage
        else:
            print("⚠️ No CPU usage data returned by Prometheus.")
            return 0.0
    except Exception as e:
        print(f"Error checking CPU usage: {e}")
        return 0.0

# ✅ CPU Spike Detection (real version)
def check_cpu_spike():
    query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    try:
        result = prom.custom_query(query)
        cpu_usage = float(result[0]['value'][1])
        print(f"CPU usage: {cpu_usage:.2f}%")
        return cpu_usage >= CPU_THRESHOLD
    except Exception as e:
        print("Error checking CPU usage:", e)
        return False

# ✅ Memory Usage (%)
def get_memory_usage():
    query = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
    try:
        result = prom.custom_query(query)
        return round(float(result[0]['value'][1]), 2)
    except:
        return 0.0

# ✅ Disk Usage (%)
def get_disk_usage():
    query = '(node_filesystem_size_bytes{fstype!~"tmpfs|sysfs"} - node_filesystem_free_bytes{fstype!~"tmpfs|sysfs"}) / node_filesystem_size_bytes{fstype!~"tmpfs|sysfs"} * 100'
    try:
        result = prom.custom_query(query)
        return round(float(result[0]['value'][1]), 2)
    except:
        return 0.0

# ✅ Network Receive (in MB/s)
def get_network_rx():
    query = 'rate(node_network_receive_bytes_total[1m])'
    try:
        result = prom.custom_query(query)
        return round(float(result[0]['value'][1]) / (1024 * 1024), 2)  # Convert to MB/s
    except:
        return 0.0
