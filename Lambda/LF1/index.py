import json
import boto3
import uuid
import requests
import json
from datetime import datetime
from pprint import pprint

def lambda_handler(event, context):
    # Testing pipeline Final Test 2 and more
    print("event: ", event)
    print("event: ", event)
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    image_name = event['Records'][0]['s3']['object']['key']
    print("bucket_name: ", bucket_name)
    
    client_rec =boto3.client('rekognition', region_name = 'us-east-1')
    response_res = client_rec.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':image_name}},
        MaxLabels=10)
    print("response_res: ", response_res)
    print("Recognition Done")
    
    client_s3 = boto3.client('s3')
    response_s3 = client_s3.head_object(Bucket=bucket_name, Key=image_name)
    print("response_s3: ", response_s3)
    
    meta_labels = []
    try:
        meta_labels = [l.strip() for l in response_s3['Metadata']['customlabels'].strip().split(',')]
    except KeyError:
        meta_labels = []

    labels = [label['Name'] for label in response_res['Labels']] + meta_labels
    
    a1 = {}
    a1["objectKey"] = image_name
    a1["bucket"] = bucket_name
    a1["createdTimestamp"] = str(datetime.now())
    a1["labels"] = labels
    print("a1: ", a1)
    
    host = 'https://search-ht2191-cf-search-photo-jggmm2xunwwj5zld46m6wunjcy.us-east-1.es.amazonaws.com'
    _index = 'ht2191-cf-search-photo'
    _type = 'Photo'
    _id = uuid.uuid1().hex
    
    path = '/{}/{}/{}/'.format(_index, _type, _id)
    master_user = "ht2191"
    master_password = "Xyz123@abc"
    
    url = host + path
    r = requests.post(url, auth=(master_user, master_password), json=a1)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
