# External imports
from abc import ABC, abstractmethod 

# Internal imports
from app.src.services.file_operations import decode_base64_to_tempfile
from app.src.services.functions import extract_text_from_pdf

class BaseProcessor(ABC):
    def __init__(self):
        self.context = {}

    def load_file(self, file_name: str, file_content: str) -> str:
        
        try:
            if file_content:
                temp_file_path = decode_base64_to_tempfile(file_name, file_content)
                return temp_file_path

            else :
                raise ValueError(f"No file_content provided")

        except Exception as e:
            raise ValueError(f"Error decoding file: {e}")

    def extract_text(self, temp_file_path: str) -> str:
        try:
            extracted_text = extract_text_from_pdf(temp_file_path)
            return extracted_text
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
        
    
    @abstractmethod
    def run(self, *args, **kwargs) -> dict:
        pass


