from marshmallow import Schema, fields


class PostCommentSchema(Schema):
    content = fields.String(required=True)
    parent_comment_id = fields.Integer(required=False)


class PutCommentSchema(Schema):
    content = fields.String(required=True)
    

post_comment_schema = PostCommentSchema()
put_comment_schema = PutCommentSchema()
