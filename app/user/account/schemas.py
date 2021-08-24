from marshmallow import Schema, fields, validate, ValidationError

def validate_extension(file_name: str):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    if len(file_name) < 4:
        raise ValidationError("Недопустимый файл")

    if not file_name[-3:].lower() in ALLOWED_EXTENSIONS:
        raise ValidationError("Недопустимый тип файла")

class PostSettingsSchema(Schema):
    nickname = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.Email(required=True)
    avatar = fields.String(required=False, validate=validate_extension)
    telegram_nickname = fields.String(required=True)

class PostDeleteAccountSchema(Schema):
    user_message = fields.String(required=True)

post_settings_schema = PostSettingsSchema()
post_delete_account_schema = PostDeleteAccountSchema()