from sqlalchemy import Column, Integer, String, Numeric
from app.models.base import Base

class Coefficient(Base):
    __tablename__ = "coefficients"

    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False)
    norm = Column(Numeric, nullable=False)
    base = Column(Numeric, nullable=False)
    weight = Column(Numeric)
    type = Column(String(20), nullable=False)