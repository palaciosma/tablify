# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_response, compose_prompt
from app.src.services.functions import count_tokens
from app.src.services.file_operations import load_txt_file
from app.src.config import ANALYSIS_SYSTEM_PROMPT_PATH

class deepseek_analyzer(BaseProcessor):
    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]):
        
        # Decode base64 content to temp file
        temp_file_path = self.load_file(file_name, file_content)
        
        # Extract text from the temp PDF file
        extracted_text = self.extract_text(temp_file_path)
        
        # Check if document is too long
        tokens = count_tokens(extracted_text, "gpt-4o-mini")
        if tokens > 100_000:  # Leave room for system prompt + response
            raise ValueError("Document is too long to process. Please provide a smaller document.")
        else:
            # Compose prompt and extract fields
            system_message = load_txt_file(ANALYSIS_SYSTEM_PROMPT_PATH)
            prompt = compose_prompt(extracted_text, system_message)

            response = deepseek_response(prompt)

        return response
    

