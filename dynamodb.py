import boto3
from botocore.exceptions import ClientError

client_dynamodb =boto3.client('dynamodb','ap-south-1')

class Book:

    def put_item(self, category, title, language, ):
        response = client_dynamodb.put_item(
            TableName='Books',
            Item={
                'category': {
                    'N': category
                    ,
                },
                'title': {
                    'S': title,
                },
                'language': {
                    'S': language
                },



            }
        )
        print("Loading data")
        return response


    def get_item(self, category, title):
        try:
            response = client_dynamodb.get_item(
                TableName='Books',
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
            return response['Item']


    def update_book(self, category, title, language, rating):
        response = client_dynamodb.update_item(

            Key={
                'category': {
                    'S': category,
                },
                'title': {
                    'S': title,
                }
            },

            UpdateExpression="set language=:l, rating=:r",
            ExpressionAttributeValues={
                ':l': language,
                ':r': rating
            },
            ReturnValues="UPDATED_NEW"
        )
        return response


    def delete_underrated_book(self, title, category, rating):
            try:
                response = client_dynamodb.delete_item(
                    TableName='TableOfBooks',
                    Key={
                        'category': {
                            'N': "{}".format(category),
                        },
                        'title': {
                            'S': "{}".format(title),
                        }
                    },
                    ConditionExpression="rating <= :a",
                    ExpressionAttributeValues={
                        ':a': {
                            'N': "{}".format(rating),
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
                TableName='TableOfBooks',
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
            print("rating increased")
            return response

    # response = client_dynamodb.batch_write_item(
    #     RequestItems={
    #         'string': [
    #             {
    #                 'PutRequest': {
    #                     'Item': {
    #                         'string': {
    #                             'S': '',
    #                             'N':