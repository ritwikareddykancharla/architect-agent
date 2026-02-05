import os
from google import genai
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class CodeFixRequest(BaseModel):
    code: str
    error_log: Optional[str] = None
    language: str = "python"

class CodeFixResponse(BaseModel):
    fixed_code: str
    explanation: str

class ArchitectAgent:
    def __init__(self):
        # The client will use GOOGLE_API_KEY from environment by default
        self.client = genai.Client()
        self.model_id = "gemini-2.0-flash"

    async def fix_code(self, request: CodeFixRequest) -> CodeFixResponse:
        prompt = f"""
        You are an expert software architect and developer.
        Analyze the following {request.language} code and the provided error log (if any).
        Identify the bug and provide a robust, idiomatic fix.
        
        CODE:
        ```{request.language}
        {request.code}
        ```
        
        ERROR LOG:
        {request.error_log if request.error_log else "No error log provided. Look for logical errors or potential improvements."}
        
        Provide your response in the following JSON format:
        {{
            "fixed_code": "the complete fixed code",
            "explanation": "a concise explanation of what was wrong and how it was fixed"
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        
        # Parse the JSON response
        import json
        result = json.loads(response.text)
        return CodeFixResponse(**result)

agent = ArchitectAgent()
