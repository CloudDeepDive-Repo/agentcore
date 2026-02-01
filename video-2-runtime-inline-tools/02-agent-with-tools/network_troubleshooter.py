"""
AWS Network Troubleshooting Agent - Video 2
Using AgentCore Runtime with Inline Tools

This agent helps diagnose EC2 connectivity issues by:
1. Getting EC2 instance details
2. Checking Internet Gateway configuration
3. Analyzing route table configuration
"""

import boto3
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Configuration
AWS_REGION = "us-east-1"
# Use cross-region inference profile for on-demand throughput
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Initialize Bedrock model
model = BedrockModel(model_id=MODEL_ID, region_name=AWS_REGION)

# Initialize AWS clients with region
ec2 = boto3.client('ec2', region_name=AWS_REGION)

# ============================================================================
# INLINE TOOLS - Python functions the agent can call
# ============================================================================

@tool
def get_ec2_details(instance_id: str) -> dict:
    """Get EC2 instance details including VPC, subnet, and security groups.
    
    Args:
        instance_id: The EC2 instance ID (e.g., i-abc123)
    
    Returns:
        Dictionary with instance details
    """
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    
    return {
        'instance_id': instance_id,
        'vpc_id': instance['VpcId'],
        'subnet_id': instance['SubnetId'],
        'security_groups': [sg['GroupId'] for sg in instance['SecurityGroups']],
        'public_ip': instance.get('PublicIpAddress'),
        'private_ip': instance['PrivateIpAddress'],
        'state': instance['State']['Name']
    }

@tool
def check_internet_gateway(vpc_id: str) -> dict:
    """Check if VPC has an Internet Gateway attached.
    
    Args:
        vpc_id: The VPC ID (e.g., vpc-abc123)
    
    Returns:
        Dictionary with IGW status and details
    """
    response = ec2.describe_internet_gateways(
        Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
    )
    
    if response['InternetGateways']:
        igw = response['InternetGateways'][0]
        return {
            'has_igw': True,
            'igw_id': igw['InternetGatewayId'],
            'state': igw['Attachments'][0]['State']
        }
    else:
        return {'has_igw': False}

@tool
def check_route_table(subnet_id: str) -> dict:
    """Check route table configuration for a subnet.
    
    Args:
        subnet_id: The subnet ID (e.g., subnet-abc123)
    
    Returns:
        Dictionary with route table details and routes
    """
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
    
    return {
        'route_table_id': route_table['RouteTableId'],
        'has_igw_route': has_igw_route,
        'routes': [
            {
                'destination': route.get('DestinationCidrBlock', 'N/A'),
                'target': route.get('GatewayId') or route.get('NatGatewayId') or 'local'
            }
            for route in routes
        ]
    }

# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

# System prompt - tells the agent how to troubleshoot
system_prompt = """You are an AWS network troubleshooting expert.

When a user reports an EC2 connectivity issue:
1. Get EC2 instance details using get_ec2_details
2. Check if VPC has Internet Gateway using check_internet_gateway
3. Check route table configuration using check_route_table

After gathering information, provide:
- Clear diagnosis of the problem
- Root cause explanation
- Step-by-step remediation guide

Be conversational and helpful."""

# Create agent with inline tools
agent = Agent(
    model=model,
    tools=[get_ec2_details, check_internet_gateway, check_route_table],
    system_prompt=system_prompt
)

# ============================================================================
# AGENTCORE RUNTIME WRAPPER
# ============================================================================

# Wrap with AgentCore Runtime
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Main entrypoint for the agent.
    
    Args:
        payload: Dictionary with 'prompt' key containing user message
    
    Returns:
        Dictionary with 'response' key containing agent response
    """
    user_message = payload.get("prompt", "")
    
    if not user_message:
        return {"error": "No prompt provided"}
    
    # Invoke agent - it will automatically call tools as needed
    response = agent(user_message)
    
    # Return response
    return {"response": str(response)}

if __name__ == "__main__":
    app.run()
