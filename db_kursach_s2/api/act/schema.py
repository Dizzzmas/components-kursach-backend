from marshmallow_enum import EnumField
from marshmallow import fields as f
from marshmallow_oneofschema import OneOfSchema

from db_kursach_s2.api.person.schema import PersonSchema
from db_kursach_s2.api.schemas import BaseSchema
from db_kursach_s2.model import BirthAct, DeathAct, MarriageAct
from db_kursach_s2.model.act import ActType


class BaseActSchema(BaseSchema):
    type = EnumField(ActType, required=True)
    issued_by = f.Integer()
    issued_at = f.Date()
    created_by = f.Nested(PersonSchema)


class BirthActSchema(BaseActSchema):
    father = f.Nested(PersonSchema)
    mother = f.Nested(PersonSchema)
    child = f.Nested(PersonSchema)
    birthpalce = f.Str()
    child_nationality = f.Str()


class MarriageActSchema(BaseActSchema):
    bride = f.Nested(PersonSchema)
    groom = f.Nested(PersonSchema)
    bride_last_name = f.Str()
    groom_last_name = f.Str()
    wed_at = f.Date()


class DeathActSchema(BaseActSchema):
    deceased = f.Nested(PersonSchema)
    deceased_at = f.Date()
    deceased_age = f.Integer()
    place_of_demise = f.Str()


class ActSchema(OneOfSchema):
    type_schemas = {
        "birth": BirthActSchema,
        "death": DeathActSchema,
        "marriage": MarriageActSchema,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, BirthAct):
            return "birth"
        elif isinstance(obj, DeathAct):
            return "death"
        elif isinstance(obj, MarriageAct):
            return "marriage"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class UpsertActSchema(BirthActSchema, DeathActSchema, MarriageActSchema):
    father_id = f.Str()
    mother_id = f.Str()
    child_id = f.Str()

    deceased_id = f.Str()

    bride_id = f.Str()
    groom_id = f.Str()

    created_by_id = f.Str()

    class Meta:
        exclude = ("father", "mother", "child", "deceased", "bride", "groom")
