"""
Lambda Function: get-ec2-details
Get EC2 instance details including VPC, subnet, security groups, and IP addresses
"""

import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Get EC2 instance details
    
    Args:
        event: {
            "instance_id": "i-064478c7beb840c75"
        }
    
    Returns:
        Instance details including VPC, subnet, security groups, IPs, and state
    """
    try:
        instance_id = event['instance_id']
        
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        result = {
            'instance_id': instance_id,
            'vpc_id': instance['VpcId'],
            'subnet_id': instance['SubnetId'],
            'security_groups': [sg['GroupId'] for sg in instance['SecurityGroups']],
            'public_ip': instance.get('PublicIpAddress'),
            'private_ip': instance['PrivateIpAddress'],
            'state': instance['State']['Name']
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
