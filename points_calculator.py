# points_calculator.py
import math
from datetime import datetime

def calculate_points(receipt_data):
    points = 0
    retailer_name = receipt_data.get('retailer', '')
    points += sum(c.isalnum() for c in retailer_name)

    total_str = receipt_data.get('total', '0.00')
    try:
        total_float = float(total_str)
    except ValueError:
        total_float = 0.0

    if total_float.is_integer() and total_float > 0:
        points += 50

    if total_float > 0 and (abs(total_float % 0.25) < 1e-9 or abs((total_float % 0.25) - 0.25) < 1e-9) :
        points += 25

    items = receipt_data.get('items', [])
    points += (len(items) // 2) * 5

    for item in items:
        description = item.get('shortDescription', '').strip()
        if len(description) > 0 and len(description) % 3 == 0:
            try:
                price_float = float(item.get('price', '0.00'))
                points += math.ceil(price_float * 0.2)
            except ValueError:
                continue # Skip item if price is invalid

    purchase_date_str = receipt_data.get('purchaseDate', '')
    try:
        purchase_dt = datetime.strptime(purchase_date_str, '%Y-%m-%d')
        if purchase_dt.day % 2 != 0:
            points += 6
    except ValueError:
        pass

    purchase_time_str = receipt_data.get('purchaseTime', '')
    try:
        purchase_tm = datetime.strptime(purchase_time_str, '%H:%M').time()
        time_1400 = datetime.strptime('14:00', '%H:%M').time()
        time_1600 = datetime.strptime('16:00', '%H:%M').time()
        if time_1400 < purchase_tm < time_1600:
            points += 10
    except ValueError:
         pass

    return points
