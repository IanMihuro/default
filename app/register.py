from framework.request_handler import YumSearchRequestHandler
from models.users import Users
from google.appengine.api import mail
from os import environ
import re

class RegisterUser(YumSearchRequestHandler):
    @classmethod
    def send_email(cls, to, user_id, confirmation_code):
        #Send Register Confirmation Email.
        email_object=mail.EmailMessage(
            sender='noreply@likizo-1.appspotmail.com',
            subject='Confirm your Likizo account',
            to=to
            )

        email_parameters = {
            'domain' : 'http://localhost:59080' if environ['SERVER_SOFTWARE'].startswith('Development') else 'http://likizo-1.appspot.com',
            'user_id' : user_id,
            'confirmation_code' : confirmation_code
        }
        html_from_template = cls.jinja2_environment.get_template('email/confirmation_email.html').render(email_parameters)
        email_object.html = html_from_template
        email_object.send()


    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')

        status = 200
        json_response = {}

        if name and email and password:
            #Success
            email_validation_pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.match(email_validation_pattern, email):
                user = Users.add_new_user(name, email, password)#saving to Users database

                if user['created']:
                    html = self.jinja2_environment.get_template('commons/register_modal_success.html').render()
                    json_response = {
                        'html' : html #send the html
                    }

                    self.send_email(to=email, user_id=user['user_id'], confirmation_code=['confirmation_code'])

                else:
                    status = 400
                    json_response = user
            else:
                status = 400
                json_response = {
                    'created'   :   False,
                    'title' :   'The email is not valid',
                    'message'   :   'Please enter a valid email address.'
                }

        else:
            #Fail
            status = 400
            json_response = {}

            if not name:
                json_response.update({
                    'title': 'The name field is required',
                    'message': 'Please fill in the name in order to continue'
                })
            if not email:
                json_response.update({
                    'title': 'The email field is required',
                    'message': 'Please fill in your email in order to continue'
                })
            if not password:
                json_response.update({
                    'title': 'The password field is required',
                    'message': 'Please fill in the password in order to continue'
                })

        self.json_response(status_code=status, **json_response)









