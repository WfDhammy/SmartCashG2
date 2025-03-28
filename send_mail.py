import os
import json
import http.client
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("MAILERSEND_API_KEY")

def send_mail(sender: str, recipient: str, subject: str, content: str):
    conn = http.client.HTTPSConnection("api.mailersend.com")

    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = json.dumps({
        "from": {"email": sender},
        "to": [{"email": recipient}],
        "subject": subject,
        "text": content,
        "html": content
    })
    conn.request("POST", "/v1/email", body=payload, headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    
    conn.close()
    return {"status_code": response.status, "response": data}


if __name__ == "__main__":
    sender_email = "info@domain.com"
    recipient_email = "emekadefirst@gmail.com"
    subject_text = "Hello from MailerSend!"
    message_content = "Greetings from the team, you got this message through MailerSend."
    
    result = send_mail(sender_email, recipient_email, subject_text, message_content)
    print(result)