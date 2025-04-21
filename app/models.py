import datetime
from sqlalchemy import func, or_, and_, ForeignKey
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

    goal: Mapped[float] = mapped_column(nullable = True, default = 1)

    def get_id(self):
        return self.user_id
    
    @classmethod
    def is_duplicate(self, username, email):
        # Check if username or email is duplicated with only one query
        return db.session.query(self.user_id).filter(
            or_(self.username == username, self.email == email)
        ).first() is not None
    
    @classmethod
    def update_password(self, email: str, new_password: str) -> None:
        """
        Update user's password.

        :email: user's email.
        :new_password: the updated password of the account.
        """
        db.session.query(self).\
            filter(User.email == email).\
            update({'password': new_password})
        db.session.commit()

    @classmethod
    def update_goal(self, user_id: int, new_goal: float) -> None:
        """
        Update user's goal.

        :user_id: user's user_id.
        :new_goal: the updated goal.
        """
        db.session.query(self).\
            filter(User.user_id == user_id).\
            update({'goal': new_goal})
        db.session.commit()

    @classmethod
    def get_goal(self, user_id: int) -> float:
        """
        Get user's goal.

        :user_id: user's id
        :return: user's goal that is a numeric data
        """
        goal = db.session.query(self.goal).\
            filter(User.user_id == user_id).\
            first()
        return goal[0] if goal else None

# Define sensor data table
class Sensor_Data(db.Model):
    __tablename__ = "sensor_data"
    data_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable = False)
    start_time: Mapped[int] = mapped_column(nullable = False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable = False)
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    # To set partition by time
    __table_args__ = {
        'postgresql_partition_by': 'RANGE (time)'
    }

    def get_id(self):
        return self.data_id
    
    @classmethod
    def get_running_session(self, user_id, start_time):
        """
        Query returns: [(user_id, created_at, latitude, longitude), (user_id, created_at, latitude, longitude),...]
        """
        from geoalchemy2 import functions
        
        return db.session.query(self.user_id, self.created_at, functions.ST_Y(self.location), functions.ST_X(self.location)).\
            select_from(Sensor_Data).\
            filter(
            and_(self.user_id == user_id, self.start_time == start_time)
        ).all()
    
class Forgot_Password(db.Model):
    __tablename__ = "forgot_password"
    fp_id: Mapped[int] = mapped_column("fp_id", primary_key = True)
    email: Mapped[str] = mapped_column(nullable = False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable = False)
    hashed_timestamp: Mapped[str] = mapped_column(nullable = False)

    @classmethod
    def take_email_from_hash(self, hashed_timestamp):
        """
        Take email from a hashed timestamp, while checking if the created_at timestamp is less than 1 hour away.

        :hashed_timestamp: A hashed timestamp, used to get unique string.
        """
        # Get current timestamp (GMT+7)
        current_timestamp = datetime.datetime.now(tz = datetime.timezone(datetime.timedelta(seconds=25200)))

        # Check if username or email is duplicated with only one query
        result = db.session.query(self.email, self.created_at).filter(
            self.hashed_timestamp == hashed_timestamp,
            current_timestamp - self.created_at <= datetime.timedelta(hours = 1)
        ).first()
        return result[0] if result else None
    
class Mobile_Session(db.Model):
    __tablename__ = "mobile_session"
    mobile_id: Mapped[int] = mapped_column("mobile_id", primary_key = True)
    user_id: Mapped[int] = mapped_column(nullable = False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable = False)
    hashed_timestamp: Mapped[str] = mapped_column(nullable = False)

    @classmethod
    def create_session(self, user_id: str, created_at: str, hashed_timestamp: str) -> None:
        """
        Create session if there has been none.
        Renew session if the hour is more than 24 hours.
        """
        # Get current timestamp (GMT+7)
        user_session = db.session.query(self.user_id).filter(
            self.user_id == user_id,
        ).first()

        user_session = True if user_session else False

        # Query
        if user_session:
            db.session.query(Mobile_Session).\
            filter(Mobile_Session.user_id == user_id).\
            update({'created_at': func.now(),'hashed_timestamp': hashed_timestamp})
        else:
            mobile_session = Mobile_Session(user_id = user_id, created_at = created_at, hashed_timestamp = hashed_timestamp)
            db.session.add(mobile_session)
        db.session.commit()

    @classmethod
    def get_user_id_from_hash(self, hashed_timestamp):
        """
        Take email from a hashed timestamp, while checking if the created_at timestamp is less than 1 hour away.

        :hashed_timestamp: A hashed timestamp, used to get user_id.
        """
        result = db.session.query(self.user_id).filter(
            self.hashed_timestamp == hashed_timestamp,
            func.now() - self.created_at <= datetime.timedelta(hours = 24)
        ).first()
        return result[0] if result else None

# Define running history table
class Personal_Stat(db.Model, UserMixin):
    __tablename__ = "personal_stat"
    person_id: Mapped[int] = mapped_column("person_id", primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, unique=True)
    weight: Mapped[float] = mapped_column(nullable=False, default=70)
    height: Mapped[float] = mapped_column(nullable=False, default=1.7)
    age: Mapped[int] = mapped_column(nullable=False, default=20)

    user = db.relationship("User", backref="personal_stat", uselist=False)

    @classmethod
    def get_weight(self, user_id: int) -> float:
        """
        Get user's weight.

        :user_id: user's id
        :return: user's weight that is a numeric data
        """
        weight = db.session.query(self.weight).\
            filter(User.user_id == user_id).\
            first()
        return weight[0] if weight else None

    @classmethod
    def get_height(self, user_id: int) -> float:
        """
        Get user's height.

        :user_id: user's id
        :return: user's height that is a numeric data
        """
        height = db.session.query(self.height).\
            filter(User.user_id == user_id).\
            first()
        return height[0] if height else None