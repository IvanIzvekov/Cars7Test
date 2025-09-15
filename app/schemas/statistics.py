from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List


class StatisticsItemRead(BaseModel):
    operator_id: List[int]
    shift_id: Optional[List[int]]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    parameter_ids: Optional[List[int]]



class StatisticsItemCreate(BaseModel):
    parameter_id : int
    value: float
    operator_id: int
    shift_id: int
