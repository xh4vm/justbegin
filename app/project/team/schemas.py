from marshmallow import Schema, fields


class PutTeamWorkerSchema(Schema):
    email = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    worker_role_ids = fields.List(fields.Integer(required=True), required=True)


class DeleteTeamWorkerSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)


class DeleteWorkerRoleSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    worker_role_id = fields.Integer(required=True)


class PutTeamSchema(Schema):
    user_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)


put_team_worker_schema = PutTeamWorkerSchema()
delete_team_worker_schema = DeleteTeamWorkerSchema()
delete_worker_role_schema = DeleteWorkerRoleSchema()
put_team_schema = PutTeamSchema()
