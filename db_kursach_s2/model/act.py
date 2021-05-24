from enum import unique, Enum
from typing import Any, Dict, Mapping

from jetkit.db.extid import ExtID
from jetkit.model.asset import S3Asset
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import Text

from db_kursach_s2.db import db


@unique
class ActType(Enum):
    marriage = "marriage"
    birth = "birth"
    death = "death"


class Act(db.Model, ExtID):
    type = db.Column(db.Enum(ActType), nullable=False)
    issued_by = db.Column(Integer)
    issued_at = db.Column(Date)
    created_by_id = db.Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL")
    )
    created_by = db.relationship(
        "User", back_populates="created_acts", foreign_keys="Act.created_by_id"
    )

    __mapper_args__: Mapping[str, Any] = {"polymorphic_on": type}


Act.add_create_uuid_extension_trigger()
