import os
import io
import boto3
import json

# grab environment variables
endpoint_name = "sklearn-local-ep2022-05-02-00-35-41"
runtime_client = boto3.client('sagemaker-runtime')
content_type = "application/json"

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = json.dumps(data)
    print(payload)
    
    response = runtime_client.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=payload,
        ContentType=content_type,
        Accept='Accept')
    
    result = json.loads(response['Body'].read().decode())['Songs']
  
    return result