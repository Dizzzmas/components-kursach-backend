from jetkit.db.model import TSTZ
from sqlalchemy import ForeignKey, Integer, Text, DateTime, Date

from db_kursach_s2.db import db
from db_kursach_s2.model.act import ActType, Act


class MarriageAct(Act):
    __mapper_args__ = {"polymorphic_identity": ActType.marriage}

    bride_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    bride = db.relationship("Person", foreign_keys="MarriageAct.bride_id")

    groom_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    groom = db.relationship("Person", foreign_keys="MarriageAct.groom_id")

    groom_last_name = db.Column(Text)
    bride_last_name = db.Column(Text)

    wed_at = db.Column(Date)
