import pytest
from copy import deepcopy
import uuid
from datetime import date
from unittest.mock import ANY
from flask_resty.testing import ApiClient, assert_response, assert_shape, get_body
from search import app
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import search

SAVED_SEARCH_POST_URL = "/search/?appuserid={}&searchtype=saved"
RECENT_SEARCH_POST_URL = "/search/?appuserid={}&searchtype=recent"
INAVLID_SEARCH_POST_URL = "/search/?appuserid={}&searchtype=invalid"
SEARCH_PATCH_URL = "/search/update/{}?appuserid={}"
SEARCH_GET_URL = "/search/?appuserid={}"


@pytest.fixture(scope="session")
def db():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    database = app.extensions["sqlalchemy"].db
    database.create_all()
    return database


@pytest.fixture(autouse=True)
def clean_tables(db):
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())

    db.session.commit()
    yield
    db.session.rollback()


@pytest.fixture
def client(monkeypatch, clean_tables):
    app.config["WTF_CSRF_METHODS"] = []
    monkeypatch.setattr(app, "testing", True)
    monkeypatch.setattr(app, "test_client_class", ApiClient)
    return app.test_client()


# ---------------------------------------------------------------------
# Use this Json when creating a new search
# Make sure to update the necessary fields based on the test scenario
# ---------------------------------------------------------------------
@pytest.fixture(name="create_search_json")
def fixture_create_search_json():
    return {
        "appuserid": 4,
        "name": uuid.uuid4().hex,
        "searchtype": "saved",
        "searchcriteria": {"reviewer": "G Smith", "patientid": "123456"},
    }


# ---------------------------------------------------------------------
# Use this Json when updating a search
# Make sure to update the necessary fields based on the test scenario
# ---------------------------------------------------------------------
@pytest.fixture(name="update_search_json")
def fixture_update_search_json():
    return {"id": 4, "appuserid": 4, "name": uuid.uuid4().hex}


# ---------------------------------------------------------------------
# Test to create a unique search for a given user and validate the response
# ---------------------------------------------------------------------
def test_create_and_retrieve_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    assert int(response_data["id"]) > 0
    create_search_data["id"] = response_data["id"]
    assert_shape(response_data, create_search_data)


# ---------------------------------------------------------------------
# Test to create a search with tampered query parameters
# ---------------------------------------------------------------------
def test_create_with_tampered_data(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(int(create_search_data["appuserid"]) + 1),
        data=create_search_data,
    )
    invalid_param_response_data = get_body(response)
    assert (
        invalid_param_response_data["message"]
        == "appuserid in query and body dont match"
    )


# ---------------------------------------------------------------------
# Test to update a search with tampered query parameters
# ---------------------------------------------------------------------
def test_update_with_tampered_data(client, create_search_json, update_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    search_id = response_data["id"]

    update_search_json = deepcopy(update_search_json)
    update_search_json["name"] = uuid.uuid4().hex
    update_search_json["id"] = search_id

    update_response = client.patch(
        SEARCH_PATCH_URL.format(search_id, int(update_search_json["appuserid"]) + 1),
        data=update_search_json,
    )
    invalid_param_response_data = get_body(update_response)
    assert (
        invalid_param_response_data["message"]
        == "appuserid in query and body doesnt match"
    )


# ---------------------------------------------------------------------
#  Test to create a search with invalid type and validate the response
# ---------------------------------------------------------------------
def test_create_invalid_searchtype(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = "test"
    create_search_data["searchtype"] = "invalid"
    response = client.post(
        INAVLID_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    invalid_searchtype_response_data = get_body(response)

    assert (
        invalid_searchtype_response_data["message"]
        == "Invalid searchtype. Valid types are recent, saved"
    )


# ---------------------------------------------------------------------
# Recent/Unnamed Search: Test to create a search for a given user and validate the response
# ---------------------------------------------------------------------
def test_create_and_retrieve_recent_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = ""
    create_search_data["searchtype"] = "recent"
    response = client.post(
        RECENT_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    assert int(response_data["id"]) > 0
    create_search_data["id"] = response_data["id"]
    assert_shape(response_data, create_search_data)


# ---------------------------------------------------------------------
# Named Search: Test to pull the given X named latest searches
# ---------------------------------------------------------------------
def test_create_and_retrieve_named_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = "Name1"
    create_search_data["searchtype"] = "saved"
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    create_search_data["name"] = "Name2"
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    create_search_data["name"] = "Name3"
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    get_search_response = client.get(
        "/search/?appuserid={}&searchtype=saved&limit=2".format(
            create_search_data["appuserid"]
        )
    )
    get_search_response_data = assert_response(get_search_response, 200)

    assert len(get_search_response_data) == 2
    assert get_search_response_data[0]["name"] == "Name3"
    assert get_search_response_data[1]["name"] == "Name2"


# ---------------------------------------------------------------------
# Recent/Unnamed Search: Test to pull the given X unnamed latest searches
# ---------------------------------------------------------------------
def test_create_and_retrieve_recent_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    del create_search_data["name"]
    create_search_data["searchtype"] = "recent"
    create_search_data["searchcriteria"] = {"reviewer": "Reviewer 1"}
    response = client.post(
        RECENT_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    create_search_data["searchcriteria"] = {"reviewer": "Reviewer 2"}
    response = client.post(
        RECENT_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    create_search_data["searchcriteria"] = {"reviewer": "Reviewer 3"}
    response = client.post(
        RECENT_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    get_search_response = client.get(
        "/search/?appuserid={}&searchtype=recent&limit=2".format(
            create_search_data["appuserid"]
        )
    )
    get_search_response_data = assert_response(get_search_response, 200)

    assert len(get_search_response_data) == 2
    assert get_search_response_data[0]["searchcriteria"] == {"reviewer": "Reviewer 3"}
    assert get_search_response_data[1]["searchcriteria"] == {"reviewer": "Reviewer 2"}


# ---------------------------------------------------------------------
#  Test performs the below steps
#       Create new search for a user
#       Update the search name
#       Validate the response from update search call
# ---------------------------------------------------------------------
def test_create_and_update_search(client, create_search_json, update_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    search_id = response_data["id"]

    update_search_json = deepcopy(update_search_json)
    update_search_json["name"] = uuid.uuid4().hex
    update_search_json["id"] = search_id

    update_response = client.patch(
        SEARCH_PATCH_URL.format(search_id, create_search_data["appuserid"]),
        data=update_search_json,
    )
    update_response_data = assert_response(update_response, 200)

    assert_shape(update_response_data, update_search_json)


# ---------------------------------------------------------------------
#  Test validates saving duplicate search name is not allowed for the same user
# ---------------------------------------------------------------------
def test_create_duplicate_searchname(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    duplicate_save_response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    duplicate_save_response_data = get_body(duplicate_save_response)
    assert (
        duplicate_save_response_data["message"]
        == "Search could not be created. It already exists"
    )


# ---------------------------------------------------------------------
#  Test validates updating duplicate search name is not allowed for the same user
# ---------------------------------------------------------------------
def test_update_duplicate_searchname(client, create_search_json, update_search_json):
    # Saving the first unique search for the user
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    search_id = response_data["id"]

    # Updating the first search to a different name
    update_search_json = deepcopy(update_search_json)
    update_search_json["name"] = uuid.uuid4().hex
    update_search_json["id"] = search_id
    update_search_json["appuserid"] = response_data["appuserid"]
    update_response = client.patch(
        SEARCH_PATCH_URL.format(search_id, create_search_data["appuserid"]),
        data=update_search_json,
    )
    assert_response(update_response, 200)

    # Saving the second unique search for the user
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    search_id = response_data["id"]

    # Updating the second search to the previosuly used search name for the same user
    update_search_json["id"] = search_id
    update_duplicate_name_response = client.patch(
        SEARCH_PATCH_URL.format(search_id, create_search_data["appuserid"]),
        data=update_search_json,
    )
    update_duplicate_name_response_data = get_body(update_duplicate_name_response)
    assert (
        update_duplicate_name_response_data["message"]
        == "Search could not be updated. It already exists"
    )


# ---------------------------------------------------------------------
#  Test validates update of no exsisting search
# ---------------------------------------------------------------------
def test_update_no_exsisting_search(client, create_search_json, update_search_json):

    # Updating the first search to a different name
    update_search_json = deepcopy(update_search_json)
    update_search_json["name"] = uuid.uuid4().hex
    update_search_json["id"] = 1
    update_search_json["appuserid"] = 2
    update_response = client.patch(
        SEARCH_PATCH_URL.format(1, 2),
        data=update_search_json,
    )
    update_response_data = get_body(update_response)
    assert (
        update_response_data["message"]
        == "No existing search found. Please save the search the first before updating it."
    )


# ---------------------------------------------------------------------
#  Test to get the search list - Named
# ---------------------------------------------------------------------
def test_get_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    assert_response(response, 201)

    get_search_response = client.get(
        SEARCH_GET_URL.format(create_search_data["appuserid"])
    )
    get_search_response_data = assert_response(get_search_response, 200)

    exists = False
    for search_result in get_search_response_data:
        if (
            search_result["appuserid"] == create_search_data["appuserid"]
            and search_result["name"] == create_search_data["name"]
        ):
            exists = True
            break
    assert exists


# ---------------------------------------------------------------------
#  Test to delete the saved search - Named/Unamed
# ---------------------------------------------------------------------
def test_delete_search(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    response_data = assert_response(response, 201)
    search_id = response_data["id"]

    get_search_response = client.delete(
        "/search/{}?appuserid={}".format(search_id, response_data["appuserid"])
    )
    assert_response(get_search_response, 204)


# ---------------------------------------------------------------------
# Test to create a search with tampered searchtype query parameter
# ---------------------------------------------------------------------
def test_invalid_search_type(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["searchtype"] = "recent"

    create_search_data["name"] = uuid.uuid4().hex
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    invalid_param_response_data = get_body(response)

    assert (
        invalid_param_response_data["message"]
        == "Searchtype in query and body dont match"
    )


# ---------------------------------------------------------------------
# Test to create a saved search with no name
# ---------------------------------------------------------------------
def test_saved_search_type_without_name(client, create_search_json):
    create_search_data = deepcopy(create_search_json)
    create_search_data["name"] = ""
    response = client.post(
        SAVED_SEARCH_POST_URL.format(create_search_data["appuserid"]),
        data=create_search_data,
    )
    no_name_response_data = get_body(response)

    assert (
        no_name_response_data["message"] == "Please specify a name for a saved search"
    )
