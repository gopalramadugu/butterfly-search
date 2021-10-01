import operator
import flask
from flask_resty import (
    ColumnFilter,
    Filtering,
    PagePagination,
    GenericModelView,
    FixedSorting,
)
from . import models, schemas, app
import datetime

# ---------------------------------------------------------------------
# Base class for HTTP POST and GET methods that defines schema, model and overrides the framework method for saving an item
# ---------------------------------------------------------------------
class SearchViewBase(GenericModelView):
    model = models.Search
    schema = schemas.SearchSchema()
    args_schema = schemas.SearchQuerySchema()

    def create_item_raw(self, data):
        data["createdby"] = self.request_args.get("appuserid")
        data["updatedby"] = self.request_args.get("appuserid")
        data["isdeleted"] = False
        data["createddate"] = datetime.datetime.now(datetime.timezone.utc)
        data["updateddate"] = datetime.datetime.now(datetime.timezone.utc)

        return super().create_item_raw(data)


# ---------------------------------------------------------------------
# Base class for HTTP DELETE method that defines schema, model and overrides the framework method for deleting an item
# ---------------------------------------------------------------------
class SearchDeleteViewBase(GenericModelView):
    model = models.Search
    schema = schemas.SearchSchema()
    args_schema = schemas.SearchQuerySchema()

    def delete_item(self, item):
        if item.isdeleted:
            flask.abort(404)

        super().delete_item(item)

    def delete_item_raw(self, item):
        item.isdeleted = True
        item.updatedby = self.request_args.get("appuserid")
        item.updateddate = datetime.datetime.now(datetime.timezone.utc)


# ---------------------------------------------------------------------
# Base class for HTTP PATCH method that defines schema, model
# ---------------------------------------------------------------------


class SearchUpdateBase(GenericModelView):
    model = models.Search
    schema = schemas.SearchUpdateSchema()
    args_schema = schemas.SearchQuerySchema()

    def update_item_raw(self, item, data):
        data["updatedby"] = self.request_args.get("appuserid")
        data["isdeleted"] = False
        data["updateddate"] = datetime.datetime.now(datetime.timezone.utc)
        super().update_item_raw(item, data)


# ---------------------------------------------------------------------
# Class that handles search HTTP GET and POST methods
# ---------------------------------------------------------------------


class SearchListView(SearchViewBase):
    SEARCH_TYPE_SAVED = "saved"
    SEARCH_TYPE_RECENT = "recent"
    SEARCH_NAME_KEY = "name"
    DEFAULT_QUERY_LIMIT = 3

    def get(self):
        try:
            data = self.request_args
            searchtype = data.get("searchtype")
            filteredsearchs = []
            if data.get("limit") is not None:
                limit = int(data.get("limit"))
            else:
                limit = self.DEFAULT_QUERY_LIMIT

            if not searchtype:
                self.filtering = Filtering(
                    appuserid=ColumnFilter(operator.eq, required=True),
                    isdeleted=ColumnFilter(operator.eq, required=False),
                )
            else:
                self.filtering = Filtering(
                    appuserid=ColumnFilter(operator.eq, required=True),
                    searchtype=ColumnFilter(operator.eq, required=False),
                    isdeleted=ColumnFilter(operator.eq, required=False),
                )

            self.sorting = FixedSorting("-updateddate,-id")
            self.pagination = PagePagination(page_size=limit)
            searches = self.get_list()

            for search in searches:
                if search.isdeleted != True:
                    filteredsearchs.append(search)

            return self.make_items_response(filteredsearchs)
        except Exception as e:
            app.logger.exception("Exception on get search: ", e.message)

    def post(self):
        try:
            querydata = self.request_args
            data = self.get_request_data()
            searchtype = querydata.get("searchtype")
            appuserid = querydata.get("appuserid")

            if appuserid != data["appuserid"]:
                return {"message": "appuserid in query and body dont match"}, 200

            if searchtype != data["searchtype"]:
                return {"message": "Searchtype in query and body dont match"}, 200

            if searchtype == self.SEARCH_TYPE_SAVED and (
                self.SEARCH_NAME_KEY not in data or not data["name"]
            ):
                return {"message": "Please specify a name for a saved search"}, 200

            if (
                searchtype == self.SEARCH_TYPE_RECENT
                or searchtype == self.SEARCH_TYPE_SAVED
            ):
                self.filtering = Filtering(
                    appuserid=ColumnFilter(operator.eq, required=True),
                    searchtype=ColumnFilter(operator.eq, required=False),
                )
            else:
                return {
                    "message": "Invalid searchtype. Valid types are recent, saved"
                }, 200

            searches = self.get_list()

            if not searches:
                return self.create()
            else:
                for search in searches:
                    if (
                        searchtype == self.SEARCH_TYPE_RECENT
                        and search.searchcriteria == data["searchcriteria"]
                    ) or (
                        searchtype == self.SEARCH_TYPE_SAVED
                        and search.name == data["name"]
                    ):
                        return {
                            "message": "Search could not be created. It already exists"
                        }, 200
            return self.create()
        except:
            app.logger.exception("Exception on creating search: ")


# ---------------------------------------------------------------------
# Class that handles search HTTP DELETE method
# ---------------------------------------------------------------------


class SearchDeleteView(SearchDeleteViewBase):
    def delete(self, id):
        try:
            return self.destroy(id)
        except:
            app.logger.exception("Exception on deleting search: ")


# ---------------------------------------------------------------------
# Class that handles search HTTP PATCH method
# ---------------------------------------------------------------------


class SearchUpdateView(SearchUpdateBase):
    def patch(self, id):
        try:
            data = self.get_request_data()
            querydata = self.request_args
            appuseridquery = querydata.get("appuserid")

            if appuseridquery != data["appuserid"]:
                return {"message": "appuserid in query and body doesnt match"}, 200

            self.filtering = Filtering(
                appuserid=ColumnFilter(operator.eq, required=True),
                id=ColumnFilter(operator.eq, required=False),
            )
            searches = self.get_list()

            if not searches:
                return {
                    "message": "No existing search found. Please save the search the first before updating it."
                }, 200
            else:
                for search in searches:
                    if search.name is not None and search.name == data["name"]:
                        return {
                            "message": "Search could not be updated. It already exists"
                        }, 200

            return self.update(id, partial=True)
        except:
            app.logger.exception("Exception on updating search: ")
