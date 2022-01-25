import boto3
from botocore.exceptions import ClientError
client_dynamodb = boto3.client('dynamodb')


def book():
    table = client_dynamodb.create_table(
        TableName='TableOfTable',
        KeySchema=[
            {
                'AttributeName': 'Category',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Category',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Language',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Creating Table")
    return table


def put_movie(category, title, language):
    response = client_dynamodb.put_item(
        TableName='TableOfBook',
        Item={
            'category': {
                'N': "{}".format(category),
            },
            'title': {
                'S': "{}".format(title),
            },
            'language': {
                "S": "{}".format(language),
            },

        }
    )
    print("Loading data")
    return response


def get_movie(category, title):
    try:
        response = client_dynamodb.get_item(
            TableName='TableOfBook',
            Key={
                'category': {
                    'S': "{}".format(category),
                },
                'title': {
                    'S': "{}".format(title),
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def update_movie(category, title, rating, language, author):
    response = client_dynamodb.update_item(
        TableName='TableOfBook',
        Key={
            'category': {
                'S': "{}".format(category),
            },
            'title': {
                'S': "{}".format(title),
            }
        },
        ExpressionAttributeNames={
            '#R': 'rating',
            '#P': 'language',
            '#A': 'author'
        },
        ExpressionAttributeValues={
            ':r': {
                'N': "{}".format(rating),
            },
            ':p': {
                'S': "{}".format(language),
            },
            ':a': {
                'SS': author,
            }
        },
        UpdateExpression='SET #R = :r, #L = :l, #A = :a',
        ReturnValues="UPDATED_NEW"
    )
    return response


def delete_underrated_book(title, category, rating):
    try:
        response = client_dynamodb.delete_item(
            TableName='TableOfBook',
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
