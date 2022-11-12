import json
import logging
import boto3
import requests
from pprint import pprint

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # TODO implement
    logger.debug(f"[USER][EVENT] {event}")
    logger.debug(f"[USER][CONTEXT] {context}")
    
    host = 'https://search-search-cf-7ochiafkyifi227dwioysmofsm.us-east-1.es.amazonaws.com'
    master_user = "test"
    master_password = "Test@1234"
    
    text = event['queryStringParameters']['q']
    
    client_lex = boto3.client('lex-runtime')
    response = client_lex.post_text(
        botName='SearchPhotos',
        botAlias ='$LATEST',
        userId="Aniket",
        inputText=text
        )
    logger.debug(f"[USER][LEX] {response}")
        
    if response['dialogState'] == "ElicitIntent" or response['dialogState'] == 'ElicitSlot':
        return {
        "statusCode": 200,
        "body": json.dumps("Hello from lambda Error")
        
    }
    
    labels = [val for val in response['slots'].values() if val is not None]
    
    
    query_labels = ','.join(labels)
    url = host + '/_search?q=labels:{}&size=1000'.format(query_labels)
    r = requests.get(url, auth=(master_user, master_password)) 
    data = json.loads(r.text)

    logger.debug(f"[USER][OPENSEARCH] {data}")
    
    image_names = []
    for doc in data['hits']['hits']:
        image_names.append(f"https://{doc['_source']['bucket']}.s3.amazonaws.com/" + doc['_source']['objectKey'])
    
    # s3 = boto3.resource('s3')
    # obj = s3.Object(bucket, key)
    logger.debug(f"[USER][image_names] {image_names}")
    send_response = {
        'statusCode': 200,
        'body': {'imagePaths':image_names}
    }
    send_reponse_simple = {
        "statusCode": 200,
        "body": json.dumps(image_names),
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Allow" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Methods" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Headers" : "*"
        }
        
    }
    logger.debug(f"[USER][SEND] {send_reponse_simple}")
    

    
    return send_reponse_simple
