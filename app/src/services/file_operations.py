# External imports
import os
import base64
import tempfile

def load_txt_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    

def decode_base64_to_tempfile(file_name: str, file_content: str) -> str:
    try:
        decoded_file_content = base64.b64decode(file_content)
        extension = os.path.splitext(file_name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            temp_file.write(decoded_file_content)
            temp_file_path = temp_file.name

        return temp_file_path
    except Exception as e:
        raise ValueError(f"Error decoding file: {e}")