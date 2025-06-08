# External imports
from pydantic import BaseModel, Field, create_model
from typing import Type

class ExtractedValue(BaseModel):
    value: str = Field(..., description="The extracted value")
    confidence_score: float = Field(..., description="The confidence score of the extraction")


# Function to dynamically build the model
def build_data_extraction_model(schema: list[dict]) -> Type[BaseModel]:
    """
    Dynamically builds a Pydantic model class with fields based on user schema.
    """
    python_type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool
    }

    try:
        fields = {}
        for item in schema:
            field_name = item["value_name"]
            field_type_str = item.get("data_type", "str")
            field_type = python_type_map.get(field_type_str, str)
            description = item.get("value_description", "")

            fields[field_name] = (field_type, Field(..., description=description))

        DataExtractionModel = create_model(
            "DataExtractionModel",
            **fields
        )

        return DataExtractionModel

    except Exception as e:
        raise ValueError(f"Failed to build data extraction model: {str(e)}")
    


def build_data_validation_model(schema: list[dict]) -> Type[BaseModel]:
    """
    Dynamically builds a Pydantic model class with fields based on user schema.
    """
    python_type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool
    }

    try:
        fields = {}
        for item in schema:
            field_name = item["value_name"]
            field_type_str = "float"
            field_type = python_type_map.get(field_type_str, str)
            description = f"Confidence score for {field_name}"

            fields[field_name] = (field_type, Field(..., description=description))

        DataValidationModel = create_model(
            "DataValidationModel",
            **fields
        )

        return DataValidationModel

    except Exception as e:
        raise ValueError(f"Failed to build data validation model: {str(e)}")