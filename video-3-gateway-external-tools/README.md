# Video 3: Using AgentCore Gateway - Moving Tools Out

Learn how to move tools from inline functions to AgentCore Gateway for better reusability and production-ready architecture!

## 🎯 What You'll Build

The same network troubleshooting agent, but with tools moved to Lambda functions and managed by AgentCore Gateway.

## 📋 Prerequisites

- Completed Video 2
- Python 3.10 or newer
- AWS account with credentials configured
- Model access in Amazon Bedrock (Claude 3.5 Sonnet)
- AWS CLI configured

## 🚧 Coming Soon!

This section will be updated with:
- Lambda function code for each tool
- Gateway configuration
- Agent code using Gateway
- Step-by-step deployment instructions

## 🔄 Key Differences from Video 2

### Video 2: Inline Tools
```python
@tool
def get_ec2_details(instance_id: str) -> dict:
    # Tool code here
    pass

agent = Agent(
    model=model,
    tools=[get_ec2_details, ...]  # Tools in agent code
)
```

### Video 3: Gateway Tools
```python
# Tools are Lambda functions, not in agent code
# Agent connects to Gateway to use tools

agent = Agent(
    model=model,
    gateway_id="your-gateway-id"  # Tools from Gateway
)
```

## 📚 Benefits of Gateway

1. **Reusability** - One tool, many agents
2. **Separation** - Tools live separately from agent code
3. **Testing** - Test tools and agents independently
4. **Management** - Update tools in one place
5. **Lambda Integration** - Use existing Lambda functions

## 🎓 What You'll Learn

1. ✅ Convert inline tools to Lambda functions
2. ✅ Create AgentCore Gateway
3. ✅ Add Lambda tools to Gateway
4. ✅ Connect agent to Gateway
5. ✅ Reuse tools across multiple agents

---

**Stay tuned for the complete code and instructions!**
