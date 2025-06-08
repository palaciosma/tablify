# External imports
from openai import OpenAI
import os
import instructor
from dotenv import load_dotenv

# Internal imports
from app.src.services.classes import build_data_extraction_model, build_data_validation_model


load_dotenv() 

###################### PROMPT CREATION ######################

def compose_prompt(user_message: str, system_message: str) -> list[dict[str, str]]:

    try:
        prompt = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        return prompt

    except Exception as e:
        raise ValueError(f"Prompt creation failed: {e}")
        


###################### STRUCTURED EXTRACTION  ######################


def gpt_extraction(prompt: list[dict[str, str]], extraction_schema: list[dict]):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        extraction_model = build_data_extraction_model(extraction_schema)
    except Exception as e:
        raise ValueError(f"Error composing schema: {e}")
    
    try:
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=prompt,
            text_format=extraction_model,
            temperature=0.0
        )
        return response.output_parsed
    except Exception as e:
        raise ValueError(f"GPT extraction failed: {e}")
    
    

def deepseek_extraction(prompt: list[dict[str, str]], extraction_schema: list[dict]):

    client = instructor.from_openai(
        OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"),
        mode=instructor.Mode.MD_JSON,
    )

    try:
        extraction_model = build_data_extraction_model(extraction_schema)
    except Exception as e:
        raise ValueError(f"Error composing schema: {e}")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=prompt,
            response_model=extraction_model,
            temperature=0.0
            )

        return response
    except Exception as e:
        raise ValueError(f"Deepseek extraction failed: {e}")
    



###################### STRUCTURED VALIDATION ######################


def deepseek_validation(prompt: list[dict[str, str]], extraction_schema: list[dict]):

    client = instructor.from_openai(
        OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"),
        mode=instructor.Mode.MD_JSON,
    )

    try:
        extraction_model = build_data_validation_model(extraction_schema)
    except Exception as e:
        raise ValueError(f"Error composing schema: {e}")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=prompt,
            response_model=extraction_model,
            temperature=0.0
            )

        return response
    except Exception as e:
        raise ValueError(f"Deepseek extraction failed: {e}")




###################### GENERAL RESPONSE ######################


def deepseek_response(prompt: list[dict[str, str]]):

    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    
    try:
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=prompt,
            temperature=0.6
            )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        raise ValueError(f"Deepseek analysis failed: {e}")
