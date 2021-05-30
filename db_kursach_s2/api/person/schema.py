from db_kursach_s2.api.schemas import BaseSchema
from marshmallow import fields as f


class PersonSchema(BaseSchema):
    first_name = f.Str()
    last_name = f.Str()
    address = f.Str()
    date_of_birth = f.Date()
    passport_series = f.Str()
    passport_number = f.Str()
