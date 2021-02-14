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
    
    textToTranslate = result['Item']['text']
    #languages = json.dumps(comprehend.detect_dominant_language(Text = textToTranslate), sort_keys=True, indent=4)
    languages = comprehend.detect_dominant_language(Text = textToTranslate)
    lang_code = languages['Languages'][0]['LanguageCode']
    responseTr = translate.translate_text(Text=textToTranslate, SourceLanguageCode=lang_code,
        TargetLanguageCode=event['pathParameters']['language'])
    result['Item']['text'] = str(responseTr['TranslatedText'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
    }
    logging.warning('This will get logged to a file')
    return response
