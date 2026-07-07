import os
import logging
import re
import time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIConfig(BaseModel):
    # Prefer OpenRouter API Key, then OpenAI
    api_key: str = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("AI_MODEL", "openai/gpt-4o-mini")
    base_url: str = "https://openrouter.ai/api/v1"
    timeout: int = 120  # AI specific timeout
    max_retries: int = 3

class AIService:
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        if not self.config.api_key:
            logger.warning("No API key found (Checked OPENROUTER_API_KEY and OPENAI_API_KEY).")
        
        # Configure client with OpenRouter base URL
        self.client = openai.OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )

    def _clean_code(self, code: str) -> str:
        if not code:
            return ""
            
        # 1. Try to find content inside code blocks
        # This matches ```language\n code \n```
        code_block_pattern = r'```(?:\w+)?\s*([\s\S]*?)```'
        matches = re.findall(code_block_pattern, code)
        
        if matches:
            # Join all code blocks found
            return "\n".join(matches).strip()
            
        # 2. If no code blocks, check for leading language identifiers on first line
        lines = code.strip().split('\n')
        if lines:
            first_line = lines[0].strip().lower()
            if first_line in ['python', 'javascript', 'java', 'cpp', 'c++', 'c', 'typescript']:
                return "\n".join(lines[1:]).strip()
                
        # 3. Last resort: just clean backticks if they are somehow mismatched
        return code.replace('```', '').strip()

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                start_time = time.time()
                logger.info(f"AI Request (Attempt {attempt + 1}/{self.config.max_retries}) using model {self.config.model}")
                
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500, # Reduced to save time/tokens
                    timeout=self.config.timeout # Ensure timeout is applied to the request
                )
                
                duration = time.time() - start_time
                logger.info(f"AI Response received successfully in {duration:.2f}s.")
                return response.choices[0].message.content or ""
                
            except Exception as e:
                last_error = e
                duration = time.time() - start_time
                error_type = type(e).__name__
                logger.warning(f"AI Request attempt {attempt + 1} failed ({error_type}) after {duration:.2f}s: {e}")
                
                if "timeout" in str(e).lower() or "deadline" in str(e).lower():
                    logger.error(f"AI Service Timeout: The request took longer than {self.config.timeout}s.")
                
                if attempt < self.config.max_retries - 1:
                    wait_time = 2 ** attempt # Exponential backoff
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                continue

        logger.error(f"AI generation failed after {self.config.max_retries} attempts: {last_error}")
        raise Exception(f"AI Service Error (Timeout or Connection): {str(last_error)}")

    def generate_code(self, prompt: str, language: str = "python") -> str:
        system_prompt = f"You are an expert {language} programmer. Return ONLY the code, no explanations."
        response = self.generate_response(prompt, system_prompt)
        return self._clean_code(response)

    def debug_code(self, code: str, error_message: str, language: str = "python") -> str:
        prompt = f"Fix this {language} code:\n{code}\nError: {error_message}"
        system_prompt = "You are a debugging expert. Return ONLY the fixed code."
        response = self.generate_response(prompt, system_prompt)
        return self._clean_code(response)

    def optimize_code(self, code: str, language: str = "python") -> str:
        prompt = f"Optimize this {language} code:\n{code}"
        system_prompt = "You are a code optimization expert. Return ONLY the optimized code."
        response = self.generate_response(prompt, system_prompt)
        return self._clean_code(response)

    def explain_code(self, code: str, language: str = "python") -> str:
        prompt = f"Explain this {language} code:\n{code}"
        system_prompt = "You are a code explanation expert. Provide a detailed but concise explanation."
        return self.generate_response(prompt, system_prompt)

    def generate_tests(self, code: str, language: str = "python") -> str:
        prompt = f"Generate unit tests for this {language} code:\n{code}"
        system_prompt = "You are a testing expert. Return ONLY the test code."
        response = self.generate_response(prompt, system_prompt)
        return self._clean_code(response)

    def augment_with_execution(self, code: str, language: str = "python") -> str:
        prompt = (
            f"The following {language} code contains only function/class definitions. "
            f"Please rewrite the ENTIRE code to include a main execution block (e.g., if __name__ == '__main__' for Python, "
            f"public static void main for Java, int main() for C/C++, etc.). "
            f"Add sample function calls with dummy data and use print statements to display the return values to the console.\n\n"
            f"Code:\n{code}"
        )
        system_prompt = "You are an expert developer. Return ONLY the code without explanations."
        response = self.generate_response(prompt, system_prompt)
        return self._clean_code(response)

    def create_plan(self, user_request: str, language: str = "python") -> str:
        prompt = f"Create a step-by-step implementation plan for: {user_request} in {language}."
        system_prompt = "You are a software architect. Provide a numbered list of steps."
        return self.generate_response(prompt, system_prompt)

    def list_models(self) -> List[str]:
        # Return OpenRouter models
        return [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "anthropic/claude-3-haiku",
            "google/gemini-pro-1.5",
            "meta-llama/llama-3-8b-instruct"
        ]
