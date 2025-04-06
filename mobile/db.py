from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry

db = SQLAlchemy()

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