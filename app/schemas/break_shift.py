from pydantic import BaseModel

class BreakShiftItemCreate(BaseModel):
    operator_id: int
    shift_id: int


class BreakShiftItemClose(BaseModel):
    break_id: int