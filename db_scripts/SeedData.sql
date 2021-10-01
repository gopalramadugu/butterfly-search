
--To reset Identity
--ALTER SEQUENCE appuser_id_seq RESTART WITH 1
INSERT INTO public.archivetype
(archive, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Archive1', false, current_timestamp, 0, current_timestamp, 0),
('Archive2', false, current_timestamp, 0, current_timestamp, 0),
('Archive3', false, current_timestamp, 0, current_timestamp, 0),
('Archive4', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.examtype
(exam, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Physical', false, current_timestamp, 0, current_timestamp, 0),
('Cardiac', false, current_timestamp, 0, current_timestamp, 0),
('Vision', false, current_timestamp, 0, current_timestamp, 0),
('Skin', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.machinetype
(machine, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Machine1', false, current_timestamp, 0, current_timestamp, 0),
('Machine2', false, current_timestamp, 0, current_timestamp, 0),
('Machine3', false, current_timestamp, 0, current_timestamp, 0),
('Machine4', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.organization
(orgname, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Tinevele Clinic', false, current_timestamp, 0, current_timestamp, 0),
('Quest', false, current_timestamp, 0, current_timestamp, 0),
('Kaiser', false, current_timestamp, 0, current_timestamp, 0),
('Forbes', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.orgrole
("role", isdeleted, createddate, createdby, updateddate, updatedby)
values
('Role1', false, current_timestamp, 0, current_timestamp, 0),
('Role2', false, current_timestamp, 0, current_timestamp, 0),
('Role3', false, current_timestamp, 0, current_timestamp, 0),
('Role4', false, current_timestamp, 0, current_timestamp, 0);


INSERT INTO public.studystatus
(status, isdeleted, createddate, createdby, updateddate, updatedby)
VALUES
('Draft', false, current_timestamp, 0, current_timestamp, 0),
('UnderReview', false, current_timestamp, 0, current_timestamp, 0),
('Reviewed', false, current_timestamp, 0, current_timestamp, 0),
('Approved', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.tag
(tag, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Tag1', false, current_timestamp, 0, current_timestamp, 0),
('Tag2', false, current_timestamp, 0, current_timestamp, 0),
('Tag3', false, current_timestamp, 0, current_timestamp, 0),
('Tag4', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.worksheettype
(worksheet, isdeleted, createddate, createdby, updateddate, updatedby)
VALUES
('Excel', false, current_timestamp, 0, current_timestamp, 0),
('Pdf', false, current_timestamp, 0, current_timestamp, 0),
('XML', false, current_timestamp, 0, current_timestamp, 0),
('Notepad', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.author
(firstname, lastname, email, isprimary, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Nicole', 'Ann', 'nicole@bfly.com', true, false, current_timestamp, 0, current_timestamp, 0),
('Richard', 'Wang', 'richard@bflycom', true, false, current_timestamp, 0, current_timestamp, 0),
('Peter', 'James', 'peter@bfly.com', true, false, current_timestamp, 0, current_timestamp, 0),
('Chris', 'Hind', 'chrish@bfly.com', false, false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.patient
(firstname, lastname, email, dob, patientmrn, accessionnumber, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Chris', 'Lesic', 'chris@bfly.com', '6/1/1980', '123456', 'Abc12345', false, current_timestamp, 0, current_timestamp, 0),
('Amy', 'Shau', 'amy@bflycom', '7/1/1981', '123457', 'Abc23456', false, current_timestamp, 0, current_timestamp, 0),
('John', 'Zach', 'john@bfly.com', '8/1/1983', '123458', 'Abc98765', false, current_timestamp, 0, current_timestamp, 0),
('Sid', 'Crosby', 'sid@bfly.com', '8/7/1987', '123459', 'Abc94567', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.reviewer
(firstname, lastname, email, isdeleted, createddate, createdby, updateddate, updatedby)
values
('Luke', 'Hilton', 'luke@bfly.com', false, current_timestamp, 0, current_timestamp, 0),
('Alex', 'Smith', 'alex@bflycom', false, current_timestamp, 0, current_timestamp, 0),
('Allison', 'Curry', 'allison@bfly.com', false, current_timestamp, 0, current_timestamp, 0),
('Joe', 'Bores', 'joe@bfly.com', false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.studyinfo
(studydate, summary, orgid, archiveid, machineid, orgroleid, patientid, authorid, reviewerid, examtypeid, studystausid, worksheetid, tagid, isdeleted, createddate, createdby, updateddate, updatedby)
values
('2/1/2021', 'Abc Test', 1, 4, 2, 2, 1, 1, 2, 1, 1, 2, 2, false, current_timestamp, 0, current_timestamp, 0),
('4/12/2021', 'XYZ', 2, 2, 2, 3, 2, 1, 3, 3, 1, 2, 3, false, current_timestamp, 0, current_timestamp, 0),
('3/23/2021', 'Test Summary', 3, 3, 3, 4, 3, 2, 2, 4, 2, 1, 1, false, current_timestamp, 0, current_timestamp, 0),
('8/30/2021', 'Summary Notes', 4, 2, 3, 1, 4, 4, 1, 1, 3, 3, 2, false, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.appuser
(firstname, lastname, email, isactive, createddate, createdby, updateddate, updatedby)
values
('First', 'User', 'first@bfly.com', true, current_timestamp, 0, current_timestamp, 0),
('Second', 'User', 'second@bfly.com', true, current_timestamp, 0, current_timestamp, 0),
('Third', 'User', 'third@bfly.com', true, current_timestamp, 0, current_timestamp, 0),
('Fourth', 'User', 'fourth@bfly.com', true, current_timestamp, 0, current_timestamp, 0);

INSERT INTO public.searchpreferences
(appuserid, "name", searchtype,searchcriteria, isdeleted, createddate, createdby, updateddate, updatedby)
values
(1, 'Search1', 'saved','{"LastName": "Lesic","Author": "Nicole Ann"}', false, current_timestamp, 0, current_timestamp, 0),
(1, 'Search2', 'saved','{"LastName": "Crosby"}', false, current_timestamp, 0, current_timestamp, 0),
(1, null, 'recent','{"Author": "Chris Hind"}', false, current_timestamp, 0, current_timestamp, 0),
(2, 'Seach1','saved' ,'{"Reviewer": "Alex Smith" }', false, current_timestamp, 0, current_timestamp, 0),
(2, null, 'recent','{ "PatientMRN": "123456" }', false, current_timestamp, 0, current_timestamp, 0),
(2, null, 'recent','{"Tags": "Tag1"}', false, current_timestamp, 0, current_timestamp, 0);


commit;