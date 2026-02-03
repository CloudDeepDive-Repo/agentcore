"""
Lambda Function: check-route-table
Check route table for a subnet and determine if it has routes to IGW or NAT Gateway
"""

import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Check route table configuration for a subnet
    
    Args:
        event: {
            "subnet_id": "subnet-xxxxx"
        }
    
    Returns:
        Route table details and whether it has IGW/NAT routes
    """
    try:
        subnet_id = event['subnet_id']
        
        # Get route table for subnet
        response = ec2.describe_route_tables(
            Filters=[{'Name': 'association.subnet-id', 'Values': [subnet_id]}]
        )
        
        if not response['RouteTables']:
            # Check main route table
            response = ec2.describe_route_tables(
                Filters=[{'Name': 'association.main', 'Values': ['true']}]
            )
        
        route_table = response['RouteTables'][0]
        routes = route_table['Routes']
        
        # Check for default route to IGW
        has_igw_route = any(
            route.get('DestinationCidrBlock') == '0.0.0.0/0' and 
            'GatewayId' in route and 
            route['GatewayId'].startswith('igw-')
            for route in routes
        )
        
        # Check for default route to NAT Gateway
        has_nat_route = any(
            route.get('DestinationCidrBlock') == '0.0.0.0/0' and 
            'NatGatewayId' in route
            for route in routes
        )
        
        result = {
            'route_table_id': route_table['RouteTableId'],
            'has_igw_route': has_igw_route,
            'has_nat_route': has_nat_route,
            'routes': [
                {
                    'destination': route.get('DestinationCidrBlock', 'N/A'),
                    'target': route.get('GatewayId') or route.get('NatGatewayId') or 'local'
                }
                for route in routes
            ]
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
