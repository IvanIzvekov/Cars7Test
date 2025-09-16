from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List


class StatisticsItemRead(BaseModel):
    operator_ids: List[int] | None = None
    shift_ids: Optional[List[int]] | None = None
    start_date: Optional[datetime] | None = None
    end_date: Optional[datetime] | None = None
    parameter_ids: Optional[List[int]] | None = None



class StatisticsItemCreate(BaseModel):
    parameter_id : int
    value: float
    operator_id: int
    shift_id: int
