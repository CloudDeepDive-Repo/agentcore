"""
AWS Network Troubleshooting Agent - Video 3
Using AgentCore Runtime with Gateway External Tools

This agent connects to AgentCore Gateway to use Lambda-based tools for:
1. Getting EC2 instance details
2. Checking Internet Gateway configuration
3. Analyzing route table configuration
4. Checking security group rules
"""

import os
import boto3
import logging
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from botocore.credentials import Credentials
from streamable_http_sigv4 import streamablehttp_client_with_sigv4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
GATEWAY_ID = "video-2-gateway-l3arzvgkjt"  # Replace with your Gateway ID
AWS_REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Gateway endpoint
gateway_endpoint = f"https://{GATEWAY_ID}.gateway.bedrock-agentcore.{AWS_REGION}.amazonaws.com/mcp"

# Initialize Bedrock model
model = BedrockModel(model_id=MODEL_ID, region_name=AWS_REGION)

# Get AWS credentials for SigV4 signing
session = boto3.Session()
credentials = session.get_credentials()
frozen_credentials = Credentials(
    access_key=credentials.access_key,
    secret_key=credentials.secret_key,
    token=credentials.token
)

mcp_client = MCPClient(lambda: streamablehttp_client_with_sigv4(
    url=gateway_endpoint,
    credentials=frozen_credentials,
    service="bedrock-agentcore",
    region=AWS_REGION
))

# Start MCP connection and get tools from Gateway
mcp_client.__enter__()
logger.info("📋 Listing tools from Gateway...")
mcp_tools = mcp_client.list_tools_sync()
logger.info(f"✅ Retrieved {len(mcp_tools)} tools from Gateway")


# System prompt - tells the agent how to troubleshoot
system_prompt = """You are an AWS network troubleshooting expert.

When a user reports an EC2 connectivity issue:
1. Get EC2 instance details using get_ec2_details
2. Check if VPC has Internet Gateway using check_internet_gateway
3. Check route table configuration using check_route_table
4. Check security group rules using check_security_group

After gathering information, provide:
- Clear diagnosis of the problem
- Root cause explanation
- Step-by-step remediation guide

Be conversational and helpful."""

# Create agent with Gateway tools
agent = Agent(
    model=model,
    tools=mcp_tools,  # Tools come from Gateway now! (4 tools)
    system_prompt=system_prompt
)

# Wrap with AgentCore Runtime
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """
    Main entrypoint for the agent
    
    Args:
        payload: Dictionary with 'prompt' key containing user message
    
    Returns:
        Dictionary with 'response' key containing agent response
    """
    user_message = payload.get("prompt", "")
    
    if not user_message:
        return {"error": "No prompt provided"}
    
    # Invoke agent - it will automatically call Gateway tools as needed
    response = agent(user_message)
    
    # Return response
    return {"response": str(response)}

if __name__ == "__main__":
    app.run()
