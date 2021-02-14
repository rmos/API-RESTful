import os
import json
import logging

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

logging.info("Probando Lambda get new deploy")

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    #b = json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
    
    # JSON data: 
    x =  '{ "organization":"GeeksForGeeks", "city":"Noida", "country":"India"}'
    # python object to be appended 
    y = {"pin":110096} 
      
    # parsing JSON string: 
    z = json.loads(json.dumps(result['Item']))
       
    # appending the data 
    z.update(y)
    # create a response
    # cambio para renombrado de stage y ramas
    response = {
        "statusCode": 200,
        "body": json.dumps(json.dumps(z), cls=decimalencoder.DecimalEncoder)
    }
    logging.warning('This will get logged to a file')
    return response
