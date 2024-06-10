import boto3
import os
import sys
import time
from datetime import datetime, timezone
from time import gmtime, strftime

def shut_rds_development():
    region = os.environ['REGION']
    key = os.environ['KEY']
    value = os.environ['VALUE']
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()
    
    for i in response['DBInstances']:
        arn = i['DBInstanceArn']
        resp2 = client.list_tags_for_resource(ResourceName=arn)
        # Check if the RDS instance is part of the environment dev group.
        if len(resp2['TagList']) == 0:
            print('DB Instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))
        else:
            for tag in resp2['TagList']:
                # If the tags match, then stop the instances by validating the current status.
                if tag['Key'] == key and tag['Value'] == value:
                    if i['DBInstanceStatus'] == 'available':
                        client.stop_db_instance(DBInstanceIdentifier=i['DBInstanceIdentifier'])
                        print('Stopping DB instance {0}'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'stopped':
                        print('DB Instance {0} is already stopped'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'starting':
                        print('DB Instance {0} is in starting state. Please stop the cluster after starting is complete'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'stopping':
                        print('DB Instance {0} is already in stopping state.'.format(i['DBInstanceIdentifier']))
                elif tag['Key'] != key and tag['Value'] != value:
                    print('DB instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))
                elif len(tag['Key']) == 0 or len(tag['Value']) == 0:
                    print('DB Instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))

def lambda_handler(event, context):
    shut_rds_development()import boto3
import os
import sys
import time
from datetime import datetime, timezone
from time import gmtime, strftime

def shut_rds_development():
    region = os.environ['REGION']
    key = os.environ['KEY']
    value = os.environ['VALUE']
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()
    
    for i in response['DBInstances']:
        arn = i['DBInstanceArn']
        resp2 = client.list_tags_for_resource(ResourceName=arn)
        # Check if the RDS instance is part of the environment dev group.
        if len(resp2['TagList']) == 0:
            print('DB Instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))
        else:
            for tag in resp2['TagList']:
                # If the tags match, then stop the instances by validating the current status.
                if tag['Key'] == key and tag['Value'] == value:
                    if i['DBInstanceStatus'] == 'available':
                        client.stop_db_instance(DBInstanceIdentifier=i['DBInstanceIdentifier'])
                        print('Stopping DB instance {0}'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'stopped':
                        print('DB Instance {0} is already stopped'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'starting':
                        print('DB Instance {0} is in starting state. Please stop the cluster after starting is complete'.format(i['DBInstanceIdentifier']))
                    elif i['DBInstanceStatus'] == 'stopping':
                        print('DB Instance {0} is already in stopping state.'.format(i['DBInstanceIdentifier']))
                elif tag['Key'] != key and tag['Value'] != value:
                    print('DB instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))
                elif len(tag['Key']) == 0 or len(tag['Value']) == 0:
                    print('DB Instance {0} is not part of dev environment'.format(i['DBInstanceIdentifier']))

def lambda_handler(event, context):
    shut_rds_development()