# External imports
from abc import ABC, abstractmethod 
from tiktoken import get_encoding

# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_extraction, compose_prompt, gpt_extraction, deepseek_validation
from app.src.services.file_operations import load_txt_file
from app.src.config import EXTRACTION_SYSTEM_PROMPT_PATH, VALIDATION_SYSTEM_PROMPT_PATH


class BaseExtractor(BaseProcessor, ABC):
    MAX_TOKENS_PER_CHUNK = 5000
    OVERLAP_TOKENS = 500

    @abstractmethod
    def extract_fields(self, prompt: str, schema: list[dict]):
        pass

    @abstractmethod
    def validate_fields(self, prompt: str, schema: list[dict]):
        pass

    def get_tokenizer(self, model_name: str = "gpt-4o-mini"):
        # Change as needed; assuming tiktoken-like tokenizer
        return get_encoding("cl100k_base")  # Works for GPT-4/4o/3.5/DeepSeek

    def chunk_text(self, text: str) -> list[str]:
        tokenizer = self.get_tokenizer()
        tokens = tokenizer.encode(text)

        max_tokens = self.MAX_TOKENS_PER_CHUNK
        overlap = self.OVERLAP_TOKENS

        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunks.append(tokenizer.decode(chunk_tokens))
            start += max_tokens - overlap  # Move with overlap

        return chunks

    def merge_chunks(self, list_of_outputs: list[dict]) -> dict:
        merged = {}
        for output in list_of_outputs:
            merged.update(output)
        return merged

    def process_text(self, text: str, extraction_schema: list[dict]) -> tuple[dict, dict]:
        extraction_system_msg = load_txt_file(EXTRACTION_SYSTEM_PROMPT_PATH)
        validation_system_msg = load_txt_file(VALIDATION_SYSTEM_PROMPT_PATH)

        chunks = self.chunk_text(text)
        extracted_list = []
        validated_list = []

        for chunk in chunks:
            extraction_prompt = compose_prompt(chunk, extraction_system_msg)
            extracted = self.extract_fields(extraction_prompt, extraction_schema)

            validation_prompt = compose_prompt(
                chunk,
                f"{validation_system_msg}\nExtracted fields: {str(extracted)}"
            )
            validated = self.validate_fields(validation_prompt, extraction_schema)

            extracted_list.append(extracted)
            validated_list.append(validated)

        return self.merge_chunks(extracted_list), self.merge_chunks(validated_list)

    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]) -> tuple[dict, dict]:
        temp_file_path = self.load_file(file_name, file_content)
        extracted_text = self.extract_text(temp_file_path)
        return self.process_text(extracted_text, extraction_schema)



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
