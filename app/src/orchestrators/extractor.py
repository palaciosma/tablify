# External imports
from abc import ABC, abstractmethod 

# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_extraction, compose_prompt, gpt_extraction, deepseek_validation
from app.src.services.functions import count_tokens
from app.src.services.file_operations import load_txt_file
from app.src.config import EXTRACTION_SYSTEM_PROMPT_PATH, VALIDATION_SYSTEM_PROMPT_PATH



class BaseExtractor(BaseProcessor, ABC):

    @abstractmethod
    def extract_fields(self, prompt: str, schema: list[dict]):
        pass

    @abstractmethod
    def validate_fields(self, prompt: str, schema: list[dict]):
        pass

    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]):
        temp_file_path = self.load_file(file_name, file_content)
        extracted_text = self.extract_text(temp_file_path)

        tokens = count_tokens(extracted_text, "gpt-4o-mini")
        if tokens > 100_000:
            raise ValueError("Document is too long to process. Please provide a smaller document.")
        
        extraction_system_message = load_txt_file(EXTRACTION_SYSTEM_PROMPT_PATH)
        prompt_extraction = compose_prompt(extracted_text, extraction_system_message)
        extracted_fields = self.extract_fields(prompt_extraction, extraction_schema)

        validation_system_message = load_txt_file(VALIDATION_SYSTEM_PROMPT_PATH)
        prompt_validation = compose_prompt(
            extracted_text,
            validation_system_message + "\n" + "Extracted fields:" + str(extracted_fields)
        )
        validated_fields = self.validate_fields(prompt_validation, extraction_schema)

        return extracted_fields, validated_fields


class deepseek_ext(BaseExtractor):
    def extract_fields(self, prompt: str, schema: list[dict]):
        return deepseek_extraction(prompt, schema)

    def validate_fields(self, prompt: str, schema: list[dict]):
        return deepseek_validation(prompt, schema)


class openai_ext(BaseExtractor):
    def extract_fields(self, prompt: str, schema: list[dict]):
        return gpt_extraction(prompt, schema)

    def validate_fields(self, prompt: str, schema: list[dict]):
        return deepseek_validation(prompt, schema)  
