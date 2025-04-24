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

class Run_History(db.Model):
    __tablename__ = 'run_history'
    
    run_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable = False)
    start_time: Mapped[datetime.datetime] = mapped_column(
        nullable=False, 
        default=func.now()
    )

    finish_goal: Mapped[bool] = mapped_column(nullable=False)
    calorie: Mapped[float] = mapped_column(nullable=False)
    step: Mapped[int] = mapped_column(nullable=False)
    total_distance: Mapped[float] = mapped_column(nullable=False)
    total_time: Mapped[datetime.timedelta] = mapped_column(nullable=False)
    pace: Mapped[float] = mapped_column(nullable=False)

    def to_dict(self):
        return {
            "run_id": self.run_id,
            "user_id": self.user_id,
            "start_time": self.start_time.isoformat(),
            "finish_goal": self.finish_goal,
            "calorie": self.calorie,
            "step": self.step,
            "total_distance": self.total_distance,
            "total_time": self.total_time.total_seconds(),
            "pace": self.pace,
        }
    
    @classmethod
    def get_overall(self, user_id: int) -> dict:
        """
        Return a dict of overall statistics of user's: total distance, longest_run, avg_pace, total_calories
        """
        # run_count = db.session.query(self.run_id).count()
        distance = db.session.query(func.sum(Run_History.total_distance)).filter(Run_History.user_id == user_id).scalar() or 0.0
        longest_run = db.session.query(func.max(Run_History.total_distance)).filter(Run_History.user_id == user_id).scalar() or 0.0
        fastest_pace = db.session.query(func.max(Run_History.pace)).filter(Run_History.user_id == user_id).scalar() or 0.0

        total_run_num = db.session.query(Run_History.run_id).filter(Run_History.user_id == user_id).count() or 0.0
        try:
            success_rate = (db.session.query(func.sum(Run_History.finish_goal)).filter(Run_History.user_id == user_id).scalar() or 0.0) * 100 / total_run_num
            success_rate = round(success_rate, 0)
        except ZeroDivisionError:
            success_rate = "null"

        return {"total_distance": distance, "longest_run": longest_run, "fastest_pace": fastest_pace,
                "total_run_num": total_run_num, "success_rate": success_rate}

    @classmethod
    def get_overall_month(self, user_id: int, year: int, month: int) -> list["Run_History"]:
        """
        List Run_History within the year and month of the timestart
        """
        distance = db.session.query(func.sum(Run_History.total_distance)).filter(
            and_(Run_History.user_id == user_id,
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month)).scalar() or 0.0
        longest_run = db.session.query(func.max(Run_History.total_distance)).filter(
            and_(Run_History.user_id == user_id,
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month)).scalar() or 0.0
        fastest_pace = db.session.query(func.max(Run_History.pace)).filter(
            and_(Run_History.user_id == user_id,
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month)).scalar() or 0.0
        total_run_num = db.session.query(Run_History.run_id).filter(
            and_(Run_History.user_id == user_id,
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month)).count() or 0.0
        total_calories = db.session.query(func.max(Run_History.calorie)).filter(
            and_(Run_History.user_id == user_id,
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month)).scalar() or 0.0

        return {"total_distance": distance, "longest_run": longest_run, "fastest_pace": fastest_pace,
                "total_run_num": total_run_num, "total_calories": total_calories}

    @classmethod
    def get_by_day(self, user_id: int, target_day: datetime.date) -> list["Run_History"]:
        """
        Return list of Run_History timestart of target_day (timezone).
        """
        return (
            db.session.query(self)
            .filter(
                and_(func.date(self.start_time) == target_day, self.user_id == user_id)
            )
            .order_by(self.start_time)
            .all()
        )

    @classmethod
    def get_by_month(self, user_id: int, year: int, month: int) -> list["Run_History"]:
        """
        List Run_History within the year and month of the timestart
        """
        return (
            db.session.query(self)
            .filter(and_(
                func.extract('year', self.start_time) == year,
                func.extract('month', self.start_time) == month,
                self.user_id == user_id
                ))
            .order_by(self.start_time)
            .all()
        )

    @classmethod
    def get_by_week(self, user_id: int, some_date: datetime.date) -> list["Run_History"]:
        """
        List Run_History of the week with the date.
        Week starts from Monday
        """
        # Tính ngày thứ Hai của tuần
        week_start = some_date - datetime.timedelta(days = some_date.weekday())
        # Tuần kết thúc vào Chủ Nhật cùng tuần
        week_end = week_start + datetime.timedelta(days=6)
        return (
            db.session.query(self)
            .filter(and_(
                self.start_time >= datetime.datetime.combine(week_start, datetime.datetime.min.time()),
                self.start_time < datetime.datetime.combine(week_end + datetime.timedelta(days=1), datetime.datetime.min.time()),
                self.user_id == user_id
                ))
            .order_by(self.start_time)
            .all()
        )
    
    @classmethod
    def get_distance_older_than_months(self, user_id: int, months: int = 1) -> list["Run_History"]:
        """
        Return a list of record with start_time more than 'months'.
        """
        # Calculate the cuttoff date
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days = 30 * months)
        data = (
            db.session.query(self)
            .filter(and_(self.start_time < cutoff_date,
                         self.user_id == user_id
                         ))
            .order_by(self.start_time)
            .all()
        )

        data = [{"start_time": run.start_time,
                 "total_distance": run.total_distance}
                 for run in data]
        return data
    
    @classmethod
    def get_distance_older_than_months(self, user_id: int, months: int = 1) -> list["dict"]:
        """
        Return a LIST of DICT record with start_time less than 'months'.
        """
        # Calculate the cuttoff date
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days = 30 * months)
        data = (
            db.session.query(self.start_time, self.total_distance)
            .filter(and_(self.start_time > cutoff_date,
                         self.user_id == user_id
                         ))
            .order_by(self.start_time)
            .all()
        )

        data = [{"start_time": run.start_time,
                 "total_distance": run.total_distance}
                 for run in data]
        return data
    
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