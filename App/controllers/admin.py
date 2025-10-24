from App.models import Admin
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_admin(username, password):
    try:
        admin = Admin(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
        return admin.get_json(), None
    except IntegrityError:
        db.session.rollback()
        return None, 'Username already exists :('
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def schedule_shift(staff_id, shift_date, start_time, end_time, admin_id=None):
    try:
        admin = db.session.get(Admin, admin_id) if admin_id else Admin.query.first()
        if not admin or not admin.is_admin():
            return None, 'Unauthorized: Admin access required'
        
        shift = admin.schedule_shift(staff_id, shift_date, start_time, end_time)
        db.session.add(shift)  # Ensure shift is added to session
        db.session.commit()
        return shift.get_json(), None
    except ValueError as e:
        return None, str(e)
    except RuntimeError as e:
        return None, str(e)
    except IntegrityError:
        db.session.rollback()
        return None, 'Database integrity error'
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def delete_shift(shift_id, admin_id=None):
    try:
        admin = db.session.get(Admin, admin_id) if admin_id else Admin.query.first()
        if not admin or not admin.is_admin():
            return False, 'Unauthorized: Admin access required -_-'
        
        result = admin.delete_shift(shift_id)
        db.session.commit()
        return result, None
    except RuntimeError as e:
        return False, str(e)
    except IntegrityError:
        db.session.rollback()
        return False, 'Database integrity error'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def get_staff_shifts(staff_id, start_date, end_date, admin_id=None):
    try:
        admin = db.session.get(Admin, admin_id) if admin_id else Admin.query.first()
        if not admin or not admin.is_admin():
            return None, 'Unauthorized: Admin access required -_-'
        
        shifts = admin.get_staff_shifts(staff_id, start_date, end_date)
        return [shift.get_json() for shift in shifts], None
    except Exception as e:
        return None, str(e)

def generate_report(week_start, week_end, admin_id=None):
    try:
        admin = db.session.get(Admin, admin_id) if admin_id else Admin.query.first()
        if not admin or not admin.is_admin():
            return None, 'Unauthorized: Admin access required -_-'
        
        report = admin.generate_report(week_start, week_end)
        return report, None
    except Exception as e:
        return None, str(e)