from marshmallow import Schema, fields


class AddTeammateSchema(Schema):
    email = fields.String(required=True)
    project_id = fields.Integer(required=True)
    teammate_role_ids = fields.List(fields.Integer(required=True))


class DeleteTeammateSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)


class DeleteTeammateRoleSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    teammate_role_id = fields.Integer(required=True)

add_teammate_schema = AddTeammateSchema()
delete_teammate_schema = DeleteTeammateSchema()
delete_teammate_role_schema = DeleteTeammateRoleSchema()
