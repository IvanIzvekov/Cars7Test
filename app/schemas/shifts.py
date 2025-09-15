from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShiftItemCreate(BaseModel):
    operator_id: int


class ShiftItemUpdate(BaseModel):
    shift_id: int