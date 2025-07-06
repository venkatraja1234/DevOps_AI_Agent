import requests

# Your Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_notification(message):
    payload = {"text": message}
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("✅ Slack notification sent.")
        else:
            print(f"❌ Failed to send notification. Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"⚠️ Error sending notification: {e}")
