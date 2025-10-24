from App.database import db
from App.models.user import User
from App.models.shift import Shift
from datetime import date

class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    def schedule_shift(self, staff_id, shift_date, start_time, end_time):
        from App.models.staff import Staff
        
        staff = Staff.query.get(staff_id)
        if not staff or staff.role != 'staff':
            raise ValueError('Invalid staff member')
        
        if shift_date <= date.today():
            raise ValueError('Can only schedule future shifts')
        
        new_shift = Shift(
            staff_id=staff_id,
            date=shift_date,
            start_time=start_time,
            end_time=end_time
        )
        
        conflicts = Shift.query.filter(
            Shift.staff_id == staff_id,
            Shift.date == shift_date
        ).all()
        
        for other in conflicts:
            if new_shift.overlaps(other):
                raise RuntimeError(f'Shift conflicts with existing shift: {other.id}')
        
        db.session.add(new_shift)
        return new_shift

    def delete_shift(self, shift_id):
        shift = Shift.query.get(shift_id)
        if not shift:
            return False
        
        if shift.is_started:
            raise RuntimeError('Cannot delete a shift that has already started')
        
        db.session.delete(shift)
        return True

    def get_staff_shifts(self, staff_id, start_date, end_date):
        return Shift.query.filter(
            Shift.staff_id == staff_id,
            Shift.date.between(start_date, end_date)
        ).order_by(Shift.date, Shift.start_time).all()

    def generate_report(self, week_start, week_end):
        shifts = Shift.query.filter(
            Shift.date.between(week_start, week_end)
        ).all()
        
        report = {}
        for shift in shifts:
            username = shift.staff.username
            if username not in report:
                report[username] = {'total_hours': 0, 'shift_count': 0}
            
            if shift.actual_duration_hours:
                report[username]['total_hours'] += shift.actual_duration_hours
            report[username]['shift_count'] += 1
        
        return report