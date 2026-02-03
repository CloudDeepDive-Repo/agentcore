# Lab 1: Building Your First Agent - Runtime & Inline Tools

Learn how to build an AI agent with inline tools and deploy it using AgentCore Runtime in under 1 minute!

## 🎯 What You'll Build

A network troubleshooting agent that diagnoses EC2 connectivity issues by calling AWS APIs directly from inline Python functions.

## 📋 Prerequisites

**On your local machine:**
- Python 3.10 or newer 
- AWS account with credentials configured
- AWS CLI configured

## 🚀 Quick Start

### Step 1: Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install AgentCore CLI
pip3 install bedrock-agentcore-starter-toolkit

# Verify installation
agentcore --version
```

### Step 2: Start Simple (No Tools)

```bash
cd 01-simple-agent

# Check for old config and delete if exists (this file is created when you configure AgentCore in next command. First time deployment you won't see it, but run the commands to be on the safer side)
rm -f .bedrock_agentcore.yaml

# Configure the agent
agentcore configure --entrypoint simple_agent.py

# Deploy
agentcore deploy --agent simple_agent

# Test with general question
agentcore invoke --agent simple_agent '{"prompt": "What is Amazon VPC?"}'
```

**Result:** Agent answers general questions but can't access AWS APIs.

### Step 3: Add Tools for AWS Access

```bash
cd ../02-agent-with-tools

# Delete old config
rm -f .bedrock_agentcore.yaml

# Configure the agent
agentcore configure --entrypoint network_troubleshooter.py

# Deploy
agentcore deploy --agent network_troubleshooter
```

### Step 4: Deploy Test Infrastructure

Deploy the test VPC with intentional network issues:

```bash
# Navigate to infrastructure folder
cd ../../infrastructure

# Deploy CloudFormation stack
aws cloudformation create-stack \
  --stack-name network-troubleshooting-labs \
  --template-body file://network-troubleshooting-labs.yaml \
  --capabilities CAPABILITY_NAMED_IAM

# Wait for stack to complete (takes ~2 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name network-troubleshooting-labs

# Get the Lab 1 instance ID
aws cloudformation describe-stacks \
  --stack-name network-troubleshooting-labs \
  --query 'Stacks[0].Outputs[?OutputKey==`Lab1InstanceId`].OutputValue' \
  --output text
```

### Step 5: Test and Hit Permission Error

```bash
# Navigate back to agent folder
cd ../Lab-1-runtime-inline-tools/02-agent-with-tools

# Test the agent (replace with your instance ID)
agentcore invoke --agent network_troubleshooter '{"prompt": "My EC2 instance i-XXXXX cannot connect to the internet"}'
```

**Expected:** Permission error! This is normal.

### Step 6: Fix Permissions

Find your execution role:

```bash
# Get role name from config
cat .bedrock_agentcore.yaml | grep execution_role
```

**Option 1: AWS Console**
1. Go to [IAM Console → Roles](https://console.aws.amazon.com/iam/home#/roles)
2. Search for your role (starts with `AmazonBedrockAgentCoreSDKRuntime`)
3. Click "Add permissions" → "Attach policies"
4. Add these policies:
   - `AmazonEC2ReadOnlyAccess`
   - `AmazonVPCReadOnlyAccess`
5. Click "Attach policies"

**Option 2: AWS CLI**
```bash
# Replace with your actual role name
ROLE_NAME="AmazonBedrockAgentCoreSDKRuntime-us-east-1-xxxxx"

aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess

aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonVPCReadOnlyAccess
```

### Step 7: Test Working Agent

```bash
# Test again (replace with your instance ID from Step 4)
agentcore invoke --agent network_troubleshooter '{"prompt": "My EC2 instance i-XXXXX cannot connect to the internet"}'
```

**Success!** Agent will:
1. Get EC2 instance details
2. Check Internet Gateway
3. Analyze route table
4. Diagnose the issue
5. Provide step-by-step fix

## 📁 Directory Structure

```
Lab-1-runtime-inline-tools/
├── 01-simple-agent/
│   ├── simple_agent.py          # Basic agent (no tools)
│   └── requirements.txt         # Python dependencies
│
├── 02-agent-with-tools/
│   ├── network_troubleshooter.py  # Agent with inline tools
│   └── requirements.txt           # Python dependencies
│
└── README.md                    # This file

infrastructure/                   # At repository root
└── network-troubleshooting-labs.yaml  # Test VPC with issues
```

## 🔍 Understanding the Code

### Simple Agent (No Tools)
- Just a model and system prompt
- Can answer questions but can't access AWS
- Foundation for adding tools

### Agent with Tools
- Tools are Python functions decorated with `@tool`
- Tools passed directly to Agent: `tools=[func1, func2, func3]`
- Agent autonomously decides which tools to call
- System prompt guides the troubleshooting workflow

### Key Concepts

**Inline Tools:**
```python
@tool
def get_ec2_details(instance_id: str) -> dict:
    """Get EC2 instance details including VPC, subnet, and security groups"""
    response = ec2.describe_instances(InstanceIds=[instance_id])
    # ... process and return data
```

**Agent Creation:**
```python
agent = Agent(
    model=model,
    tools=[get_ec2_details, check_internet_gateway, check_route_table],
    system_prompt=system_prompt
)
```

**AgentCore Runtime Wrapper:**
```python
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    response = agent(user_message)
    return {"response": str(response)}
```

## 🎓 What You Learned

1. ✅ Create a simple agent with just a model
2. ✅ Add inline tools as Python functions
3. ✅ Deploy with AgentCore Runtime (< 1 minute)
4. ✅ Handle IAM permissions (standard practice)
5. ✅ Build a working troubleshooting agent

## ⚠️ Limitations of Inline Tools

- Tools are embedded in agent code
- Hard to reuse across multiple agents
- No separation of concerns
- Difficult to test independently

**Solution:** Lab 2 shows how to move tools to AgentCore Gateway!

## 🧹 Cleanup

```bash
# Delete the agent
agentcore delete --agent network_troubleshooter

# Delete the simple agent
agentcore delete --agent simple_agent

# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name network-troubleshooting-labs
```

## 🐛 Troubleshooting

**Issue:** `agentcore: command not found`
- Make sure virtual environment is activated
- Reinstall: `pip3 install bedrock-agentcore-starter-toolkit`

**Issue:** Permission denied errors
- Make sure you added EC2 and VPC read policies to the execution role
- Wait a few seconds after adding policies for them to take effect

**Issue:** Model access denied
- Enable Claude 3.5 Sonnet in Bedrock console
- Go to Bedrock → Model access → Request access

## 📚 Next Steps

Ready to level up? Check out **Lab 2** to learn how to move tools to AgentCore Gateway for better reusability and production-ready architecture!

---

**Questions?** Open an issue in the GitHub repository!
