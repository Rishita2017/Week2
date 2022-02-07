import boto3
from botocore.exceptions import ClientError

client_dynamodb = boto3.client('dynamodb', 'ap-south-1')


class Book:

    def put_item(self, category, title, language, year):
        response = client_dynamodb.put_item(
            TableName='TableOfBooks',
            Item={
                'category': {
                    'S': category
                    ,
                },
                'title': {
                    'S': title,
                },
                'language': {
                    'S': language,
                },
                'year': {
                    'N': year,
                }

            }
        )
        print("Loading data")
        return response


    def get_item( self, category, title):
        try:
            response = client_dynamodb.get_item(
                TableName='TableOfBooks',
                Key={
                    'category': {
                        'S': category,
                    },
                    'title': {
                        'S': title,
                    }
                }

            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print(response['Item'])

    def update_book(self,category, title, language, year, rating):
        response = client_dynamodb.update_item(
            TableName='Tableofbooks',
            Key={
                'category': {
                    'S': category,
                },
                'title': {
                    'S': title,
                }
            },
            ExpressionAttributeNames={
                '#L': 'language',
                '#Y': 'year',
                '#R': 'rating'
            },
            ExpressionAttributeValues={
                ':l': {
                    'S': language,
                },
                ':y': {
                    'N': year,
                },
                ':r': {
                    'N': rating,
                }
            },
            UpdateExpression='SET #L = :l, #Y = :y, #R= :r',
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_underratedbook(self, category, title, rating):
        try:
            response = client_dynamodb.delete_item(
                TableName='Tableofbooks',
                Key={
                    'category': {
                        'S': category,
                    },
                    'title': {
                        'S': title,
                    }
                },
                ConditionExpression="rating <= :a",
                ExpressionAttributeValues={
                    ':a': {
                        'N': rating,
                    }
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            return response

    def increase_rating(self, category, title, rating_increase):
        response = client_dynamodb.update_item(
            TableName='Tableofbooks',
            Key={
                'category': {
                    'S': category,
                },
                'title': {
                    'S': title,
                }
            },
            ExpressionAttributeNames={
                '#R': 'rating'
            },
            ExpressionAttributeValues={
                ':r': {
                    'N': rating_increase,
                }
            },
            UpdateExpression='SET #R = #R + :r',
            ReturnValues="UPDATED_NEW"
        )
        print("Rating increase")
        return response


    # Batch Crud operation

