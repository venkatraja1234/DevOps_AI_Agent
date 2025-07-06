import streamlit as st
import subprocess
import google.generativeai as genai
from monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_rx

genai.configure(api_key="AIzaSyCajPD9uYRvQA4Q_oJX6hqKbu5OJK1cJ2g")  # Use .env in production
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="DevOps AI Agent", layout="wide")

st.title("🚀 DevOps AI Agent Dashboard")
st.markdown("Real-time Monitoring | LLM Log Analysis | Auto Remediation")

tab1, tab2, tab3, tab4 = st.tabs(["📊 System Metrics", "📋 Logs", "🤖 Analysis", "🛠 Remediation"])
with tab1:
    st.subheader("Live System Metrics")

    cpu = get_cpu_usage()
    mem = get_memory_usage()
    disk = get_disk_usage()
    net = get_network_rx()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CPU Usage", f"{cpu:.4f}%")
    col2.metric("Memory Usage", f"{mem:.2f}%")
    col3.metric("Disk Usage", f"{disk:.2f}%")
    col4.metric("Network RX", f"{net:.2f} MB/s")

with tab2:
    st.subheader("Latest System Logs")
    logs = subprocess.getoutput("tail -n 50 /var/log/syslog")
    st.text_area("System Logs", logs, height=300)
with tab3:
    st.subheader("Analyze Logs with Gemini")
    if st.button("Run Gemini Analysis"):
        with st.spinner("Analyzing logs..."):
            logs = subprocess.getoutput("tail -n 50 /var/log/syslog")
            prompt = f"""
You are a Gemini-powered DevOps assistant. Analyze the following system logs and identify potential causes of high CPU usage:
Logs:
{logs}
"""
            try:
                response = model.generate_content(prompt)
                st.text_area("Gemini Output", response.text, height=300)
            except Exception as e:
                st.error(f"Gemini error: {str(e)}")
with tab4:
    st.subheader("Manual Remediation")
    container = st.text_input("Container name (Docker)")
    if st.button("Restart Container"):
        if container:
            output = subprocess.getoutput(f"docker restart {container}")
            st.success(output)
        else:
            st.warning("Please enter a container name.")
