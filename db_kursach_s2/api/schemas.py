from marshmallow import Schema, fields as f


class BaseSchema(Schema):
    extid = f.UUID(dump_only=True, data_key="id")
    created_at = f.DateTime()
    updated_at = f.DateTime()
