# External imports
from abc import ABC, abstractmethod 

# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_response, compose_prompt
from app.src.services.functions import count_tokens
from app.src.services.file_operations import load_txt_file
from app.src.config import ANALYSIS_SYSTEM_PROMPT_PATH


class BaseAnalyzer(BaseProcessor, ABC):

    @abstractmethod
    def extract_response(self, prompt: str, schema: list[dict]):
        pass

    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]):
        temp_file_path = self.load_file(file_name, file_content)
        extracted_text = self.extract_text(temp_file_path)

        tokens = count_tokens(extracted_text, "gpt-4o-mini")
        if tokens > 100_000:
            raise ValueError("Document is too long to process. Please provide a smaller document.")
        
        analysis_system_message = load_txt_file(ANALYSIS_SYSTEM_PROMPT_PATH)
        prompt_analysis = compose_prompt(extracted_text, analysis_system_message)
        extracted_response = self.extract_response(prompt_analysis, extraction_schema)

        return extracted_response
    

class deepseek_analyzer(BaseAnalyzer):
    def extract_response(self, prompt: str, schema: list[dict]):
        return deepseek_response(prompt, schema)

    

