def test_create_user():
  username= "Andrew"
  role= "staff"
  password= "andrewPass"
  user= create_user(username, password, role)

if not user:
  print("Failed creation!")
  return False;

if user.get("username")!= username:
  print("Failed username!")
  return False

if user.get(password)!= password:
  print("Failed password!")
  return False

if user.get("staff_id")!= staff_id:
  print("Failed ID!")
  return False

print ("User successfully created!")
return True
