# Amazon Bedrock AgentCore - Video Series Code

This repository contains all the code examples from the Amazon Bedrock AgentCore video series. Follow along with the videos and use this code to build your own AI agents!

## 📺 Video Series

### Video 1: Introduction to AgentCore
- Overview of AgentCore architecture
- Understanding Runtime and Gateway
- When to use each approach

### Video 2: Building Your First Agent - Runtime & Inline Tools
- Create a simple agent with no tools
- Add inline tools for AWS API access
- Deploy with AgentCore Runtime
- Handle IAM permissions
- Build a network troubleshooting agent

### Video 3: Using AgentCore Gateway - Moving Tools Out
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

# Choose your video and follow the README in that directory
cd video-2-runtime-inline-tools
# OR
cd video-3-gateway-external-tools
```

## 📁 Repository Structure

```
agentcore/
├── video-2-runtime-inline-tools/     # Video 2: Runtime & Inline Tools
│   ├── 01-simple-agent/              # Step 1: Basic agent (no tools)
│   ├── 02-agent-with-tools/          # Step 2: Agent with inline tools
│   ├── infrastructure/               # CloudFormation for test environment
│   └── README.md                     # Detailed instructions
│
├── video-3-gateway-external-tools/   # Video 3: Gateway & External Tools
│   ├── lambda-tools/                 # Lambda functions (tools)
│   ├── agent/                        # Agent code using Gateway
│   └── README.md                     # Detailed instructions
│
└── README.md                         # This file
```

## 🎯 What You'll Build

### Video 2: Network Troubleshooting Agent
An AI agent that diagnoses EC2 connectivity issues by:
- Getting EC2 instance details
- Checking Internet Gateway configuration
- Analyzing route table settings
- Providing step-by-step remediation

**Deployment time:** < 1 minute with AgentCore Runtime

### Video 3: Reusable Tools with Gateway
The same agent, but with tools moved to AgentCore Gateway:
- Tools as Lambda functions
- Centralized tool management
- Reusable across multiple agents
- Production-ready architecture

## 📖 Learning Path

1. **Start with Video 2** - Learn the basics with inline tools
2. **Progress to Video 3** - Level up with Gateway architecture
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

- Watch the video series for detailed explanations
- Check the README in each video directory
- Open an issue in this repository

---

**Happy Building! 🚀**
