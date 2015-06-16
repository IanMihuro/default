from webapp2 import WSGIApplication
from webapp2 import Route

app = WSGIApplication(
	routes = [
		Route('/', handler='app.home.Home'),
        Route('/register', handler='app.register.RegisterUser'),
        Route('/account/<user_id:[0-9]+>/confirm/<confirmation_code:[a-z0-9]{32}>', handler='app.login.LoginUser'),
        Route('/login/agent', handler='app.login.LoginAgent'),#user_id
        Route('/login', handler='app.login.LoginUser'),
        Route('/login/<location_id:[0-9]+>', handler='app.login.LoginUserPackage'),
        Route('/account', handler='app.account.UserAccount'),
        Route('/account/new-location', handler='app.account.PostLocation'),
        Route('/search', handler='app.serp.SearchLocations'),
        Route('/location/<location_id:[0-9]+>', handler='app.location.LocationPage'),
        Route('/book/<location_id:[0-9]+>', handler='app.booking.BookTrip'),

	]


)