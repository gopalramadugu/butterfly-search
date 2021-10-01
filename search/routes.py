from flask_resty import Api
from . import app, views

api = Api(app, prefix="/api")
api.add_resource("/search/", views.SearchListView)
api.add_resource("/search/<int:id>", views.SearchDeleteView)
api.add_resource("/search/update/<int:id>", views.SearchUpdateView)
