-- DROP TABLE searchpreferences;
-- DROP TABLE appuser; 
-- DROP TABLE studyinfo;
-- DROP TABLE archivetype;
-- DROP TABLE studystatus;
-- DROP TABLE tag;
-- DROP TABLE worksheettype;
-- DROP TABLE examtype;
-- DROP TABLE machinetype;
-- DROP TABLE organization;
-- DROP TABLE orgrole;
-- DROP TABLE author;
-- DROP TABLE patient;
-- DROP TABLE reviewer;

CREATE TABLE appuser (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	email varchar NOT NULL,
	isactive bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT appuser_pk PRIMARY KEY (id)
);

CREATE TABLE archivetype (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	archive varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT archivetype_pk PRIMARY KEY (id)
);

CREATE TABLE author (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	email varchar NOT NULL,
	isprimary bool NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT author_pk PRIMARY KEY (id)
);

CREATE TABLE examtype (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	exam varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT examtype_pk PRIMARY KEY (id)
);

CREATE TABLE machinetype (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	machine varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT machinetype_pk PRIMARY KEY (id)
);

CREATE TABLE organization (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	orgname varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT organization_pk PRIMARY KEY (id)
);

CREATE TABLE orgrole (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"role" varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT orgrole_pk PRIMARY KEY (id)
);

CREATE TABLE patient (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	email varchar NOT NULL,
	dob date NULL,
	patientmrn varchar NULL,
	accessionnumber varchar NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT patient_pk PRIMARY KEY (id)
);

CREATE TABLE reviewer (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	email varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT reviewer_pk PRIMARY KEY (id)
);


CREATE TABLE studystatus (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	status varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT studystatus_pk PRIMARY KEY (id)
);

CREATE TABLE tag (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	tag varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT tag_pk PRIMARY KEY (id)
);

CREATE TABLE worksheettype (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	worksheet varchar NOT NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT worksheettype_pk PRIMARY KEY (id)
);

CREATE TABLE searchpreferences (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	appuserid int4 NOT NULL,
	name varchar NULL,
	searchtype varchar NULL,
	searchcriteria json NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT searchpreferences_pk PRIMARY KEY (id),
	CONSTRAINT searchpreferences_fk FOREIGN KEY (appuserid) REFERENCES appuser(id)
);

CREATE TABLE studyinfo (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	studydate timestamp NOT NULL,
	summary varchar NOT NULL,
	orgid int4 NULL,
	archiveid int4 NULL,
	machineid int4 NULL,
	orgroleid int4 NULL,
	patientid int4 NULL,
	authorid int4 NULL,
	reviewerid int4 NULL,
	examtypeid int4 NULL,
	studystausid int4 NULL,
	worksheetid int4 NULL,
	tagid int4 NULL,
	isdeleted bool NULL,
	createddate timestamp NULL,
	createdby int4 NULL,
	updateddate timestamp NULL,
	updatedby int4 NULL,
	CONSTRAINT studyinfo_pk PRIMARY KEY (id),
	CONSTRAINT studyinfo_fk FOREIGN KEY (orgid) REFERENCES organization(id),
	CONSTRAINT studyinfo_fk_1 FOREIGN KEY (authorid) REFERENCES author(id),
	CONSTRAINT studyinfo_fk_10 FOREIGN KEY (archiveid) REFERENCES archivetype(id),
	CONSTRAINT studyinfo_fk_2 FOREIGN KEY (examtypeid) REFERENCES examtype(id),
	CONSTRAINT studyinfo_fk_3 FOREIGN KEY (machineid) REFERENCES machinetype(id),
	CONSTRAINT studyinfo_fk_4 FOREIGN KEY (orgroleid) REFERENCES orgrole(id),
	CONSTRAINT studyinfo_fk_5 FOREIGN KEY (patientid) REFERENCES patient(id),
	CONSTRAINT studyinfo_fk_6 FOREIGN KEY (reviewerid) REFERENCES reviewer(id),
	CONSTRAINT studyinfo_fk_7 FOREIGN KEY (studystausid) REFERENCES studystatus(id),
	CONSTRAINT studyinfo_fk_8 FOREIGN KEY (tagid) REFERENCES tag(id),
	CONSTRAINT studyinfo_fk_9 FOREIGN KEY (worksheetid) REFERENCES worksheettype(id)
);