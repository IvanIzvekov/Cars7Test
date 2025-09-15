from sqlalchemy import Column, Integer, Numeric, TIMESTAMP, ForeignKey
from app.models.base import Base

class OperatorStatistics(Base):
    __tablename__ = "operator_statistics"

    id = Column(Integer, primary_key=True)
    stat_date = Column(TIMESTAMP, nullable=False)
    parameter_id = Column(Integer, ForeignKey("coefficients.id"), nullable=False)
    value = Column(Numeric, nullable=False)
    operator_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)

