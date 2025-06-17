# scripts/email_alert.py

import boto3
from botocore.exceptions import ClientError

def send_email(subject, body, sender, recipient):
    ses = boto3.client('ses', region_name='us-east-1')

    try:
        response = ses.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}},
            },
        )
        print(f"Email sent: {response['MessageId']}")
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")
