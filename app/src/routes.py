# External imports
from typing import Optional
import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Internal imports
from app.src.orchestrators.registry import PROCESSOR_REGISTRY

router = APIRouter()

class SingleDocumentRequest(BaseModel):
    file_name: Optional[str]
    file_content: Optional[str]
    extraction_schema: Optional[list[dict]]

class ProcessRequest(BaseModel):
    documents: list[SingleDocumentRequest]


@router.post("/extract")
async def process_document(request: ProcessRequest):

    processor = PROCESSOR_REGISTRY["extract"]()
    results = []

    for doc in request.documents:
        try:
            extracted_fields, validated_fields = processor.run(**doc.dict())
            results.append({
                "file_name": doc.file_name,
                "status": "success",
                "extracted_fields": extracted_fields,
                "validated_fields": validated_fields
            })
        except ValueError as ve:
            results.append({
                "file_name": doc.file_name,
                "status": "error",
                "detail": str(ve)
            })
        except Exception as e:
            traceback.print_exc()
            results.append({
                "file_name": doc.file_name,
                "status": "error",
                "detail": f"Internal Server Error: {e}"
            })

    return {"results": results}


@router.post("/analyze")
async def process_document(request: ProcessRequest):

    processor = PROCESSOR_REGISTRY["analyze"]()
    results = []

    for doc in request.documents:
        try:
            result = processor.run(**doc.dict())
            results.append({
                "file_name": doc.file_name,
                "status": "success",
                "analysis": result
            })
        except ValueError as ve:
            results.append({
                "file_name": doc.file_name,
                "status": "error",
                "detail": str(ve)
            })
        except Exception as e:
            traceback.print_exc()
            results.append({
                "file_name": doc.file_name,
                "status": "error",
                "detail": f"Internal Server Error: {e}"
            })

    return {"results": results}


@router.post("/analyze2")
async def process_document(request: ProcessRequest):

    # Assign the processor
    processor = PROCESSOR_REGISTRY["analyze"]()

    try:
        result = processor.run(**request.dict())
        return {"status": "success", "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")