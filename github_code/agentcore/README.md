# Amazon Bedrock AgentCore - Hands-On Labs

This repository contains hands-on labs for learning Amazon Bedrock AgentCore. Build AI agents step-by-step, from basic inline tools to production-ready Gateway architecture!

## � Labs Overview

### Lab 1: Building Your First Agent - Runtime & Inline Tools
- Create a simple agent with no tools
- Add inline tools for AWS API access
- Deploy with AgentCore Runtime
- Handle IAM permissions
- Build a network troubleshooting agent

### Lab 2: Using AgentCore Gateway - Moving Tools Out
- Convert inline tools to Lambda functions
- Create AgentCore Gateway
- Connect agent to Gateway
- Reuse tools across multiple agents

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or newer
- AWS account with credentials configured
- Model access in Amazon Bedrock (Claude 3.5 Sonnet)
- AWS CLI configured

### Installation

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/agentcore.git
cd agentcore

# Choose your lab and follow the README in that directory
cd Lab-1-runtime-inline-tools
# OR
cd Lab-2-gateway-external-tools
```

## 📁 Repository Structure

```
agentcore/
├── Lab-1-runtime-inline-tools/       # Lab 1: Runtime & Inline Tools
│   ├── 01-simple-agent/              # Step 1: Basic agent (no tools)
│   ├── 02-agent-with-tools/          # Step 2: Agent with inline tools
│   └── README.md                     # Detailed instructions
│
├── Lab-2-gateway-external-tools/     # Lab 2: Gateway & External Tools
│   ├── lambda_*.py                   # Lambda functions (4 tools)
│   ├── network_troubleshooter.py     # Agent code using Gateway
│   ├── streamable_http_sigv4.py      # SigV4 authentication helper
│   ├── gateway_inline_schemas.json   # MCP tool schemas
│   └── README.md                     # Detailed instructions
│
├── infrastructure/                   # CloudFormation for test environment
│   └── network-troubleshooting-labs.yaml
│
└── README.md                         # This file
```

## 🎯 What You'll Build

### Lab 1: Network Troubleshooting Agent with Inline Tools
An AI agent that diagnoses EC2 connectivity issues using inline tools:
- ✅ Getting EC2 instance details
- ✅ Checking Internet Gateway configuration
- ✅ Analyzing route table settings
- ✅ Checking security group rules
- ✅ Providing step-by-step remediation

**Architecture:** Agent → Inline Tools → AWS APIs  
**Deployment time:** < 1 minute with AgentCore Runtime

### Lab 2: Network Troubleshooting Agent with Gateway
The same agent, but with tools moved to AgentCore Gateway:
- ✅ Tools as Lambda functions
- ✅ Centralized tool management via Gateway
- ✅ Reusable across multiple agents
- ✅ Production-ready architecture
- ✅ IAM-based authentication

**Architecture:** Agent → Gateway → Lambda Functions → AWS APIs  
**Deployment time:** ~5 minutes (Lambda + Gateway setup)

## 📖 Learning Path

### Lab 1: Runtime & Inline Tools
**What you'll learn:**
- Create a basic agent with no tools
- Add inline tools for AWS API access
- Deploy with AgentCore Runtime
- Handle IAM permissions
- Build a complete network troubleshooting agent

**Time:** 30-45 minutes  
**Difficulty:** Beginner

### Lab 2: Gateway & External Tools
**What you'll learn:**
- Convert inline tools to Lambda functions
- Create and configure AgentCore Gateway
- Add Lambda functions as Gateway targets
- Enable IAM authentication on Gateway
- Connect agent to Gateway using SigV4
- Deploy production-ready architecture

**Time:** 45-60 minutes  
**Difficulty:** Intermediate

### Recommended Path
1. **Start with Lab 1** - Learn the basics with inline tools
2. **Progress to Lab 2** - Level up with Gateway architecture
3. **Experiment** - Modify the code and build your own agents!

## 🛠️ Technologies Used

- **Amazon Bedrock** - LLM inference (Claude 3.5 Sonnet)
- **AgentCore Runtime** - Serverless agent execution
- **AgentCore Gateway** - Centralized tool management
- **Strands Agent SDK** - Agent framework
- **AWS Lambda** - Tool execution (Video 3)
- **AWS CloudFormation** - Infrastructure as Code

## 📚 Additional Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Strands Agent SDK](https://github.com/awslabs/strands)

## 🤝 Contributing

Found an issue or want to improve the code? Feel free to open an issue or submit a pull request!

## 📝 License

This code is provided as-is for educational purposes. See LICENSE file for details.

## 💬 Questions?

- Check the README in each lab directory for detailed instructions
- Open an issue in this repository for help

---

**Happy Building! 🚀**
