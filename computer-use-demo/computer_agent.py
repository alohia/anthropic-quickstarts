import asyncio
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import AnthropicBedrock
from computer_use_demo.loop import sampling_loop, APIProvider
from computer_use_demo.tools import ToolVersion
import uvicorn

app = FastAPI()

class Instructions(BaseModel):
    text: str

async def run_computer_instructions(instructions: str) -> str:
    """
    Run computer instructions using Claude via Bedrock and return the final result.
    
    Args:
        instructions: The instructions to execute
        
    Returns:
        The final result/response from Claude after executing the instructions
    """
    # Initialize the Bedrock client
    client = AnthropicBedrock()
    
    # Prepare the initial message
    messages = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": instructions
        }]
    }]
    
    # Callbacks to collect results
    results = []
    
    def output_callback(content):
        if content["type"] == "text":
            results.append(content["text"])
    
    def tool_output_callback(result, tool_id):
        # You can optionally log or process tool outputs here
        pass
    
    def api_response_callback(request, response, error):
        # You can optionally log API responses here
        pass
    
    # Run the sampling loop
    final_messages = await sampling_loop(
        model="anthropic.claude-3-sonnet-20240229-v1:0",  # Bedrock model ID
        provider=APIProvider.BEDROCK,
        system_prompt_suffix="",
        messages=messages,
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        api_key="",  # Not needed for Bedrock
        tool_version=ToolVersion.V1,
        max_tokens=4096
    )
    
    # Return the collected results
    return "\n".join(results)

@app.post("/execute")
async def execute_instructions(instructions: Instructions):
    try:
        result = await run_computer_instructions(instructions.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 