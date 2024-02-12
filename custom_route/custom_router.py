from fastapi import APIRouter
from pydantic import BaseModel
from utils import normalizer, input_formatter

custom_router = APIRouter(prefix="/api")


class ValidationResult(BaseModel):
    code: int
    status: str
    result: dict


@custom_router.post("/validate_data")
def validate_data(input_data: str) -> ValidationResult:
    try:
        input_data = input_formatter.preprocess_xml_or_json(input_data)
        normalized_tree = normalizer.normalize(input_data)
        return ValidationResult(code=200, status="success", result=normalized_tree)
    except Exception as exception:
        return ValidationResult(
            code=500,
            status="internal server error",
            result={"exception": str(exception)},
        )
