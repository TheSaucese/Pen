from pynessus import Nessus
from pynessus.models.user import User
server = Nessus("localhost", 8834)
if server.login(User("username", "password")):
    print("Success!")
else:
    print("Fail!")