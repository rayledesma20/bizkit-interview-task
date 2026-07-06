"""
Equipment Rental — a small booking app.

Run it with:
    python app.py
Then open http://localhost:5000 in your browser.

Business rules:
  - A booking reserves one piece of equipment for a date range.
  - Rentals are billed *inclusively*: both the start day and the end day count.
    (A pick-up-and-return-same-day rental is therefore 1 day.)
  - You cannot book a piece of equipment for dates that overlap an existing booking.
  - Equipment that is not available (e.g. under maintenance) cannot be booked.
"""

from datetime import date
from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

EQUIPMENT = [
    {"id": 1, "name": "Canon DSLR Camera", "daily_rate": 1500.0, "status": "available"},
    {"id": 2, "name": "Cordless Drill",     "daily_rate": 480.0,  "status": "available"},
    {"id": 3, "name": "HD Projector",       "daily_rate": 900.0, "status": "maintenance"},
    {"id": 4, "name": "PA Speaker System",  "daily_rate": 1800.0, "status": "available"},
]

BOOKINGS_FILE = "bookings.json"


def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE) as f:
            return json.load(f)
    return []


def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=2)


def get_equipment(equipment_id):
    for item in EQUIPMENT:
        if item["id"] == equipment_id:
            return item
    return None


def is_bookable(item):
    return item.get("status") == "available"


# ---------------------------------------------------------------------------
# Booking logic
# ---------------------------------------------------------------------------

def parse_date(value):
    return date.fromisoformat(value)


def parse_booking_dates(data):
    """Return (from_date, to_date) or raise ValueError with a message."""
    from_raw = data.get("from_date")
    to_raw = data.get("to_date")
    if not from_raw or not to_raw:
        raise ValueError("Start and end dates are required")
    try:
        from_date = parse_date(from_raw)
        to_date = parse_date(to_raw)
    except (TypeError, ValueError):
        raise ValueError("Invalid date format") from None
    return from_date, to_date


def rental_days(from_date, to_date):
    """Number of days a rental covers."""
    return (to_date - from_date).days + 1


def dates_overlap(start_a, end_a, start_b, end_b):
    """True if date range A overlaps date range B."""
    return not (end_a < start_b or end_b < start_a)


def find_conflicting_booking(equipment_id, from_date, to_date, bookings):
    """Return an existing booking that clashes with this one, or None."""
    for booking in bookings:
        if booking["equipment_id"] != equipment_id:
            continue
        if booking.get("status") == "cancelled":
            continue
        if dates_overlap(
            from_date,
            to_date,
            parse_date(booking["from_date"]),
            parse_date(booking["to_date"]),
        ):
            return booking
    return None


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/equipment")
def list_equipment():
    return jsonify(EQUIPMENT)


@app.route("/api/bookings")
def list_bookings():
    return jsonify(load_bookings())


@app.route("/api/availability")
def availability():
    from_raw = request.args.get("from")
    to_raw = request.args.get("to")
    if not from_raw or not to_raw:
        return jsonify({"error": "Start and end dates are required"}), 400
    try:
        from_date = parse_date(from_raw)
        to_date = parse_date(to_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid date format"}), 400
    if to_date < from_date:
        return jsonify({"error": "End date cannot be before start date"}), 400

    bookings = load_bookings()

    available = []
    for item in EQUIPMENT:
        if not is_bookable(item):
            continue
        conflict = find_conflicting_booking(item["id"], from_date, to_date, bookings)
        if conflict is None:
            available.append(item)
    return jsonify(available)


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(force=True)

    equipment = get_equipment(data.get("equipment_id"))
    if equipment is None:
        return jsonify({"error": "Unknown equipment"}), 400
    if not is_bookable(equipment):
        return jsonify({"error": f"{equipment['name']} is not available for booking"}), 400

    try:
        from_date, to_date = parse_booking_dates(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if to_date < from_date:
        return jsonify({"error": "End date cannot be before start date"}), 400

    customer = (data.get("customer") or "").strip()
    if not customer:
        return jsonify({"error": "Customer name is required"}), 400

    bookings = load_bookings()
    conflict = find_conflicting_booking(equipment["id"], from_date, to_date, bookings)
    if conflict is not None:
        return jsonify({
            "error": f"{equipment['name']} is already booked from "
                     f"{conflict['from_date']} to {conflict['to_date']}"
        }), 409

    days = rental_days(from_date, to_date)
    total = equipment["daily_rate"] * days

    booking = {
        "id": (max([b["id"] for b in bookings]) + 1) if bookings else 1,
        "equipment_id": equipment["id"],
        "equipment_name": equipment["name"],
        "customer": customer,
        "from_date": data["from_date"],
        "to_date": data["to_date"],
        "total": total,
        "status": "confirmed",
    }
    bookings.append(booking)
    save_bookings(bookings)
    return jsonify(booking), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
