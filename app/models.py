from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define User table
class User(db.Model, UserMixin):
    __tablename__ = "users" # Do not use global var for performance
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(nullable=False)
    vip_status: Mapped[bool] = mapped_column()