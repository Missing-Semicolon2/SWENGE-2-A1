import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from datetime import datetime, date, time

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="staff")
def create_user_command(username, password, role):
    create_user(username, password, role)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Staff Commands
'''

staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Create a staff member")
@click.argument("username", default="staff0")
@click.argument("password", default="staffpass")
def create_staff_command(username, password):
    staff = Staff(username=username, password=password, role='staff')
    db.session.add(staff)
    db.session.commit()
    print(f'Staff {username} created!')

# Note original CLI commands for clock in and clock out, directly call the model methods, therefore, they must be updated to utilize the controller instead, for view implementation
@staff_cli.command("clock-in", help="Clock in for current shift")
@click.argument("username")
def staff_clock_in_command(username):
    staff = Staff.query.filter_by(username=username).first()
    if not staff:
        print(f"Staff member {username} not found")
        return
    try:
        result = staff.clock_in() # direct call of method in model
        print(result)
    except Exception as e:
        print(f"Error: {e}")

@staff_cli.command("clock-out", help="Clock out of current shift")
@click.argument("username")
def staff_clock_out_command(username):
    staff = Staff.query.filter_by(username=username).first()
    if not staff:
        print(f"Staff member {username} not found")
        return
    try:
        result = staff.clock_out() # direct call of method in model
        print(result)
    except Exception as e:
        print(f"Error: {e}")

@staff_cli.command("view-roster", help="View combined roster of all staff shifts for date range")
@click.argument("username")
@click.argument("start_date")
@click.argument("end_date")
def staff_view_roster_command(username, start_date, end_date):
    staff = Staff.query.filter_by(username=username).first()
    if not staff:
        print(f"Staff member {username} not found")
        return
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        
        # Get all shifts for all staff in the date range
        shifts = Shift.query.filter(
            Shift.date.between(start, end)
        ).order_by(Shift.date, Shift.start_time).all()
        
        if not shifts:
            print("No shifts found for the given date range")
            return
        
        # Group shifts by date for better organization
        shifts_by_date = {}
        for shift in shifts:
            shift_date = shift.date.isoformat()
            if shift_date not in shifts_by_date:
                shifts_by_date[shift_date] = []
            shifts_by_date[shift_date].append(shift)
        
        print(f"Combined Roster for {start} to {end}:")
        print("=" * 60)
        
        for shift_date, date_shifts in sorted(shifts_by_date.items()):
            print(f"\n{shift_date}:")
            print("-" * 40)
            for shift in date_shifts:
                staff_name = shift.staff.username
                status_icon = "🟢" if shift.status == 'completed' else "🟡" if shift.status == 'in_progress' else "⚪"
                clock_info = ""
                if shift.clock_in_at:
                    clock_info = f" | Clocked: {shift.clock_in_at.strftime('%H:%M')}"
                    if shift.clock_out_at:
                        clock_info += f" - {shift.clock_out_at.strftime('%H:%M')}"
                
                print(f"  {status_icon} {staff_name:15} {shift.start_time}-{shift.end_time} {clock_info}")
                
    except Exception as e:
        print(f"Error: {e}")

app.cli.add_command(staff_cli)

'''
Admin Commands
'''

admin_cli = AppGroup('admin', help='Admin object commands')

@admin_cli.command("create", help="Create an admin user")
@click.argument("username", default="admin0")
@click.argument("password", default="adminpass")
def create_admin_command(username, password):
    admin = Admin(username=username, password=password, role='admin')
    db.session.add(admin)
    db.session.commit()
    print(f'Admin {username} created!')

@admin_cli.command("schedule-shift", help="Schedule a shift for staff")
@click.argument("staff_username")
@click.argument("shift_date")
@click.argument("start_time")
@click.argument("end_time")
def admin_schedule_shift_command(staff_username, shift_date, start_time, end_time):
    staff = Staff.query.filter_by(username=staff_username).first()
    if not staff:
        print(f"Staff member {staff_username} not found")
        return
    
    admin = Admin.query.first()  # Get first admin user
    if not admin:
        print("No admin user found")
        return
    
    try:
        shift_date_obj = date.fromisoformat(shift_date)
        start_time_obj = time.fromisoformat(start_time)
        end_time_obj = time.fromisoformat(end_time)
        
        shift = admin.schedule_shift(staff.id, shift_date_obj, start_time_obj, end_time_obj)
        print(f"Shift scheduled: {shift}")
    except Exception as e:
        print(f"Error: {e}")


@admin_cli.command("delete-shift", help="Delete a shift")
@click.argument("shift_id")
def admin_delete_shift_command(shift_id):
    admin = Admin.query.first()
    if not admin:
        print("No admin user found")
        return
    
    try:
        result = admin.delete_shift(int(shift_id))
        if result:
            print(f"Shift {shift_id} deleted successfully")
        else:
            print(f"Shift {shift_id} not found")
    except Exception as e:
        print(f"Error: {e}")

@admin_cli.command("generate-report", help="Generate shift report for date range")
@click.argument("start_date")
@click.argument("end_date")
def admin_generate_report_command(start_date, end_date):
    admin = Admin.query.first()
    if not admin:
        print("No admin user found")
        return
    
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        report = admin.generate_report(start, end)
        
        print(f"Shift Report for {start} to {end}:")
        print("-" * 50)
        for username, data in report.items():
            print(f"{username}:")
            print(f"  Total Shifts: {data['shift_count']}")
            print(f"  Total Hours: {data['total_hours']:.2f}")
            print()
    except Exception as e:
        print(f"Error: {e}")

@admin_cli.command("list-shifts", help="List all shifts for a staff member")
@click.argument("staff_username")
@click.argument("start_date")
@click.argument("end_date")
def admin_list_shifts_command(staff_username, start_date, end_date):
    staff = Staff.query.filter_by(username=staff_username).first()
    if not staff:
        print(f"Staff member {staff_username} not found")
        return
    
    admin = Admin.query.first()
    if not admin:
        print("No admin user found")
        return
    
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        shifts = admin.get_staff_shifts(staff.id, start, end)
        
        print(f"Shifts for {staff_username} from {start} to {end}:")
        print("-" * 50)
        for shift in shifts:
            status = shift.status
            clock_in = shift.clock_in_at.strftime("%H:%M") if shift.clock_in_at else "Not started"
            clock_out = shift.clock_out_at.strftime("%H:%M") if shift.clock_out_at else "Not ended"
            print(f"Shift {shift.id}: {shift.date} {shift.start_time}-{shift.end_time}")
            print(f"  Status: {status}, Clock In: {clock_in}, Clock Out: {clock_out}")
            print()
    except Exception as e:
        print(f"Error: {e}")

app.cli.add_command(admin_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)