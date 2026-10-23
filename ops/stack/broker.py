"""Create isolated P04 local queue and event resources idempotently."""

import json

import boto3

settings = dict(endpoint_url='http://localstack:4566', region_name='us-east-1',
                aws_access_key_id='test', aws_secret_access_key='test')
sqs = boto3.client('sqs', **settings)
dlq = sqs.create_queue(QueueName='lab-p04-tasks-dlq')['QueueUrl']
arn = sqs.get_queue_attributes(QueueUrl=dlq, AttributeNames=['QueueArn'])['Attributes']['QueueArn']
sqs.create_queue(QueueName='lab-p04-tasks', Attributes={
    'RedrivePolicy': json.dumps({'deadLetterTargetArn':arn, 'maxReceiveCount':'3'}),
})
sns = boto3.client('sns', **settings)
for suffix in ('created', 'completed', 'failed'):
    sns.create_topic(Name='lab-task-'+suffix)
print('P04 queues, dead-letter queue and event topics ready; local emulation only.')
