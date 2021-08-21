from marshmallow import Schema, fields


class PostUserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class PostResetSchema(Schema):
    email = fields.String(required=True)


class PutResetSchema(Schema):
    password = fields.String(required=True)


class PutUserSchema(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=True)
    nickname = fields.String(required=True)
    confirm_password = fields.String(required=True)
    password = fields.String(required=True)
    avatar = fields.String(required=False)
    telegram_nickname = fields.String(required=True)


post_user_schema = PostUserSchema()
post_reset_schema = PostResetSchema()
put_user_schema = PutUserSchema()
put_reset_schema = PutResetSchema()
