-- ============================================================================
-- Load script: run police_fir_schema_and_data.sql FIRST (creates empty schema),
-- then run this to bulk-load the 100,000-row CSVs via COPY.
-- Run psql from the folder containing the CSVs, or adjust paths below.
-- ============================================================================

TRUNCATE TABLE
    ChargesheetDetails, inv_arrestsurrenderaccused, ArrestSurrender,
    Accused, Victim, ActSectionAssociation, Inv_OccuranceTime, ComplainantDetails,
    CaseMaster, CrimeHeadActSection, Section, Act, CrimeSubHead, CrimeHead,
    GravityOffence, CaseCategory, Court, Employee, Designation, Rank, Unit,
    UnitType, District, State, CasteMaster, ReligionMaster, OccupationMaster,
    CaseStatusMaster
    RESTART IDENTITY CASCADE;

\copy State FROM 'State.csv' WITH (FORMAT csv, HEADER true);
\copy District FROM 'District.csv' WITH (FORMAT csv, HEADER true);
\copy UnitType FROM 'UnitType.csv' WITH (FORMAT csv, HEADER true);
\copy Unit FROM 'Unit.csv' WITH (FORMAT csv, HEADER true);
\copy Rank FROM 'Rank.csv' WITH (FORMAT csv, HEADER true);
\copy Designation FROM 'Designation.csv' WITH (FORMAT csv, HEADER true);
\copy Employee FROM 'Employee.csv' WITH (FORMAT csv, HEADER true);
\copy Court FROM 'Court.csv' WITH (FORMAT csv, HEADER true);
\copy CaseCategory FROM 'CaseCategory.csv' WITH (FORMAT csv, HEADER true);
\copy GravityOffence FROM 'GravityOffence.csv' WITH (FORMAT csv, HEADER true);
\copy CrimeHead FROM 'CrimeHead.csv' WITH (FORMAT csv, HEADER true);
\copy CrimeSubHead FROM 'CrimeSubHead.csv' WITH (FORMAT csv, HEADER true);
\copy CaseStatusMaster FROM 'CaseStatusMaster.csv' WITH (FORMAT csv, HEADER true);
\copy Act FROM 'Act.csv' WITH (FORMAT csv, HEADER true);
\copy Section FROM 'Section.csv' WITH (FORMAT csv, HEADER true);
\copy CrimeHeadActSection FROM 'CrimeHeadActSection.csv' WITH (FORMAT csv, HEADER true);
\copy OccupationMaster FROM 'OccupationMaster.csv' WITH (FORMAT csv, HEADER true);
\copy ReligionMaster FROM 'ReligionMaster.csv' WITH (FORMAT csv, HEADER true);
\copy CasteMaster FROM 'CasteMaster.csv' WITH (FORMAT csv, HEADER true);
\copy CaseMaster FROM 'CaseMaster.csv' WITH (FORMAT csv, HEADER true);
\copy ComplainantDetails FROM 'ComplainantDetails.csv' WITH (FORMAT csv, HEADER true);
\copy ActSectionAssociation FROM 'ActSectionAssociation.csv' WITH (FORMAT csv, HEADER true);
\copy Inv_OccuranceTime FROM 'Inv_OccuranceTime.csv' WITH (FORMAT csv, HEADER true);
\copy Victim FROM 'Victim.csv' WITH (FORMAT csv, HEADER true);
\copy Accused FROM 'Accused.csv' WITH (FORMAT csv, HEADER true);
\copy ArrestSurrender FROM 'ArrestSurrender.csv' WITH (FORMAT csv, HEADER true);
\copy inv_arrestsurrenderaccused FROM 'inv_arrestsurrenderaccused.csv' WITH (FORMAT csv, HEADER true);
\copy ChargesheetDetails FROM 'ChargesheetDetails.csv' WITH (FORMAT csv, HEADER true);

-- Sanity check
SELECT 'State' t, count(*) FROM State
UNION ALL SELECT 'District', count(*) FROM District
UNION ALL SELECT 'CaseMaster', count(*) FROM CaseMaster
UNION ALL SELECT 'ChargesheetDetails', count(*) FROM ChargesheetDetails;
