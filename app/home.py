from framework.request_handler import YumSearchRequestHandler
from models.locations import Locations

class Home(YumSearchRequestHandler):
	def get(self):
            suggestions = Locations.get_suggestions()
            tmp_values = {
                'suggestions' : suggestions
            }
            self.render('home/home.html', **tmp_values)





