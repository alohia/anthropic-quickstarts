import requests
import json

class ComputerAgentClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def execute_instructions(self, instructions: str) -> str:
        """
        Send instructions to the computer agent and get the results.
        
        Args:
            instructions: The instructions to execute
            
        Returns:
            The result from the computer agent
        """
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={"text": instructions}
            )
            response.raise_for_status()
            return response.json()["result"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to execute instructions: {str(e)}")

# Example usage
if __name__ == "__main__":
    client = ComputerAgentClient()
    result = client.execute_instructions(
        "Please open Firefox and search for 'Python programming'. "
        "Take a screenshot of the results and tell me what you see."
    )
    print(result) 