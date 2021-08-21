from marshmallow import Schema, fields, validates_schema, ValidationError


class PostProjectStorySchema(Schema):
    title: str = fields.String(required=True)
    content: str = fields.String(required=True)


class PutProjectStorySchema(Schema):
    title: str = fields.String(required=False)
    content: str = fields.String(required=False)

    @validates_schema
    def validate_title_or_content_required(self, data, **kwargs) -> None:
        if 'title' not in data and 'content' not in data:
            raise ValidationError('title or content required')


post_project_story_schema = PostProjectStorySchema()
put_project_story_schema = PutProjectStorySchema()
