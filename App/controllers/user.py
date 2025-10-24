from App.models import User, Staff, Admin
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_user(username, password, role='user'):
    try:
        if role == 'staff':
            new_user = Staff(username=username, password=password)
        elif role ==- 'admin':
            new_user = Admin(username=username, password=password)
        else:
            new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.get_json()
    except IntegrityError:
        db.session.rollback()
        return None, 'Username already exists :('
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    try:
        user = get_user(id)
        if user:
            user.username = username
            # user is already in the session; no need to re-add
            db.session.commit()
            return True
        return None, 'User not found :('
    except IntegrityError:
        db.session.rollback()
        return None, 'Username already exists :('
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_staff_members():
    staff = User.query.filter_by(role='staff').all()
    return [s.get_json() for s in staff] if staff else []

def get_admins():
    admin = User.query.filter_by(role='staff').all()
    return [a.get_json() for a in admin] if admin else []