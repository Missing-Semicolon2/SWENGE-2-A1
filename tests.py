import unittest
from App.controllers.staff import clock_in, clock_out, create_staff
from App.controllers.admin import schedule_shift

# UNIT TESTS

class UsersIntegrationTests(unittest.TestCase):

    def test_new_staff(self):
        staff = staff.Staff("andrew", "andrewPass")
        return staff
    
    def test_clock_in(self):
        staffid = "012345"
        result = clock_in(staffid)
        return result
    
    def test_clock_out(self):
        staffid = "012345"
        result = clock_out(staffid)
        return result
    


# INTEGRATION TESTS

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user():
        staff = create_staff("andrew", "andrewPass")
        return staff
    
    def test_schedule_shift():
        staffid = "012345"
        shiftDate = "10102020"
        startTime = "08"
        endTime = "14"
        tempShift = schedule_shift(staffid, shiftDate, startTime, endTime)
        return tempShift
    
    def test_shiftDuration_calc():
        staffid = "012345"
        result = clock_in(staffid) - clock_out(staffid)
        return result