import os
import json
import logging

from todos import decimalencoder
import boto3
translate = boto3.client(service_name='translate')
comprehend = boto3.client(service_name='comprehend')
dynamodb = boto3.resource('dynamodb')

logging.info("Probando Lambda get new deploy")

def getByLang(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    textToTranslate = "Prueba traduccion going to the jungle"
    #languages = json.dumps(comprehend.detect_dominant_language(Text = textToTranslate), sort_keys=True, indent=4)
    languages_2 = comprehend.detect_dominant_language(Text = textToTranslate)
    lang_code = languages_2[0]['LanguageCode']
    
    responseTr = translate.translate_text(Text=textToTranslate, SourceLanguageCode=lang_code,
        TargetLanguageCode=event['pathParameters']['language'])
    jsonBody = {'text': str(responseTr)}

    # create a response
    response = {
        "statusCode": 200,
        #"body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
        "body": languages_2
    }
    logging.warning('This will get logged to a file')
    return response
