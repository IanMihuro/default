from google.appengine.ext import ndb
from google.appengine.api import search
from models.users import Users
from models.locations import Locations

class Booking(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    location_id = ndb.StringProperty()
    price = ndb.StringProperty()
    numbers = ndb.StringProperty()
    date_booked = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_user_booking(cls,user, price, numbers, location_id):

        booking_key = cls(
            user=user,
            price=price,
            numbers=numbers,
            location_id=location_id,
        ).put()

