"""Create local event topics for the P04 SNS publisher."""

import boto3

settings = dict(endpoint_url='http://localstack:4566', region_name='us-east-1',
                aws_access_key_id='test', aws_secret_access_key='test')
sns = boto3.client('sns', **settings)
for suffix in ('created', 'completed', 'failed'):
    sns.create_topic(Name='lab-task-'+suffix)
print('P04 event topics ready; local SNS emulation only.')
