"""
Lambda Function: check-internet-gateway
Check if a VPC has an Internet Gateway attached
"""

import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Check if VPC has Internet Gateway attached
    
    Args:
        event: {
            "vpc_id": "vpc-0f80cb9c14c6a5ca7"
        }
    
    Returns:
        IGW status and ID if present
    """
    try:
        vpc_id = event['vpc_id']
        
        response = ec2.describe_internet_gateways(
            Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
        )
        
        if response['InternetGateways']:
            igw = response['InternetGateways'][0]
            result = {
                'has_igw': True,
                'igw_id': igw['InternetGatewayId'],
                'state': igw['Attachments'][0]['State']
            }
        else:
            result = {'has_igw': False}
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
