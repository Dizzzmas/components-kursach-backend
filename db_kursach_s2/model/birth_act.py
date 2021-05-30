from sqlalchemy import ForeignKey, Integer, Text

from db_kursach_s2.db import db
from db_kursach_s2.model.act import ActType, Act


class BirthAct(Act):
    __mapper_args__ = {"polymorphic_identity": ActType.birth}

    father_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    father = db.relationship("Person", foreign_keys="BirthAct.father_id")

    mother_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    mother = db.relationship("Person", foreign_keys="BirthAct.mother_id")

    child_id = db.Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
    child = db.relationship("Person", foreign_keys="BirthAct.child_id")

    birthplace = db.Column(Text)
    child_nationality = db.Column(Text)
