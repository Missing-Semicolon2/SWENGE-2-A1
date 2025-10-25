def test_view_roster():
  start_date= datetime.now().date()
  end_date= start_date+timedelta(days=7)

combined_roster=get_combined_roster(start_date, end_date)

if not combined_roster:
  print ("Failed combined roster!")
  return False

for entry in combined_roster:
  staff_id= entry.get("staff_id")
  shift_time= entry.get("shift_time")

  if not staff_if or not shift_time:
    print("Failed for invalid entry: staff id/shift time")
    return False

print ("Passed all test!")
return True
