import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import ast
from decimal import Decimal
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def lambda_handler(event, context):
    
    
    dynamo = boto3.client("dynamodb")
    scan = dynamo.scan(TableName = "EventsArchive")
        
    PastEvents = []
    for i in scan['Items']:
        d = ast.literal_eval(json.dumps(i, cls=DecimalEncoder))
        PastEvents.append(d)
    
    print(PastEvents)
        
    return {
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(PastEvents)

    }
