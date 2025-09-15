from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from app.models.base import Base

class Break(Base):
    __tablename__ = "breaks"

    id = Column(Integer, primary_key=True)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
