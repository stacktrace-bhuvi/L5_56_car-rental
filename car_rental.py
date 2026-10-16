"""Car rental booking system with static analysis fixes."""

import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import tempfile
from datetime import datetime

# Global rental state
FLEET = {}
BOOKINGS = []
CONN = sqlite3.connect(":memory:")
CONN.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")


def is_valid_plate(plate):
    """Validate vehicle registration number format."""
    return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate))


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car to the fleet with validation."""
    if not is_valid_plate(plate):
        raise ValueError(f"Invalid license plate format: {plate}")
    if daily_rate < 0:
        raise ValueError("Daily rate cannot be negative")
    car_features = list(features) if features is not None else []
    FLEET[plate] = {"model": model, "rate": daily_rate, "available": True, "features": car_features}
    return FLEET[plate]


def register_customer(name, licence, phone):
    """Register a new customer using parameterized query."""
    CONN.execute("INSERT INTO customers VALUES (?, ?, ?)", (name, licence, phone))


def find_customer(name):
    """Find customers by name using parameterized query."""
    query = "SELECT * FROM customers WHERE name = ?"
    return CONN.execute(query, (name,)).fetchall()


def booking_code():
    """Generate a secure random booking code."""
    return f"BK-{secrets.randbelow(90000) + 10000}"


def licence_hash(licence):
    """Return SHA-256 hash of a driving licence."""
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(percent_off, amount):
    """Apply discount percentage to amount."""
    if not 0 <= percent_off <= 100:
        raise ValueError("Discount percentage must be between 0 and 100")
    return amount * (100 - percent_off) / 100


def rent_car(plate, customer, start, end):
    """Rent a car to a customer for a given date range."""
    if not find_customer(customer):
        raise ValueError("Customer not registered")
    if plate not in FLEET:
        raise KeyError(f"Car with plate '{plate}' not found in fleet")
    if not FLEET[plate]["available"]:
        raise ValueError(f"Car with plate '{plate}' is not available")
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    if end_dt <= start_dt:
        raise ValueError("End date must be after start date")
    days = (end_dt - start_dt).days
    cost = days * FLEET[plate]["rate"]
    FLEET[plate]["available"] = False
    code = booking_code()
    BOOKINGS.append(
        {"code": code, "plate": plate, "customer": customer, "days": days, "cost": cost}
    )
    return cost


def return_car(plate, km_driven):
    """Process car return, update availability, and compute extra charges."""
    if plate not in FLEET:
        raise KeyError(f"Car with plate '{plate}' not found in fleet")
    FLEET[plate]["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return 0


def write_receipt(booking):
    """Write receipt to a secure temporary file and return path."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as file_obj:
        file_obj.write(
            f"Booking {booking['code']}: {booking['plate']} "
            f"for {booking['days']} days = Rs.{booking['cost']}\n"
        )
        path = file_obj.name
    os.chmod(path, 0o600)
    return path


def admin_login(user, password):
    """Verify admin login against ADMIN_PASSWORD environment variable."""
    expected_password = os.environ.get("ADMIN_PASSWORD")
    if not expected_password:
        return False
    if user == "admin" and hmac.compare_digest(password, expected_password):
        return True
    return False


def available_cars():
    """Return list of plates for all currently available cars."""
    result = []
    for plate, car in FLEET.items():
        if car["available"]:
            result.append(plate)
    return result


def main():
    """Demonstrate car rental operations and error handling."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    try:
        add_car("KA03EF9999", "Nexon", -500)
    except ValueError as exc:
        print("Add Nexon failed:", exc)

    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")

    print("Rent Swift:", rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"))
    try:
        print("Rent Swift again:", rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"))
    except ValueError as exc:
        print("Rent Swift again failed:", exc)

    try:
        print("Rent Innova:", rent_car("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"))
    except ValueError as exc:
        print("Rent Innova failed:", exc)

    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    try:
        print("Return unknown car:", return_car("XX00XX0000", 50))
    except (KeyError, ValueError) as exc:
        print("Return unknown car failed:", exc)

    print("Promo price:", apply_promo(10, 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print("Admin:", admin_login("admin", os.environ.get("ADMIN_PASSWORD", "")))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(BOOKINGS[0]))


if __name__ == "__main__":
    main()
