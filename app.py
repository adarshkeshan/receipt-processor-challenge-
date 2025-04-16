# app.py
import os
import uuid
import re
import json
from flask import Flask, request, jsonify
from marshmallow import ValidationError

from extensions import db, ma
from models import ReceiptData
from schemas import receipt_schema, receipt_id_schema, points_response_schema
from points_calculator import calculate_points

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

db_folder = os.environ.get('DATABASE_FOLDER', os.path.join(basedir, 'data'))
db_path = os.path.join(db_folder, 'receipts.db')

os.makedirs(db_folder, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """Processes a receipt submission."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"description": "Request must be JSON"}), 400

    try:
        validated_data = receipt_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"description": "The receipt is invalid."}), 400

    points = calculate_points(validated_data)
    receipt_id = str(uuid.uuid4())

    new_receipt = ReceiptData(
        id=receipt_id,
        retailer=validated_data['retailer'],
        purchase_date=validated_data['purchaseDate'],
        purchase_time=validated_data['purchaseTime'],
        items=validated_data['items'],
        total=validated_data['total'],
        points=points
    )

    try:
        db.session.add(new_receipt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Database Error on Process: {e}")
        return jsonify({"description": "Internal server error during database operation."}), 500

    return jsonify(receipt_id_schema.dump({"id": receipt_id})), 200

@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    """Retrieves points for a specific receipt ID."""
    if not re.match(r"^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", receipt_id, re.IGNORECASE):
       return jsonify({"description": "Invalid receipt ID format."}), 400

    receipt = db.session.get(ReceiptData, receipt_id)

    if receipt is None:
        return jsonify({"description": "No receipt found for that ID."}), 404
    else:
        return jsonify(points_response_schema.dump({"points": receipt.points})), 200

@app.cli.command('init-db')
def init_db_command():
    db.drop_all()
    db.create_all()
    print('Initialized the database.')

@app.before_request
def ensure_tables_exist():
    if not hasattr(ensure_tables_exist, 'tables_created'):
        with app.app_context():
            db.create_all()
            ensure_tables_exist.tables_created = True

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')
