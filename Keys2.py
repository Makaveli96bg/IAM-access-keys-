import boto3
import os
import datetime
from datetime import date
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    email_70_list = []
    email_80_list = []
    email_90_list = []

    unique_user_list = (iam.list_users()['Users'])

    for userlist in unique_user_list:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        
        for keyValue in userKeys['AccessKeyMetadata']:
            UserAccessKeyID = keyValue['AccessKeyId']
            IAMUserName = keyValue['UserName']

            if keyValue['Status'] == 'Active':
                currentdate = date.today()
                active_days = currentdate - keyValue['CreateDate'].date()

                # if Access key age is greater than or equal to 70 days, send warning
                if active_days == datetime.timedelta(days=int(os.environ['days_70'])):
                    email = IAMUserName  # Assuming IAM username is the email address
                    email_70_list.append(email)
                    print(f"This User: {IAMUserName}, is having access key age 70 days")

                # if Access key age is greater than or equal to 80 days, send email alert
                if active_days == datetime.timedelta(days=int(os.environ['days_80'])):
                    email = IAMUserName  # Assuming IAM username is the email address
                    email_80_list.append(email)
                    print(f"The User: {IAMUserName}, is having access key age 80 days")

                # if Access key age is greater than or equal to 90 days, send email alert and inactive access keys
                if active_days >= datetime.timedelta(days=int(os.environ['days_90'])):
                    email = IAMUserName  # Assuming IAM username is the email address
                    email_90_list.append(email)
                    print(f"The User: {IAMUserName}, is having access key age greater than 90 days")

                    # If you want to deactivate the access key, you can uncomment the following lines
                    # iam.update_access_key(AccessKeyId=UserAccessKeyID, Status='Inactive', UserName=IAMUserName)
                    # print("Status has been updated to Inactive")

    # Send email notifications for users with access keys older than 70, 80, and 90 days
    send_email_notifications(email_70_list, os.environ['SUBJECT_70'], os.environ['BODY_TEXT_70'], os.environ['BODY_HTML_70'])
    send_email_notifications(email_80_list, os.environ['SUBJECT_80'], os.environ['BODY_TEXT_80'], os.environ['BODY_HTML_80'])
    send_email_notifications(email_90_list, os.environ['SUBJECT_90'], os.environ['BODY_TEXT_90'], os.environ['BODY_HTML_90'])

def send_email_notifications(recipients, subject, body_text, body_html):
    if recipients:
        RECIPIENTS = list(set(recipients))
        SENDER = os.environ['sender_email']
        AWS_REGION = os.environ['region']
        CHARSET = "UTF-8"

        client = boto3.client('ses', region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': RECIPIENTS,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': subject,
                    },
                },
                Source=SENDER,
            )
            print("Email sent! Message ID:", response['MessageId'])
        except ClientError as e:
            print(e.response['Error']['Message'])

# Ensure to replace the placeholders in the send_email_notifications function with your actual subject, body_text, and body_html.
