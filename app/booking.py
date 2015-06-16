from framework.request_handler import YumSearchRequestHandler
from models.locations import Locations
from models.users import Users
from models.userBookings import Booking
from google.appengine.api import mail
from os import environ

class BookTrip(YumSearchRequestHandler):
    @classmethod
    def BookingEmail(cls, to, user_id, location_id):
        #Send Booking Confirmation Email
        link = "http://likizo-1.appspot.com/location/"+location_id

        email_object=mail.EmailMessage(
            sender='noreply@likizo-1.appspotmail.com',
            subject='Confirm your Holiday Package',
            to=to
            )

        email_parameters = {
            'domain' : 'http://localhost:59080' if environ['SERVER_SOFTWARE'].startswith('Development') else 'http://likizo-1.appspot.com',
            'user_id' : user_id,
            'link' : link,
        }
        html_from_template = cls.jinja2_environment.get_template('email/confirm_booking_email.html').render(email_parameters)
        email_object.html = html_from_template
        email_object.send()



    @YumSearchRequestHandler.login_required
    def get(self, location_id):

        package = Locations.get_by_id(int(location_id))
        user_id = self.check_user_logged_in.key.id()


        temp_values = {
            'package' : package,
            'location_id'   : location_id,

        }
        self.render('/book/book-package.html', **temp_values)

    @YumSearchRequestHandler.login_required
    def post(self, location_id):
        user_id = self.check_user_logged_in.key
        price = self.request.get('price')
        numbers = self.request.get('numbers')

        email = Users.check_email(user_id)

        Booking.add_user_booking(
            user=user_id,
            price=price,
            numbers=numbers,
            location_id=location_id
        )
        #send Email
        to = Users.check_email(user_id)


        self.BookingEmail(to=to, user_id=user_id, location_id=location_id)
        self.render('/success/success.html')








