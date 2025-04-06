from datetime import datetime
from sqlalchemy import or_, and_, ForeignKey, cast, Date
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from flask_login import UserMixin

from .extensions import db

# Define User table
class User(db.Model, UserMixin):
    __tablename__ = "users" # Do not use global var for performance
    user_id: Mapped[int] = mapped_column("user_id", primary_key = True)
    username: Mapped[str] = mapped_column(unique = True, nullable = False)
    email: Mapped[str] = mapped_column(unique = True, nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)
    name: Mapped[str] = mapped_column(nullable = False)
    admin: Mapped[bool] = mapped_column()

    def get_id(self):
        return self.user_id
    
    @classmethod
    def is_duplicate(self, username, email):
        # Check if username or email is duplicated with only one query
        return db.session.query(self.user_id).filter(
            or_(self.username == username, self.email == email)
        ).first() is not None
    
# Define sensor data table
class Sensor_Data(db.Model):
    __tablename__ = "sensor_data"
    data_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable = False)
    time: Mapped[datetime] = mapped_column(nullable = False)
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    # To set partition by time
    __table_args__ = {
        'postgresql_partition_by': 'RANGE (time)'
    }

    def get_id(self):
        return self.data_id
    
# Define running history table
class Run_History(db.Model, UserMixin):
    __tablename__ = "run_history"
    run_id: Mapped[int] = mapped_column("run_id", primary_key = True)
    user_id: Mapped[int] = mapped_column(nullable = False)
    start_time: Mapped[datetime] = mapped_column(nullable = False)
    end_time: Mapped[datetime] = mapped_column(nullable = False)
    distance_km: Mapped[float] = mapped_column(nullable = False)
    avg_speed: Mapped[float] = mapped_column()

    @classmethod
    def history_on_user_start_time(self, user_id, chosen_time):
        """
        :chosen_time: date(2025, 3, 31), while self.start_time will be in ISO format "2025-04-04 10:05:00+00"
        """
        # Tạo truy vấn
        return db.session.query(self.run_id).filter(
            and_(self.user_id == user_id, cast(self.start_time, Date) == chosen_time)
        )
    
class Forgot_Password(db.Model):
    __tablename__ = "forgot_password"
    fp_id: Mapped[int] = mapped_column("fp_id", primary_key = True)
    email: Mapped[str] = mapped_column(nullable = False)
    hashed_timestamp: Mapped[str] = mapped_column(nullable = False)

    @classmethod
    def take_email_from_hash(self, hashed_timestamp):
        # Check if username or email is duplicated with only one query
        # TODO: added a method to get email from this query
        # return "a"
        result = db.session.query(self.email).filter(
            self.hashed_timestamp == hashed_timestamp
        ).first()
        return result[0] if result else None