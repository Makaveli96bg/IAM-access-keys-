# How to Get the list of IAM users whose access keys are older than 90 days and send the email?
list of IAM users whose access keys are older than 90 days and send the email


Prerequisites:

IAM users with proper tags(key=email & value=email_ID).
verified emails of all the users in the AWS SES service.
lambda execution role with IAMFullAccess and AmazonSESFullAccess.

STEP: 1 Create a lambda function with python runtime and choose the lambda execution role created in the Prerequisites section. Go to general configuration and give sufficient memory and timeout


STEP: 2 Paste the below code in the lambda function to fetch the IAM users whose access key is older than N days(here N=90 days).

NOTE: This script exludes all the service accounts from the IAM user list.

RESULT: you should get the below response after executing the lambda function.

<Test Event Name
test
Response
null
Function Logs
START RequestId: 6862780d-a314-45df-86b6-25435a12a7da Version: $LATEST
All IAM user emails that have AccessKeys 90 days or older
bhanu.prathap@gmail.com
['bhanu.prathap@gmail.com']
END RequestId: 6862780d-a314-45df-86b6-25435a12a7da
REPORT RequestId: 6862780d-a314-45df-86b6-25435a12a7da Duration: 2747.23 ms Billed Duration: 2748 ms Memory Size: 1280 MB Max Memory Used: 65 MB Init Duration: 371.84 ms
Request ID
6862780d-a314-45df-86b6-25435a12a7da>



you should get the email for the expired user
