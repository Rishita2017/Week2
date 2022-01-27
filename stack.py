import boto3
from botocore.client import ClientError

class Stack:
    def __init__(self, stack_name, template_url, region):
        self.stack_name = stack_name
        self.template_url = template_url
        self.client_cloudformation = boto3.client('cloudformation', region_name=region)
        self.client_dynamodb = boto3.client('dynamodb',region_name = region)

    def create_stack(self):
        try:
            self.client_cloudformation.create_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM']

            )
        except ClientError as ce:
            print(ce)
    def update_stack(self):
        try:
            self.client_cloudformation.update_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],

            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("Stack Already Updated")
            else:
                print(ce)