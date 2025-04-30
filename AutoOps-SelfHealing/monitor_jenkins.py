import requests
import time
import smtplib
from email.mime.text import MIMEText

# Jenkins API details
jenkins_url = 'http://localhost:8080'  # Replace with your Jenkins server URL
job_name = 'AutoOps-CI-CD'  # Replace with your Jenkins job name
jenkins_user = 'Supriya'  # Replace with your Jenkins username (if using basic auth)
jenkins_token = '11d6bdca67881ab65f83f53c712c7ac8c6'  # Replace with your Jenkins API token

# Retry settings
max_retries = 3
retry_interval = 10  # Time in seconds between retries

# Email settings
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
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Alert sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check Jenkins job status
def check_job_status():
    url = f'{jenkins_url}/job/{job_name}/lastBuild/api/json'
    response = requests.get(url, auth=(jenkins_user, jenkins_token))

    if response.status_code == 200:
        data = response.json()
        build_status = data['result']
        print(f"Build status: {build_status}")
        return build_status
    else:
        print(f"Failed to fetch job status: {response.status_code}")
        return None

# Retry logic for job
def monitor_jenkins_job():
    retries = 0 
    while retries < max_retries:
        status = check_job_status()

        if status == "SUCCESS":
            print("Job succeeded.")
            break
        elif status == "FAILURE":
            retries += 1
            print(f"Job failed. Retry {retries}/{max_retries}...")
            time.sleep(retry_interval)
        else:
            print("Job is still in progress...")

    if retries == max_retries:
        send_email("Jenkins Job Failure Alert", "The job has failed after maximum retries.")
        print("Max retries reached. Failure alert sent.")

if __name__ == "__main__":
    monitor_jenkins_job()
