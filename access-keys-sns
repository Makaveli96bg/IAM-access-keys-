#This lambda send email with sns topic 

import boto3
from datetime import date, timedelta
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    print("IAM users with AccessKeys 3 days or older")

    old_keys_info = []

    for userlist in iam.list_users()['Users']:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            if keyValue['Status'] == 'Active':
                currentdate = date.today()
                active_days = (currentdate - keyValue['CreateDate'].date()).days

                if active_days >= 3:
                    userTags = iam.list_user_tags(UserName=userlist['UserName'])
                    email_tag = [tag['Value'] for tag in userTags['Tags'] if tag['Key'] == 'email']

                    if email_tag:
                        email = email_tag[0]
                        old_keys_info.append(f"User: {userlist['UserName']}, Email: {email}, AccessKey Created: {keyValue['CreateDate']}")

    if old_keys_info:
        RECIPIENT = "elcloudops@dxc.com"  # Replace with the recipient's email address
        SENDER = "elcloudops@dxc.com"     # Replace with a valid SES verified email address
        AWS_REGION = "eu-central-1"       # Replace the correct AWS Region
        SUBJECT = "IAM Access Keys Rotation Report"

        BODY_TEXT = "\n".join(old_keys_info)
        BODY_HTML = f"<p>{'<br>'.join(old_keys_info)}</p>"

        CHARSET = "UTF-8"

        client = boto3.client('ses', region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={'ToAddresses': [RECIPIENT]},
                Message={
                    'Body': {
                        'Html': {'Charset': CHARSET, 'Data': BODY_HTML},
                        'Text': {'Charset': CHARSET, 'Data': BODY_TEXT},
                    },
                    'Subject': {'Charset': CHARSET, 'Data': SUBJECT},
                },
                Source=SENDER,
            )
            print("Email sent! Message ID:", response['MessageId'])
        except ClientError as e:
            print("Error sending email:", e.response['Error']['Message'])
