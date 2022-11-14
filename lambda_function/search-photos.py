import json
import boto3
import requests
from requests_aws4auth import AWS4Auth 
opensearch_host = "https://search-photos-3tbvybzjz4w3ikfd7qjxfujdyq.us-east-1.es.amazonaws.com/photos/_search?q="
bucketname = "photo-storage-bucket"
def searchwithKeyWords(keywords):
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    headers = {"Content-Type": "application/json"}
    query = []
    res = []
   
    for ele in keywords:
        keywordurl = opensearch_host + ele
        # print(keywordurl)
        query.append(requests.get(keywordurl,  auth=awsauth).json())
     
        
    for ele in query:
        if "hits" in ele:
            for v in ele["hits"]["hits"]:
                objectkey = v["_source"]["objectKey"]
                if objectkey not in res:
                    bucketname = "photo-storage-bucket"
                    objecturl = "https://" + bucketname + ".s3.amazonaws.com/" + objectkey
                    res.append(objecturl)
    print(res)
    return res
     

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('lexv2-runtime')
 
    print(event)
    query_text = event["queryStringParameters"]["q"]
    # query_text = "show me photos with cat"
    lexkeywords = []
    response = client.recognize_text(
                botId='Y8M9RITRWI', # MODIFY HERE
                botAliasId='TSTALIASID', # MODIFY HERE
                localeId='en_US',
                sessionId='testuser',
                text=query_text)
    print(response)
    
    if response["sessionState"]["intent"]["slots"] != None:
 
        lexkeywords.append(response["sessionState"]["intent"]["slots"]["keywordone"]["value"]["interpretedValue"])
        if (response["sessionState"]["intent"]["slots"]["keywordtwo"]!=None):
            lexkeywords.append(response["sessionState"]["intent"]["slots"]["keywordtwo"]["value"]["interpretedValue"])
        
        searchphotos = searchwithKeyWords(lexkeywords)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": json.dumps(searchphotos),
            "isBase64Encoded": False
        }
        
    else:
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": [],
            "isBase64Encoded": False
        }
    
   

    
