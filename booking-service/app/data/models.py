from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint, func
from app.data.database import Base

class Ride(Base):
    __tablename__ = "rides"
    __table_args__ = {"schema": "booking_schema"}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    rider_id = Column(Integer, nullable=False)
    pickup_location = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    distance_km = Column(Numeric(5, 2), nullable=False)
    fare_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False, default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('Pending', 'In Progress', 'Completed', 'Canceled')"),
        {"schema": "booking_schema"}
    )