import json
import boto3

ecs_client = boto3.client('ecs')

def lambda_handler(event, context):
    # Extract S3 event details
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    print(f"CSV uploaded: {file_key} in bucket {bucket_name}")

    # Trigger ECS Task to run your FAISS processing container
    response = ecs_client.run_task(
        cluster='shoptalk-cluster', 
        launchType='FARGATE',
        taskDefinition='imageembed',  # Matches the "family" in your ECS Task Definition
        overrides={
            'containerOverrides': [
                {
                    'name': 'imageembed',  # Matches the container name in your Task Definition
                    'environment': [
                        {'name': 'S3_BUCKET', 'value': bucket_name},
                        {'name': 'S3_KEY', 'value': file_key}
                    ]
                }
            ]
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-00fa5599192147274','subnet-09f7d665c96b037d6', 'subnet-0c1a5634f2805761f','subnet-0260d6d792a57ff50','subnet-0e4f8f3832b581506','subnet-0d1adc72a31a46653'],  # Replace with your subnet ID
                'securityGroups': ['sg-046a49fea24181989','sg-03b932c7f80a4c374'],  # Replace with your security group
                'assignPublicIp': 'ENABLED'
            }
        }
    )

    print("ECS Task Triggered:", response)
    return response
