import json
import boto3
import requests
from pprint import pprint
import inflect
p = inflect.engine()

def lambda_handler(event, context):
    # Testing private repo
    print("event: ", event)

    host = 'https://search-ht2191-cf-search-photo-jggmm2xunwwj5zld46m6wunjcy.us-east-1.es.amazonaws.com'
    master_user = "ht2191"
    master_password = "Xyz123@abc"

    q = event['queryStringParameters']['q'].lower()
    print("q: ", q)

    if (not p.singular_noun(q)):
        text = q
    else:
        text = p.singular_noun(q)

    print("text: ", text)

    client_lex = boto3.client('lex-runtime')
    response = client_lex.post_text(
        botName='photo_search',
        botAlias ='$LATEST',
        userId='Himani',
        inputText=text  
        )
    print("Lex response: ", response)
    print("Lex client_lex: ", client_lex)

        
    if response['dialogState'] == "ElicitIntent" or response['dialogState'] == 'ElicitSlot':
        print("ElicitSlot")
        return {
        "statusCode": 200,
        "body": json.dumps([]),
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Allow" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Methods" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Headers" : "*"
        }
        
    }
    
    labels = [val for val in response['slots'].values() if val is not None]
    
    
    query_labels = ','.join(labels)
    print("query_labels: ", query_labels)

    url = host + '/_search?q=labels:{}&size=1000'.format(query_labels)
    r = requests.get(url, auth=(master_user, master_password)) 

    print("r: ", r)

    data = json.loads(r.text)
    
    print("data: ", data)
    
    image_names = []
    for doc in data['hits']['hits']:
        image_names.append(f"https://{doc['_source']['bucket']}.s3.amazonaws.com/" + doc['_source']['objectKey'])
    
    print("image_names: ", image_names)

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
    print("send_reponse_simple: ", send_reponse_simple)
    
    return send_reponse_simple
