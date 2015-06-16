from framework.request_handler import YumSearchRequestHandler
from google.appengine.api import search

class SearchLocations(YumSearchRequestHandler):
    def get(self):
        query = self.request.get('q')

        if not query:
            self.redirect('/')
        else:

            index = search.Index('locations')
            snippet = 'snippet("%s", description, 140 )' % query

            options = search.QueryOptions(
                returned_expressions=[
                    search.FieldExpression(name='snippet', expression=snippet)
                ]

            )

            results = index.search(
                query=search.Query(
                    query_string=query,
                    options=options,

                )

            )

            docs = []
            if results:
                docs = results.results
            tpl_values = {
                'locations' : docs,
                'query' : query
            }
            self.render('serp/serp.html', **tpl_values)



