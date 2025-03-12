from sqlalchemy import DateTime, column
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from flask_login import UserMixin

from .extensions import db

# Define User table
class User(db.Model, UserMixin):
    __tablename__ = "users" # Do not use global var for performance
    user_id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(unique = True, nullable = False)
    email: Mapped[str] = mapped_column(unique = True, nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)
    name: Mapped[str] = mapped_column(nullable = False)
    admin: Mapped[bool] = mapped_column()

class Sensor_Data(db.Model):
    __tablename__ = "sensor_data"
    data_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(nullable = False)
    time: Mapped[datetime] = mapped_column(nullable = False)
    location: Mapped = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    __table_args__ = {
        # To set partition by time
        'postgresql_partition_by': 'RANGE (time)'
    }

