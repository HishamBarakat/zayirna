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

dynamodb = boto3.resource('dynamodb')
EventsTable = dynamodb.Table('Events')



def lambda_handler(event, context):



    #get the updated aggregates by querying the table to get all data with partition key "AGGREGATES"
    response = EventsTable.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES'))

    #converting query result to json and save it into an array
    aggregatesJSON = []
    for i in response['Items']:
        d = ast.literal_eval(json.dumps(i, cls=DecimalEncoder))
        aggregatesJSON.append(d)

    print(aggregatesJSON)



    return {
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(aggregatesJSON)

    }
