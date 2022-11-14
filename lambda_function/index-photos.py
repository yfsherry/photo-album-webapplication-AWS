
import json
import requests
from requests_aws4auth import AWS4Auth 
import boto3
import time
opensearch_host = "https://search-photos-3tbvybzjz4w3ikfd7qjxfujdyq.us-east-1.es.amazonaws.com"
index = 'photos'
url = opensearch_host + '/' + index + '/photo/'
print(url)

def detect_labels(photo, bucket):
    client = boto3.client("rekognition", "us-east-1")
    s3client = boto3.client("s3", "us-east-1")
    label_res = []
    meta = s3client.head_object(Bucket = bucket, Key = photo)
    
    if meta["Metadata"]:
        metainfo = meta["Metadata"]["customlabels"]
        metaList = metainfo.split(",")
        print(metaList)
        for ele in metaList:
            label_res.append(ele)
    print(label_res)
    resp = client.detect_labels(Image = {'S3Object': {'Bucket': bucket, 'Name': photo}}, MaxLabels = 10)
    for ele in resp["Labels"]:
        label_res.append(ele["Name"])
    print(label_res)
    return label_res
    

def lambda_handler(event, context):
    s3 = event["Records"][0]["s3"]
    photo = s3["object"]["key"]
    print(event)
    bucket = s3["bucket"]["name"]
    labels = detect_labels(photo, bucket)
    query = { "objectKey": photo, "bucket": bucket, "createdTimetamp": time.time(), "labels": labels}

    headers = { "Content-Type": "application/json" }
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    # r = requests.put(url, auth=awsauth, headers=headers, data=json.dumps(query))
    r = requests.post(url, auth=awsauth, data=json.dumps(query), headers=headers)
    print(r.text)
    print("im here")
  
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Headers": 'x-amz-meta-customLabels',
            "Access-Control-Allow-Methods": 'OPTIONS, PUT, GET'
        },
        "isBase64Encoded": False
    }
