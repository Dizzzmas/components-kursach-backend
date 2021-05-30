from jetkit.db.extid import ExtID
from sqlalchemy import Date
from sqlalchemy.types import Text

from db_kursach_s2.db import db


class Person(db.Model, ExtID):
    first_name = db.Column(Text)
    last_name = db.Column(Text)
    address = db.Column(Text)
    date_of_birth = db.Column(Date)
    passport_series = db.Column(Text)
    passport_number = db.Column(Text)

    fatherhoods = db.relationship(
        "BirthAct",
        foreign_keys="BirthAct.father_id",
    )
    childhoods = db.relationship(
        "BirthAct",
        foreign_keys="BirthAct.child_id"
    )


Person.add_create_uuid_extension_trigger()
