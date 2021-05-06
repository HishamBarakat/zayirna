import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.client('dynamodb')
dynamo = boto3.resource('dynamodb')
table = dynamo.Table('ScheduledEvents')

def lambda_handler(event, context):
    for record in event['Records']:
        #check if TTL record has expired which triggered this stream
        if record['eventName'] == "REMOVE":
            
            #get the eventID value of deleted record
            eventIDType = record['dynamodb']['OldImage']['eventID']['S']
            
            #split the value by - to get status and eventID
            eventData = eventIDType.split('-')

            eventStatus = eventData[0]

            #update the the table based on the status
            #if eventStatus == "START":
                #response = dynamodb.put_item(
                    #TableName= 'ScheduledEvents', 
                    #Item={
                        #'eventID': {'S': eventData[1]},
                        #'status': {'S': 'Running'}
                        #}
                #) 
            if eventStatus == "START":  
                response = table.update_item(
                    Key={
                            'eventID':  eventData[1],
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='SET #st = :d',
                    ExpressionAttributeValues={':d': 'Running'},
                    ExpressionAttributeNames={'#st': 'status'}

                ) 
                
            if eventStatus == "STOP":
                response = table.update_item(
                    Key={
                            'eventID':  eventData[1],
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='SET #st = :d',
                    ExpressionAttributeValues={':d': 'Stopped'},
                    ExpressionAttributeNames={'#st': 'status'}

                ) 
                
            if eventStatus == "ONHOLD":
                response = table.update_item(
                    Key={
                            'eventID': eventData[1],
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='SET #st = :d',
                    ExpressionAttributeValues={':d': 'OnHold'},
                    ExpressionAttributeNames={'#st': 'status'}
                ) 
                
            if eventStatus == "RESTART":
                response = table.update_item(
                    Key={
                            'eventID':  eventData[1],
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='SET #st =:d',
                    ExpressionAttributeValues={':d': 'Running'},
                    ExpressionAttributeNames={'#st': 'status'}

                ) 
            
            print(record)
