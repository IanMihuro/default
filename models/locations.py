from google.appengine.ext import ndb
from google.appengine.api import search

class Locations(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    parsed = ndb.BooleanProperty()
    source_url = ndb.StringProperty()
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    image_key = ndb.BlobKeyProperty()
    image_url = ndb.StringProperty()
    price = ndb.StringProperty()
    date = ndb.StringProperty()
    posted = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_new_location(cls, title, description, image_key, image_url, price, date, user_key=None, source_url=None):
        parsed = True
        user_id = ''

        if user_key:
            parsed = False
            user_id = str(user_key.id())

        location_key = cls(
            user = user_key,
            parsed = parsed,
            source_url = source_url,
            title = title,
            description = description,
            image_key = image_key,
            image_url = image_url,
            price = price,
            date =  date
        ).put()

        index = search.Index('locations') #name of search index
        doc = search.Document(
            doc_id=str(location_key.id()),
            fields=[
                search.TextField(name='user_id', value=user_id),
                search.AtomField(name='parsed', value='1' if parsed else '0'),
                search.TextField(name='title', value=title),
                search.TextField(name='description', value=description),
                search.TextField(name='image_url', value=image_url),
                search.TextField(name='price', value=price),
                search.TextField(name='date', value=date),
            ]


        )
        index.put(doc)

    @classmethod
    def get_all_locations_by_user(cls, user_id):
        index = search.Index('locations')

        query = 'user_id:(%s)' % user_id
        results = index.search(query)

        return results.results

    @classmethod
    def get_suggestions(cls):
        index = search.Index('locations')
        query = ''
        results = index.search(query)
        return results.results

    @classmethod
    def get_specific_location(cls, location_id):
        index = search.Index('locations')
        query = 'location_id:(%s)' & location_id
        results = index.search(query)
        return results.results







