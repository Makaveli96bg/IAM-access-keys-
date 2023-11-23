#uses SES to send emails

import boto3
from datetime import date, timedelta
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    print("All IAM user emails that have AccessKeys 90 days or older")
    email_list = []

    for userlist in iam.list_users()['Users']:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            if keyValue['Status'] == 'Active':
                currentdate = date.today()
                active_days = currentdate - keyValue['CreateDate'].date()

                if active_days >= timedelta(days=90):
                    userTags = iam.list_user_tags(UserName=keyValue['UserName'])
                    email_tag = [tag['Value'] for tag in userTags['Tags'] if tag['Key'] == 'email']

                    if email_tag:
                        email = email_tag[0]
                        email_list.append(email)
                        print(email)

    email_unique = list(set(email_list))
    print(email_unique)

    if email_unique:
        RECIPIENTS = email_unique
        SENDER = "elcloudops@dxc.com"  # Replace with a valid SES verified email address
        AWS_REGION = "eu-central-1"    # Replace the correct AWS Region
        SUBJECT = "Electralink AWS DTS account IAM Access Key Rotation"
        BODY_TEXT = (
            "Your IAM Access Key needs to be rotated in Electralink DTS AWS Account: 628535880471 "
            "as it is 90 days or older. Log into AWS and go to your IAM user to fix: "
            "https://console.aws.amazon.com/iam/home?#security_credential"
        )

        BODY_HTML = (
            "AWS Security: IAM Access Key Rotation: Your IAM Access Key needs to be rotated in "
            "Electralink DTS AWS Account: 628535880471 as it is 90 days or older. Log into AWS and go to your "
            "https://console.aws.amazon.com/iam/home?#security_credential to create a new set of keys. "
            "Ensure to disable/remove your previous key pair."
        )

        CHARSET = "UTF-8"

        client = boto3.client('ses', region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={'ToAddresses': RECIPIENTS},
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
