# Lab 2: Using AgentCore Gateway - Moving Tools Out

Learn how to move tools from inline functions to AgentCore Gateway for better reusability and production-ready architecture!

## 🎯 What You'll Build

The same network troubleshooting agent, but with tools moved to Lambda functions and managed by AgentCore Gateway.

## 📋 Prerequisites

- Completed Lab 1
- Python 3.10 or newer
- AWS account with credentials configured
- Model access in Amazon Bedrock (Claude 3.5 Sonnet)
- AWS CLI configured
- IAM permissions to create Lambda functions and AgentCore Gateway

## 📁 Files in This Lab

- `lambda_get_ec2_details.py` - Lambda function to get EC2 instance details
- `lambda_check_internet_gateway.py` - Lambda function to check Internet Gateway
- `lambda_check_route_table.py` - Lambda function to check route tables
- `lambda_check_security_group.py` - Lambda function to check security groups
- `gateway_inline_schemas.json` - MCP tool schemas for Gateway targets
- `network_troubleshooter.py` - Agent code that connects to Gateway
- `streamable_http_sigv4.py` - SigV4 authentication helper for Gateway
- `requirements.txt` - Python dependencies

## 🚀 Step-by-Step Setup

### Step 1: Create Lambda Functions

Create 4 Lambda functions with the provided code:

```bash
# Create Lambda execution role first (if you don't have one)
aws iam create-role \
  --role-name AgentCoreLambdaRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policies for Lambda execution and EC2 read access
aws iam attach-role-policy \
  --role-name AgentCoreLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name AgentCoreLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess

aws iam attach-role-policy \
  --role-name AgentCoreLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonVPCReadOnlyAccess
```

Create deployment packages and deploy each Lambda:

```bash
# Create deployment packages
zip lambda_get_ec2_details.zip lambda_get_ec2_details.py
zip lambda_check_internet_gateway.zip lambda_check_internet_gateway.py
zip lambda_check_route_table.zip lambda_check_route_table.py
zip lambda_check_security_group.zip lambda_check_security_group.py

# Get your account ID and role ARN
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/AgentCoreLambdaRole"

# Deploy Lambda functions
aws lambda create-function \
  --function-name get-ec2-details \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_get_ec2_details.lambda_handler \
  --zip-file fileb://lambda_get_ec2_details.zip \
  --timeout 30

aws lambda create-function \
  --function-name check-internet-gateway \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_check_internet_gateway.lambda_handler \
  --zip-file fileb://lambda_check_internet_gateway.zip \
  --timeout 30

aws lambda create-function \
  --function-name check-route-table \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_check_route_table.lambda_handler \
  --zip-file fileb://lambda_check_route_table.zip \
  --timeout 30

aws lambda create-function \
  --function-name check-security-group \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_check_security_group.lambda_handler \
  --zip-file fileb://lambda_check_security_group.zip \
  --timeout 30
```

### Step 2: Create AgentCore Gateway

1. Go to **Amazon Bedrock Console** → **AgentCore** → **Gateways**
2. Click **Create Gateway**
3. Configure:
   - **Name**: `network-troubleshooter-gateway`
   - **Description**: Gateway for network troubleshooting tools
   - **Semantic search**: Enable (recommended)
   - **Authentication**: Enable **IAM authentication**
4. Click **Create Gateway**
5. Note the **Gateway ID** (you'll need this later)

### Step 3: Add Lambda Functions as Gateway Targets

For each Lambda function, add it as a Gateway target:

1. In your Gateway, click **Add target**
2. Select **Lambda function**
3. Choose the Lambda function (e.g., `get-ec2-details`)
4. Copy the corresponding inline schema from `gateway_inline_schemas.json`
5. Paste the schema in the **Inline schema** field
6. Click **Add target**

Repeat for all 4 Lambda functions:
- `get-ec2-details` → Use `get_ec2_details` schema
- `check-internet-gateway` → Use `check_internet_gateway` schema
- `check-route-table` → Use `check_route_table` schema
- `check-security-group` → Use `check_security_group` schema

### Step 4: Update IAM Role for AgentCore Runtime

Add the `BedrockAgentCoreFullAccess` managed policy to your AgentCore Runtime IAM role:

```bash
# Find your Runtime role name (replace with your actual role name)
RUNTIME_ROLE_NAME="your-agentcore-runtime-role"

# Attach BedrockAgentCoreFullAccess policy
aws iam attach-role-policy \
  --role-name $RUNTIME_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess
```

Or via AWS Console:
1. Go to **IAM** → **Roles**
2. Find your AgentCore Runtime role
3. Click **Add permissions** → **Attach policies**
4. Search for `BedrockAgentCoreFullAccess`
5. Select and attach the policy

### Step 5: Navigate to Lab-2 Directory

```bash
cd Lab-2-gateway-external-tools
```

### Step 6: Update Agent Code with Gateway ID

Edit `network_troubleshooter.py` and update the Gateway ID:

```python
GATEWAY_ID = "your-gateway-id"  # Replace with your actual Gateway ID from Step 2
```

### Step 7: Deploy the Agent

```bash
# Deploy the agent
agentcore deploy
```

### Step 8: Test the Agent

```bash
agentcore invoke '{"prompt": "My EC2 instance i-1234567890abcdef0 cannot connect to the internet"}'
```

## 🔄 Key Differences from Lab 1

### Lab 1: Inline Tools
```python
@tool
def get_ec2_details(instance_id: str) -> dict:
    # Tool code here
    pass

agent = Agent(
    model=model,
    tools=[get_ec2_details, ...]  # Tools embedded in agent code
)
```

### Lab 2: Gateway Tools
```python
# Tools are Lambda functions accessed through Gateway
mcp_client = MCPClient(lambda: streamablehttp_client_with_sigv4(
    url=gateway_endpoint,
    credentials=frozen_credentials,
    service="bedrock-agentcore",
    region=AWS_REGION
))

mcp_client.__enter__()
mcp_tools = mcp_client.list_tools_sync()  # Get tools from Gateway

agent = Agent(
    model=model,
    tools=mcp_tools  # Tools come from Gateway!
)
```

## 📚 Benefits of Gateway

1. **Reusability** - One Gateway, multiple agents can use the same tools
2. **Separation** - Tools live separately from agent code
3. **Testing** - Test tools and agents independently
4. **Management** - Update tools in one place, all agents benefit
5. **Lambda Integration** - Use existing Lambda functions as tools
6. **Centralized** - Manage all tools in one Gateway
7. **MCP Standard** - Works with any MCP-compatible framework

## 🎓 What You Learned

1. ✅ Convert inline tools to Lambda functions
2. ✅ Create AgentCore Gateway
3. ✅ Add Lambda tools to Gateway with inline schemas
4. ✅ Enable IAM authentication on Gateway
5. ✅ Connect agent to Gateway using SigV4
6. ✅ Deploy and test Gateway-based agent

## 🔍 Architecture

```
Agent → Gateway → Lambda Functions → AWS APIs
                  ├── get-ec2-details
                  ├── check-internet-gateway
                  ├── check-route-table
                  └── check-security-group
```

## 🧹 Cleanup

When you're done, clean up resources:

```bash
# Delete agent
agentcore delete

# Delete Lambda functions
aws lambda delete-function --function-name get-ec2-details
aws lambda delete-function --function-name check-internet-gateway
aws lambda delete-function --function-name check-route-table
aws lambda delete-function --function-name check-security-group

# Delete Gateway (via console or CLI)
aws bedrock-agentcore delete-gateway --gateway-id YOUR_GATEWAY_ID
```

## 🐛 Troubleshooting

### Issue: 401 Unauthorized Error

**Cause**: Gateway doesn't have IAM authentication enabled

**Solution**: 
1. Go to Bedrock Console → AgentCore → Gateways
2. Select your Gateway
3. Edit authentication settings
4. Enable **IAM authentication**

### Issue: Agent can't find tools

**Cause**: Gateway targets not configured correctly

**Solution**:
1. Verify all 4 Lambda functions are added as Gateway targets
2. Check that inline schemas are correctly pasted
3. Test Gateway with: `aws bedrock-agentcore invoke-gateway --gateway-id YOUR_GATEWAY_ID`

### Issue: Lambda permission errors

**Cause**: Lambda execution role missing permissions

**Solution**:
- Ensure Lambda role has `AmazonEC2ReadOnlyAccess` and `AmazonVPCReadOnlyAccess`

## 📖 Additional Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Strands Agents Documentation](https://strandsagents.com/)

## ➡️ Next Steps

Ready for more? Check out:
- **Lab 3**: Adding memory to your agent
- **Lab 4**: Multi-agent systems
- **Lab 5**: Production deployment patterns

---

**Questions or issues?** Open an issue on GitHub!
