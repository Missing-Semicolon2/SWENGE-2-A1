from App.models import Staff, Shift
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_staff(username, password):
    try:
        staff = Staff(username=username, password=password)
        db.session.add(staff)
        db.session.commit()
        return staff.get_json(), None
    except IntegrityError:
        db.session.rollback()
        return None, 'Username already exists'
    except Exception as e:
        db.session.rollback()
        return None, str(e)
    
# Note original CLI commands for clock in and clock out, directly call the model methods, therefore, they must be updated to utilize the controller instead for the views implementation
def clock_in(staff_id):
    try:
        staff = db.session.get(Staff, staff_id)
        if not staff or not staff.is_staff():
            return None, 'Unauthorized: Staff access required'
        
        result = staff.clock_in()
        db.session.commit()
        return result, None
    except (ValueError, RuntimeError) as e:
        return None, str(e)
    except IntegrityError:
        db.session.rollback()
        return None, 'Database integrity error'
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def clock_out(staff_id):
    try:
        staff = db.session.get(Staff, staff_id)
        if not staff or not staff.is_staff():
            return None, 'Unauthorized: Staff access required'
        
        result = staff.clock_out()
        db.session.commit()
        return result, None
    except (ValueError, RuntimeError) as e:
        return None, str(e)
    except IntegrityError:
        db.session.rollback()
        return None, 'Database integrity error'
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def view_roster(staff_id, week_start, week_end):
    try:
        staff = db.session.get(Staff, staff_id)
        if not staff or not staff.is_staff():
            return None, 'Unauthorized: Staff access required'
        
        shifts = staff.view_roster(week_start, week_end)
        return [shift.get_json() for shift in shifts], None
    except Exception as e:
        return None, str(e)

def get_combined_roster(start_date, end_date):
    try:
        shifts = Shift.query.filter(
            Shift.date.between(start_date, end_date)
        ).order_by(Shift.date, Shift.start_time).all()
        return [shift.get_json() for shift in shifts], None
    except Exception as e:
        return None, str(e)