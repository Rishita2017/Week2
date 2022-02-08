import boto3
from botocore.client import ClientError

class Stack:
    def __init__(self, stack_name, template_body, region):
        self.stack_name = stack_name
        self.template_body = template_body
        self.client_cloudformation = boto3.client('cloudformation', region_name=region)
        self.client_dynamodb = boto3.client('dynamodb',region_name = region)

    def create_stack(self):
        try:
            self.client_cloudformation.create_stack(
                StackName=self.stack_name,
                TemplateBody=self.template_body,
                Capabilities=['CAPABILITY_NAMED_IAM']

            )
            waiter = self.client_cloudformation.get_waiter('stack_create_complete')
            waiter.wait(StackName=self.stack_name, WaiterConfig={
                'Delay': 2,
                'MaxAttemtps': 5
            })
            print("Stack is created...............")
        except ClientError as ce:
            print(ce)
    def update_stack(self):
        try:
            self.client_cloudformation.update_stack(
                StackName=self.stack_name,
                TemplateBody=self.template_body,
                Capabilities=['CAPABILITY_NAMED_IAM'],

            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("Stack Already Updated..................")
            else:
                print(ce)