from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, func
from app.database import Base

class Rider(Base):
    __tablename__ = "riders"
    __table_args__ = {"schema": "rider_schema"}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)
    vehicle_type = Column(String, nullable=False)
    license_plate = Column(String, nullable=False, unique=True)
    rating = Column(Numeric(3, 2), default=5.0)
    status = Column(String, default="Available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('Available', 'Busy')"),
        {"schema": "rider_schema"}
    )

class DistanceMatrix(Base):
    __tablename__ = "distance_matrix"
    __table_args__ = (
        UniqueConstraint("user_id", "rider_id", name="unique_user_rider_distance"),
        {"schema": "rider_schema"}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    rider_id = Column(Integer, nullable=False, index=True)
    distance_km = Column(Numeric(5, 2), nullable=False)