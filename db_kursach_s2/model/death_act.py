from jetkit.db.model import TSTZ
from sqlalchemy import ForeignKey, Integer, Text, DateTime

from db_kursach_s2.db import db
from db_kursach_s2.model.act import ActType, Act


class DeathAct(Act):
    __mapper_args__ = {"polymorphic_identity": ActType.death}

    deceased_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    deceased = db.relationship("Person", foreign_keys="DeathAct.deceased_id")

    deceased_at = db.Column(TSTZ)
    deceased_age = db.Column(Integer)
    place_of_demise = db.Column(Text)
