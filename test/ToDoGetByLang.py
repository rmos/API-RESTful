import boto3
from botocore.exceptions import ClientError


def get_todo(id, dynamodb=None):
    
    responseLang = {"Languages": [{"LanguageCode": "en", "Score": 0.5243282318115234}, 
						{"LanguageCode": "es", "Score": 0.45777541399002075}]}
    sample_text = "El nuevo programa se emite mañana"
						
    try:
        responseLang['Languages'][0]['LanguageCode'] = "es"
        print(responseLang)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return responseLang


def main():
    todo = get_todo("123e4567-e89b-12d3-a456-426614174000")
    if todo:
        return todo


if __name__ == '__main__':
    main()
