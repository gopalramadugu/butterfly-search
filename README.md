# Saved Searches Flask Resty API

# Introduction

Saved Search API was built from the grounds with a Flask API that makes it easy for developers and sysadmins to monitor saved and recent searches.

This project shows one of the possible ways to implement RESTful API server for saved and recent searches.

There are implemented with a models having search criteria, search type and last updated date.

Main libraries used:

1. Flask-WTForms - for form validation.
2. Flask-RESTful - restful API library.
3. Flask-Script - provides support for writing external scripts.
4. Flask-SQLAlchemy - adds support for SQLAlchemy ORM.

## Project structure and architecture:

### API Layer

In this folder/layer we can write all our end points in separate files. For a example we can have **init**.py that contains all the routes related to the API. Like wise we can write all the end points in this layer in different files.

### Model Layer

In this layer we can define all our model classes. If we use something like sql alchemy or mongo engine we can define those model classes in here.

### Service Layer

As you saw in the API layer we only accepted the user’s request. But we did not perform any logic in there. We use service layer to write our end points logic. For a example let’s say you have an endpoint to get search data. So in API layer you can write the end point. But in order to get data you need to write queries against a data base or file. So that logic is going to written in this layer.

```
.
├── README.md                         // Readme file showing instructions
├── db_scripts                        // This folder has db scripts
│   ├── SchemaScript.sql
│   ├── SeedData.sql
├── logging                           // Logging data is stored here
│   ├── logs
│   │   ├── logging.ini
│   │
├── search                            // The main API
│   ├── __init__.py
│   ├── models.py                     // Search Model
│   ├── readenv.py
│   ├── routes.py
│   ├── schemas.py
│   ├── settings.py
│   └── views.py
│
├── tests                             // Tests should be in this folder
│   ├── __init__.py
│   └── test_search.py
│
├── __init__.py
├── .env                              // Environment variables are stored here
├── .flake8                           // For Linting purposes
├── .gitattributes                    // Git Attributes
├── .gitignore                        // Which needs to be ignored while pull request
├── .pre-commit-config.yaml           // Pre-Commit configuration make sures Pull Request
├── pyvenv.cfg                        // Config files for the virtual environment
├── Dockerfile                        // Source of Docker file which wraps app into container
├── sonar-project.properties          //Code Quality Assurance tool that collects and analyzes source code, and provides reports for the code quality of your project.
├── sonarcloud.properties
└── requirements.txt                  // Dependencies required for installation
```

- endpoints - holds all endpoints.
- app.py - Flask application initialization.
- settings.py - all global app settings.
- manage.py - script for managing application (migrations, server execution, etc.)

## Use Cases

There are many reasons to use the Saved Search API. The most common use case is to gather report information for a given search and save it, so that you can retrive saved and .

The history of a saved search contains the past and current instances (jobs) of the search.

When you create a saved search, at a minimum you need to provide a search query and a name for the search. You can also specify additional properties for the saved search at this time by providing a dictionary of key-value pairs for the properties. Or, modify properties after you have created the saved search.

## Running

1. Clone repository.
2. Open Docker-Desktop application in background.
3. `docker-compose up --build`
4. `docker-compose down` when done.

## Responses

Many API endpoints return the JSON representation of the resources created or edited. However, if an invalid request is submitted, or some other error occurs, our API returns a JSON response in the following format:

```javascript
{
  "message" : string,
  "success" : bool,
  "data"    : string
}
```

The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource was properly deleted.

The `success` attribute describes if the transaction was successful or not.

The `data` attribute contains any other metadata associated with the response. This will be an escaped string containing JSON data.

## Status Codes

Butterfly Search API returns the following status codes in its API:

| Status Code | Description             |
| :---------- | :---------------------- |
| 200         | `OK`                    |
| 201         | `CREATED`               |
| 400         | `BAD REQUEST`           |
| 404         | `NOT FOUND`             |
| 500         | `INTERNAL SERVER ERROR` |

## Get Saved Searches

By default an array of entry ids is returned in the correct order. The theory is that you will already have some or all of the entries and the ones that you don't yet have can be picked up using `GET /api/search/?appuserid=1&limit=10`.


- `GET /api/search/?appuserid=1&limit=10`
  shall return only specific searches

RESPONSE

```json
{
    "data": [
        {
            "appuserid": 2,
            "createdby": 0,
            "createddate": "2021-09-18T00:00:00",
            "id": 2,
            "name": "SearchSep21343",
            "searchcriteria": {},
            "searchtype": "saved",
            "updatedby": 2,
            "updateddate": "2021-09-30T20:27:33.792445"
        }
    ],
    "meta": {
        "has_next_page": true
    }
}
```

| Parameter               | Required | Example                                                                                                         |
| ----------------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `include_entries: bool` | false    | `GET /v2/saved_searches/1.json?include_entries=true` will return entry objects instead of an array of entry_ids |
| `page: number`          | false    | `GET /v2/saved_searches.json?page=2` will get page two of the search results                                    |

**Status Codes**

- `200 OK` will be returned if found
- `403 Forbidden` will be returned if the user does not own this saved search

## Create Saved Search

- `POST /api/search/?appuserid=4&searchtype=saved` will create a new saved search with the specified parameters

**Request**

```json
{
  "data": {
    "appuserid": 4,
    "createdby": 0,
    "name": "e60f7662c6174021ba6feee",
    "searchtype": "saved",
    "searchcriteria": {
      "reviewer": "G Smith",
      "patientid": "123456"
    },
    "updatedby": 0
  }
}
```

**Response**

```json
{
    "data": {
        "appuserid": 3,
        "createdby": 3,
        "createddate": "2021-10-01T00:49:17.528867",
        "id": 8,
        "name": "Test122",
        "searchcriteria": {
            "firstname": "John",
            "lastname": "Roberts",
            "patientid": "123456",
            "reviewer": "G Smith"
        },
        "searchtype": "saved",
        "updatedby": 3,
        "updateddate": "2021-10-01T00:49:17.528873"
    }
}
```

| Parameter       | Required |
| --------------- | -------- |
| `name: string`  | true     |
| `query: string` | true     |

**Status Codes**

- `201 Created` will be returned if creating the saved search is successful, the `Location` header will have the URL to the newly created saved search

## Delete Saved Search

`DELETE /api/search/14` will delete the saved search with and id of `14`

**Response**

**Status Codes**

- `204 No Content` will be returned if the request was successful
- `403 Forbidden` will be returned if the user does not own this saved search

## Rename Saved Search

Updating a saved search can be used to set a custom title for a feed.

`PATCH /api/search/update/7?appuserid=3` will update the saved search with and id of `7`

**Request**

```json
    {
    "data": 
        {
        "id": 7, 
        "appuserid": 3,
        "name": "User3 - Search2"
        }
    
} 
```

**Response**

```json
{
    "data": {
        "appuserid": 3,
        "createdby": 3,
        "createddate": "2021-09-30",
        "id": 7,
        "name": "User3 - Search2",
        "updatedby": 3,
        "updateddate": "2021-09-30"
    }
}
```

**Status Codes**

- `200 OK` will be returned if the request was successful
- `403 Forbidden` will be returned if the user does not own this saved search

### Swagger API Documentation

------------- TO DO ---------

### POST-Man API requests

------------------ TO DO --------
