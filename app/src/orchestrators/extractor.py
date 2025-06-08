# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_extraction, compose_prompt, gpt_extraction, deepseek_validation
from app.src.services.functions import count_tokens
from app.src.services.file_operations import load_txt_file
from app.src.config import EXTRACTION_SYSTEM_PROMPT_PATH, VALIDATION_SYSTEM_PROMPT_PATH

class deepseek_ext(BaseProcessor):
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
            system_message = load_txt_file(EXTRACTION_SYSTEM_PROMPT_PATH)
            prompt_extraction = compose_prompt(extracted_text, system_message)
            extracted_fields = deepseek_extraction(prompt_extraction, extraction_schema)

            # Run validation
            validation_system_message = load_txt_file(VALIDATION_SYSTEM_PROMPT_PATH)
            prompt_validation = compose_prompt(extracted_text, validation_system_message + "\n" + "Exracted fields:" + str(extracted_fields))
            validated_fields = deepseek_validation(prompt_validation, extraction_schema)


        return extracted_fields, validated_fields
    

class openai_ext(BaseProcessor):
    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]):
        
        # Decode base64 content to temp file
        temp_file_path = self.load_file(file_name, file_content)
        
        # Extract text from the temp PDF file
        extracted_text = self.extract_text(temp_file_path)
        
        # Compose prompt and extract fields
        extraction_system_message = load_txt_file(EXTRACTION_SYSTEM_PROMPT_PATH)
        prompt_extraction = compose_prompt(extracted_text, extraction_system_message)
        extracted_fields = gpt_extraction(prompt_extraction, extraction_schema)

        # Run validation
        validation_system_message = load_txt_file(VALIDATION_SYSTEM_PROMPT_PATH)
        prompt_validation = compose_prompt(extracted_text, validation_system_message + "\n" + "Exracted fields:" + str(extracted_fields))
        validated_fields = deepseek_validation(prompt_validation, extraction_schema)

        return extracted_fields, validated_fields

