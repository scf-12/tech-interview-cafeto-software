"""
File containing related data sources and schemas for the application
"""
from app import app
from marshmallow import Schema, fields, validate


class CreateDocumentSectionSchema(Schema):
    path = fields.String(required=True)
    name = fields.String(
        required=True,
        validate=[validate.Length(
            1, error=f"Field must have at least {min} characters")]
    )
    text = fields.String(required=True)


documents_dict = {}
