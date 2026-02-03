"""
Lambda Function: check-security-group
Check security group ingress and egress rules for internet traffic
"""

import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Check security group rules to determine if outbound internet traffic is allowed
    
    Args:
        event: {
            "security_group_id": "sg-xxxxx"
        }
    
    Returns:
        Security group rules and whether outbound internet traffic is allowed
    """
    try:
        security_group_id = event['security_group_id']
        
        response = ec2.describe_security_groups(GroupIds=[security_group_id])
        security_group = response['SecurityGroups'][0]
        
        # Check egress rules for outbound internet access (0.0.0.0/0)
        egress_rules = security_group['IpPermissionsEgress']
        allows_outbound_internet = any(
            any(ip_range.get('CidrIp') == '0.0.0.0/0' for ip_range in rule.get('IpRanges', []))
            for rule in egress_rules
        )
        
        # Format ingress rules
        ingress_rules = [
            {
                'protocol': rule.get('IpProtocol', 'all'),
                'from_port': rule.get('FromPort', 'all'),
                'to_port': rule.get('ToPort', 'all'),
                'cidr_blocks': [ip_range.get('CidrIp') for ip_range in rule.get('IpRanges', [])]
            }
            for rule in security_group['IpPermissions']
        ]
        
        # Format egress rules
        egress_rules_formatted = [
            {
                'protocol': rule.get('IpProtocol', 'all'),
                'from_port': rule.get('FromPort', 'all'),
                'to_port': rule.get('ToPort', 'all'),
                'cidr_blocks': [ip_range.get('CidrIp') for ip_range in rule.get('IpRanges', [])]
            }
            for rule in egress_rules
        ]
        
        result = {
            'security_group_id': security_group_id,
            'security_group_name': security_group['GroupName'],
            'allows_outbound_internet': allows_outbound_internet,
            'ingress_rules': ingress_rules,
            'egress_rules': egress_rules_formatted
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
