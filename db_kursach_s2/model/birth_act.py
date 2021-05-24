from sqlalchemy import ForeignKey, Integer, Text

from db_kursach_s2.db import db
from db_kursach_s2.model.act import ActType, Act


class BirthAct(Act):
    __mapper_args__ = {"polymorphic_identity": ActType.birth}

    father_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    father = db.relationship("User")

    mother_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    mother = db.relationship("User")

    child_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    child = db.relationship("User")

    birthplace = db.Column(Text)
    child_nationality = db.Column(Text)
