from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from app.models.base import Base

class SalaryCalculation(Base):
    __tablename__ = "salary_calculation"

    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False)
    value = Column(Numeric, nullable=False)
    total = Column(Numeric, nullable=False)
    start_at = Column(TIMESTAMP, nullable=False)
    end_at = Column(TIMESTAMP, nullable=False)
    operator_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
