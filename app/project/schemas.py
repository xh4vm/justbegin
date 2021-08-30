from marshmallow import Schema, fields


class CreateProjectSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String(required=False)


create_project_schema = CreateProjectSchema()
 