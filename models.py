import json
from extensions import db

class ReceiptData(db.Model):
    __tablename__ = 'receipt_data'

    id = db.Column(db.String(36), primary_key=True)
    retailer = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.String(10), nullable=False)
    purchase_time = db.Column(db.String(5), nullable=False)
    items_json = db.Column(db.Text, nullable=False, name="items")
    total = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    @property
    def items(self):
        try:
            return json.loads(self.items_json)
        except json.JSONDecodeError:
             # Handle potential error if data is corrupted
             return []

    @items.setter
    def items(self, value):
        self.items_json = json.dumps(value)

    def __repr__(self):
        return f'<ReceiptData {self.id}>'
