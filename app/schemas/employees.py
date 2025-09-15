from enum import Enum
from typing import Optional
from pydantic import BaseModel

class EmployeePositions(str, Enum):
    MANAGER = 'manager'
    SUPEROPERATOR = 'superoperator'
    OPERATOR = 'operator'
    SENIOR_OPERATOR = 'senior operator'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value_lower = value.lower()
            for member in cls:
                if member.value == value_lower:
                    return member
        return None


class EmployeesStatuses(str, Enum):
    SETTLED = 'settled'
    FIRED = 'fired'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value_lower = value.lower()
            for member in cls:
                if member.value == value_lower:
                    return member
        return None


class EmployeeItemCreate(BaseModel):
    last_name: str
    first_name: str
    second_name: Optional[str] = None
    position: EmployeePositions
    status: EmployeesStatuses
