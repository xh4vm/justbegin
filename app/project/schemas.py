from marshmallow import Schema, fields


class PostLikeSchema(Schema):
    project_id = fields.String(required=True)


class PutProjectSchema(Schema):
    content = fields.String(required=True)


post_like_schema = PostLikeSchema()
