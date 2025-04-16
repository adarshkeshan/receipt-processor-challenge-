# schemas.py
from marshmallow import fields, validate, Schema
from extensions import ma

class ItemSchema(ma.Schema):
    shortDescription = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[\w\s\-]+$"),
        data_key="shortDescription"
    )
    price = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d+\.\d{2}$"),
    )

class ReceiptSchema(ma.Schema):
    retailer = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[\w\s\-&]+$")
    )
    purchaseDate = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d{4}-\d{2}-\d{2}$"),
        data_key="purchaseDate"
    )
    purchaseTime = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d{2}:\d{2}$"),
        data_key="purchaseTime"
    )
    items = fields.List(
        fields.Nested(ItemSchema),
        required=True,
        validate=validate.Length(min=1)
    )
    total = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d+\.\d{2}$")
    )

class ReceiptIdSchema(ma.Schema):
    id = fields.Str(required=True)

class PointsResponseSchema(ma.Schema):
    points = fields.Int(required=True)

item_schema = ItemSchema()
receipt_schema = ReceiptSchema()
receipt_id_schema = ReceiptIdSchema()
points_response_schema = PointsResponseSchema()
