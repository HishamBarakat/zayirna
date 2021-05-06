import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.client("dynamodb")
    dynamodb.put_item(TableName="OnlineUsers", Item={"connectionID": {"S": event["requestContext"].get("connectionId")}})


    return {
        'statusCode': 200,
        'body': json.dumps('Connected')
    }
