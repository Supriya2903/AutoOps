import requests
import time
import smtplib
from email.mime.text import MIMEText
from requests.auth import HTTPBasicAuth

# Jenkins API details
jenkins_url = 'http://localhost:8080'
job_name = 'AutoOps-CI-CD'
jenkins_user = 'Supriya'
jenkins_token = '11d6bdca67881ab65f83f53c712c7ac8c6'

# Retry settings
max_retries = 3
retry_interval = 10  # seconds
max_wait_time = 300  # total wait time for building job, in seconds

# Email settings (dummy placeholders - replace with real values)
sender_email = "youremail@example.com"
receiver_email = "receiver@example.com"
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_user = "youremail@example.com"
smtp_password = "your-email-password"

# Function to send email alert
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Alert sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check Jenkins job status
def check_job_status():
    url = f'{jenkins_url}/job/{job_name}/lastBuild/api/json'
    try:
        response = requests.get(url, auth=HTTPBasicAuth(jenkins_user, jenkins_token))
        if response.status_code == 200:
            data = response.json()
            if data.get('building'):
                return 'BUILDING'
            else:
                return data.get('result')  # "SUCCESS", "FAILURE", etc.
        else:
            print(f"Failed to fetch job status: {response.status_code}")
            return 'ERROR'
    except Exception as e:
        print(f"Exception while checking job status: {e}")
        return 'ERROR'

# Monitor Jenkins job with retry + timeout
def monitor_jenkins_job():
    retries = 0
    total_wait = 0

    while retries < max_retries:
        status = check_job_status()

        if status == "SUCCESS":
            print("✅ Job succeeded.")
            return
        elif status == "FAILURE":
            retries += 1
            print(f"❌ Job failed. Retrying ({retries}/{max_retries})...")
            time.sleep(retry_interval)
        elif status == "BUILDING":
            if total_wait >= max_wait_time:
                print("⏱️ Job stuck in building state. Timeout reached.")
                break
            print("🔄 Job is still in progress...")
            total_wait += retry_interval
            time.sleep(retry_interval)
        else:  # status == 'ERROR' or unexpected
            print("⚠️ Error occurred or unauthorized access.")
            break

    # Final failure alert
    send_email("🚨 Jenkins Job Alert", f"Job '{job_name}' did not complete successfully after retries.")
    print("📧 Failure alert sent.")

if __name__ == "__main__":
    monitor_jenkins_job()
