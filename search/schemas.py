from marshmallow import Schema, fields


class SearchCriteria(Schema):
    lastname = fields.String(required=False)
    firstname = fields.String(required=False)
    dateofbirth = fields.Date(required=False)
    patientid = fields.String(required=False)
    accessionnumber = fields.Int(required=False)
    studyauthor = fields.Int(required=False)
    startdate = fields.Date(required=False)
    enddate = fields.Date(required=False)
    reviewer = fields.String(required=False)
    examtype = fields.String(required=False)
    studystatus = fields.String(required=False)
    worksheet = fields.String(required=False)
    tags = fields.String(required=False)


class SearchSchema(Schema):
    id = fields.Int(required=False)
    appuserid = fields.Int(required=True)
    name = fields.String(required=False)
    searchtype = fields.String(required=True)
    searchcriteria = fields.Nested(SearchCriteria)
    isdeleted = fields.Boolean(required=False, load_only=True, dump_only=True)
    createddate = fields.DateTime(required=False)
    createdby = fields.Int(required=False)
    updateddate = fields.DateTime(required=False)
    updatedby = fields.Int(required=False)


class SearchQuerySchema(Schema):
    appuserid = fields.Int(required=True)
    searchtype = fields.String(required=False)
    limit = fields.Int(required=False)
    pagination = fields.Int(required=False)


class SearchUpdateSchema(Schema):
    id = fields.Int(required=True)
    appuserid = fields.Int(required=True)
    name = fields.String(required=True)
    createddate = fields.DateTime(required=False)
    createdby = fields.Int(required=False)
    updateddate = fields.DateTime(required=False)
    updatedby = fields.Int(required=False)


class SearchDeleteSchema(Schema):
    id = fields.Int(required=False)
