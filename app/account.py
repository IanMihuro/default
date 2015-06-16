from framework.request_handler import YumSearchRequestHandler
from models.locations import Locations
from lib.cloudstorage import cloudstorage_api
from google.appengine.api import blobstore
from google.appengine.api import images


class UserAccount(YumSearchRequestHandler):

    @YumSearchRequestHandler.login_required
    def get(self):
        user_id = self.check_user_logged_in.key.id()
        locations = Locations.get_all_locations_by_user(user_id)

        tpl_values = {
            'locations' : locations
        }

        self.render('account/home.html', **tpl_values)

class PostLocation(YumSearchRequestHandler):
    @YumSearchRequestHandler.login_required
    def get(self):
        self.render('account/post_location.html')

    @YumSearchRequestHandler.login_required
    def post(self):
        user_key = self.check_user_logged_in.key
        title = self.request.get('title')
        description = self.request.get('description')
        price = self.request.get('price')
        date = self.request.get('date')
        image = self.request.POST['image']

        saved_photo = self.save_image(image, user_key)

        Locations.add_new_location(
            user_key = user_key,
            title = title,
            description = description,
            price = price,
            date = date,
            image_key=saved_photo['blobstore_key'],
            image_url=saved_photo['serving_url'],


        )
        self.redirect('/account')


    @classmethod
    def save_image(cls, photo, user_key):
        img_title = photo.filename
        img_content = photo.file.read()
        img_type = photo.type

        cloud_storage_path = '/gs/likizo-images/%s/%s' %(user_key.id(), img_title)
        blobstore_key = blobstore.create_gs_key(cloud_storage_path)

        cloud_storage_file = cloudstorage_api.open(
            filename=cloud_storage_path[3:], mode='w', content_type=img_type
        )
        cloud_storage_file.write(img_content)
        cloud_storage_file.close()

        blobstore_key = blobstore.BlobKey(blobstore_key)
        serving_url = images.get_serving_url(blobstore_key)

        return {
            'serving_url' : serving_url,
            'blobstore_key' : blobstore_key
        }









