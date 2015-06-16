from framework.request_handler import YumSearchRequestHandler
from models.locations import Locations

class LocationPage(YumSearchRequestHandler):
    def get(self, location_id):
        location = Locations.get_by_id(int(location_id))

        temp_values = {
            'location'  :   location,
            'location_id' : location_id
        }
        self.render('location-page/location-page.html', **temp_values)



