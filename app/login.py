from framework.request_handler import YumSearchRequestHandler
from models.users import Users

class LoginAgent(YumSearchRequestHandler):
    def get(self):
        self.render('login/login.html')

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        user_id = Users.check_password(email, password)

        if user_id:
            self.send_cookie(name='User', value=user_id)
            self.redirect('/account') #test, redirect to '/'
        else:
            self.redirect('/login')

class LoginUser(YumSearchRequestHandler):
    def get(self):

        self.render('login/login.html')

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        user_id = Users.check_password(email, password)

        if user_id:
            self.send_cookie(name='User', value=user_id)
            self.redirect('/')
        else:
            self.redirect('/login')



