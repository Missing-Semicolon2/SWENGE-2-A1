from App.models import Shift
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_shift(shift_id):
    shift = db.session.get(Shift, shift_id)
    return shift.get_json() if shift else None

def get_all_shifts():
    shifts = db.session.scalars(db.select(Shift)).all()
    return [shift.get_json() for shift in shifts] if shifts else []

def get_shifts_by_date(start_date, end_date):
    try:
        shifts = Shift.query.filter(
            Shift.date.between(start_date, end_date)
        ).order_by(Shift.date, Shift.start_time).all()
        return [shift.get_json() for shift in shifts], None
    except Exception as e:
        return None, str(e)