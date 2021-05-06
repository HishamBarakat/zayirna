import boto3
import json
import os

#THIS LAMBDA IS TRIGGERED BY DYNAMODB STREAMS ON EVENTS TABLE. IT CHECKS IF THE
#TRIGGER WAS AN INSERT OF NEW FACE DATA. IF YES IT USES THE NEW IMAGE DATA TO
#UPDATE THE AGGREGATE VALUES IN THE EVENTS TABLE

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')


def lambda_handler(event, context):

    for record in event['Records']:
        if record['eventName'] == "INSERT" and "faceID" in record["dynamodb"]["NewImage"]:

            #Aggregation #1: update total adult count
            if record['dynamodb']['NewImage']['ageGroup']['S'] == "Adult":

                response = table.update_item(
                    Key={
                         'partitionKey': 'AGGREGATES',
                            'metadata': 'currentAdults'
                         },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )

        #Aggregation #2: update total children count
            if record['dynamodb']['NewImage']['ageGroup']['S'] == "Child":
                response = table.update_item(
                    Key={
                        'partitionKey': 'AGGREGATES',
                        'metadata': 'currentChildren'
                         },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )

        #Aggregation #3: update total Female count
            if record['dynamodb']['NewImage']['gender']['S'] == "Female":
                response = table.update_item(
                    Key={
                         'partitionKey': 'AGGREGATES',
                          'metadata': 'currentFemales'
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )


        #Aggregation #4: update total Male count
            if record['dynamodb']['NewImage']['gender']['S'] == "Male":
                response = table.update_item(
                    Key={
                        'partitionKey': 'AGGREGATES',
                        'metadata': 'currentMales'
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )

        #Aggregation #5: update total Redundant count
            if record['dynamodb']['NewImage']['isRedundant']['S'] == "True":
                response = table.update_item(
                    Key={
                        'partitionKey': 'AGGREGATES',
                        'metadata': 'currentRedundant'
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )

            if record['dynamodb']['NewImage']['isRedundant']['S'] == "False":
                response = table.update_item(
                    Key={
                        'partitionKey': 'AGGREGATES',
                        'metadata': 'currentUnique'
                        },
                    ReturnValues='UPDATED_NEW',
                    UpdateExpression='ADD aggregateValue :d',
                    ExpressionAttributeValues={':d': 1}
                    )
