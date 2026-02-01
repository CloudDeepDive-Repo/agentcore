"""
Simple Agent - No Tools
This is the starting point showing a basic agent without any tools.
"""

from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Configuration
AWS_REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"  # Cross-region inference profile

# Initialize model
model = BedrockModel(
    model_id=MODEL_ID,
    region=AWS_REGION
)

# System prompt - tells the agent its role
system_prompt = """You are a helpful AWS assistant. 
Answer questions about AWS services, best practices, and general cloud computing topics.
Be conversational and friendly."""

# Create agent without tools
agent = Agent(
    model=model,
    system_prompt=system_prompt
)

# Wrap with AgentCore Runtime
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Main entrypoint for the agent"""
    user_message = payload.get("prompt", "")
    
    if not user_message:
        return {"error": "No prompt provided"}
    
    # Invoke agent
    response = agent(user_message)
    
    # Return response
    return {"response": str(response)}

if __name__ == "__main__":
    app.run()
