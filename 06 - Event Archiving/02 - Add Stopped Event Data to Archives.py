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

dynamo = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')

def lambda_handler(event, context):
    for record in event['Records']:
	   #ensure that an update is what triggered the function, and the updated record is one of the aggregate values
        if record['eventName'] == "MODIFY" and record["dynamodb"]["NewImage"]["status"]["S"] == "Stopped":
            eventID = record["dynamodb"]["NewImage"]["eventID"]["S"]
            
            print("the edited ID is: " + eventID)
            
            #getting event information (start/stop/organizer info) without the faces detected in the event
            response = table.query(KeyConditionExpression=Key('partitionKey').eq(eventID) & Key('metadata').begins_with('DATE'))
   
            #get the total aggregates by querying the table to get all data with partition key "AGGREGATES"
            totalUnique = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentUnique'))
            totalRedundant = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentRedundant'))
            totalMales = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentMales'))
            totalFemales = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentFemales'))
            totalAdults = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentAdults'))
            totalChildren = table.query(KeyConditionExpression=Key('partitionKey').eq('AGGREGATES') & Key('metadata').eq('currentChildren'))
            
            for i in totalUnique['Items']:
                totalUnique = i['aggregateValue']
                
            for i in totalRedundant['Items']:
                totalRedundant = i['aggregateValue']
            
            for i in totalMales['Items']:
                totalMales = i['aggregateValue']
            
            for i in totalFemales['Items']:
                totalFemales = i['aggregateValue']
                
            for i in totalAdults['Items']:
                totalAdults = i['aggregateValue']
                
            for i in totalChildren['Items']:
                totalChildren = i['aggregateValue']
            
            
            for eventData in response['Items']:
                startDate = eventData['startDate']
                startTime = eventData['startTime']
                endDate = eventData['endDate']
                endTime = eventData['endTime']
                eventName = eventData['eventName']
                organizerName = eventData['organizerName']
                organizerName = eventData['organizerName']
                organizerEmail = eventData['organizerEmail']
                organizerPhone = eventData['organizerPhone']
                
                
                
                #dump the data into the archives
                response2 = dynamo.put_item(
                    TableName= 'EventsArchive', 
                    Item={
                    'eventID': {'S': eventID},
                    'eventName': {'S': eventName},
                    'startDate': {'S': startDate},
                    'startTime': {'S': startTime},
                    'endDate': {'S': endDate},
                    'endTime': {'S': endTime},
                    'organizerName': {'S': organizerName},
                    'organizerEmail': {'S': organizerEmail},
                    'organizerPhone': {'S': organizerPhone},
                    'unique':{'N': str(int(totalUnique))},
                    'redundant':{'N': str(int(totalRedundant))},
                    'males':{'N': str(int(totalMales))},
                    'females':{'N': str(int(totalFemales))},
                    'adults':{'N': str(int(totalAdults))},
                    'children':{'N': str(int(totalChildren))}
                })
                
            
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentUnique'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentRedundant'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentMales'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentFemales'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentAdults'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            response = table.update_item(
                Key={
                    'partitionKey': 'AGGREGATES',
                    'metadata': 'currentChildren'
                    },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='set aggregateValue= :d',
                ExpressionAttributeValues={':d': 0}
                )
            print(response)
                
                
            #dynamodbDelete = boto3.resource('dynamodb')
            #tableDelete = dynamodbDelete.Table('ScheduledEvents')
            #tableDelete.delete_item(
                #Key={
                    #'eventID': eventID
                #}
            #)
