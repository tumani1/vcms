# coding: utf-8
from models.locations import Cities
from models.users import Users
from models.users.constants import APP_USERS_GENDER_UNDEF
from utils.connection import get_session

import sys
import signal
import getpass

session = get_session()


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? ([y]/n)? ").lower() in ('yes', 'y', ''):
            sys.exit(1)

    except (KeyboardInterrupt, RuntimeError):
        print "\n"
        sys.exit(1)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)

# Get data to create manager
print u"Create manager: "
data = {"is_manager": True, "gender": APP_USERS_GENDER_UNDEF}
data['email'] = raw_input(u"Email: ")
data['firstname'] = raw_input(u"Name: ")
data['lastname'] = raw_input(u"Lastname: ")
data['password'] = getpass.getpass()
password2 = getpass.getpass(u"Password2: ")
if data['password'] != password2:
    raise ValueError(u"Password doesn't equal!")
# Select a city
print u"Cities: "
cities = session.query(Cities.id, Cities.name)
for city in cities.all():
    print u"{0}. {1}".format(city.id, city.name)
city_id = int(raw_input(u"Pleas, enter numer of citie: "))
if city_id in [city.id for city in cities]:
    data['city_id'] = city_id
else:
    print "Not valid city ID"
    sys.exit(1)
# Create User object
try:
    user = Users(**data)
    session.add(user)
    session.commit()
    session.close()
    print "Manager is created"
except Exception as e:
    print "An error has occurred"
    print e
