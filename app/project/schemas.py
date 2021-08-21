from marshmallow import Schema, fields


class PutProjectSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String(required=False)


class PostLikeSchema(Schema):
    project_id = fields.Integer(required=True)


class DeleteProjectSchema(Schema):
    project_id = fields.Integer(required=True)


post_like_schema = PostLikeSchema()
delete_project_schema = DeleteProjectSchema()
put_project_schema = PutProjectSchema()
 