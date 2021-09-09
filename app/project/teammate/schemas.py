from marshmallow import Schema, fields


class PostTeammateSchema(Schema):
    email = fields.String(required=True)
    project_id = fields.Integer(required=True)
    role_ids = fields.List(fields.Integer(required=True))


class DeleteTeammateSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)


class DeleteTeammateRoleSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    role_id = fields.Integer(required=True)

post_teammate_schema = PostTeammateSchema()
delete_teammate_schema = DeleteTeammateSchema()
delete_teammate_role_schema = DeleteTeammateRoleSchema()
