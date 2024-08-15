import boto3
from datetime import date, timedelta
from botocore.exceptions import ClientError

iam = boto3.client('iam')
sns = boto3.client('sns')

def lambda_handler(event, context):
    print("IAM users with AccessKeys 90 days or older")

    old_keys_info = []

    for userlist in iam.list_users()['Users']:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            if keyValue['Status'] == 'Active':
                currentdate = date.today()
                active_days = (currentdate - keyValue['CreateDate'].date()).days

                if active_days >= 90:
                    userTags = iam.list_user_tags(UserName=userlist['UserName'])
                    email_tag = [tag['Value'] for tag in userTags['Tags'] if tag['Key'] == 'email']

                    if email_tag:
                        email = email_tag[0]
                        old_keys_info.append(f"User: {userlist['UserName']}, Email: {email}, AccessKey Created: {keyValue['CreateDate']}")

    if old_keys_info:
        TOPIC_ARN = "arn:aws:sns:eu-west-2:628535880471:Blackhole_CloudOps"  # Replace with the SNS topic ARN
        SUBJECT = "DTS account IAM Access Keys Rotation Report"

        MESSAGE_BODY = "\n".join(old_keys_info)

        try:
            response = sns.publish(
                TopicArn=TOPIC_ARN,
                Subject=SUBJECT,
                Message=MESSAGE_BODY
            )
            print("Notification sent! Message ID:", response['MessageId'])
        except ClientError as e:
            print("Error sending SNS notification:", e.response['Error']['Message'])
