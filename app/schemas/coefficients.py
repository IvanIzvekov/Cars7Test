from enum import Enum
from typing import List
from pydantic import BaseModel, confloat

class CoefficientType(str, Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value_lower = value.lower()
            for member in cls:
                if member.value == value_lower:
                    return member
        return None

class CoefficientItem(BaseModel):
    parameter: str
    norm: float
    base: float
    weight: confloat(ge=0.0, le=1.0)
    type: CoefficientType

class CoefficientUpdateRequest(BaseModel):
    coefficients: List[CoefficientItem]

class CoefficientItemCreate(BaseModel):
    parameter: str
    norm: float
    base: float
    type: CoefficientType
