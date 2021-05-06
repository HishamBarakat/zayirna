import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import ast
from decimal import Decimal
import decimal



#THIS LAMBDA IS TRIGGERED BY DYNAMODB STREAMS IT CHECKS IF THE CHANGE ON THE
#TABLE IS A MODIFY ON THE AGGREGATED VALUES. IF YES IT QUERIES THE TABLE TO GET
#THE MOST RECENT AGGREGATES, CONVERTS THEM TO JSON AND PUSHES THEM TO ALL
#CONNECTED FRONT-END CLIENTTS VIA WEBSOCKET API




# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

deeplensTable = "DeepLens"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')
#s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
	   #ensure that an update is what triggered the function, and the updated record is one of the aggregate values
        if record['eventName'] == "MODIFY" and "aggregateValue" in record["dynamodb"]["NewImage"]:

            #get the updated aggregates by querying the table to get all data with partition key "AGGREGATES"
            response = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES'))

            #converting query result to json and save it into an array
            aggregatesJSON = []
            for i in response['Items']:
                d = ast.literal_eval(json.dumps(i, cls=DecimalEncoder))
                aggregatesJSON.append(d)

            tableDeepLens = dynamodb.Table(deeplensTable)
            resp = tableDeepLens.scan()
            deepLenses = resp['Items']
            for eachDeepLens in deepLenses:
                aggregatesJSON.append(eachDeepLens)

            #Websocket API connection endpoint
            URL = "https://8wv8wzrnql.execute-api.us-east-1.amazonaws.com/dev"
            API = boto3.client("apigatewaymanagementapi", endpoint_url = URL)


            #get all currently connected users from table
            dynamo = boto3.client("dynamodb")
            scan = dynamo.scan(TableName = "OnlineUsers")

            #sending out new aggregates to all connected clients
            for connection in scan["Items"]:
                result = API.post_to_connection(ConnectionId=connection["connectionID"]["S"], Data=json.dumps(aggregatesJSON))





    
