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
        self._client = None
        self.model_id = "gemini-2.0-flash"

    @property
    def client(self):
        if self._client is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
            self._client = genai.Client(api_key=api_key)
        return self._client

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
        {request.error_log if request.error_log else "No error log provided."}
        
        Provide your response in JSON format:
        {{
            "fixed_code": "the complete fixed code",
            "explanation": "a concise explanation"
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        
        import json
        result = json.loads(response.text)
        return CodeFixResponse(**result)

agent = ArchitectAgent()