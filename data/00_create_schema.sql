-- ============================================================================
-- Police FIR System — PostgreSQL Schema + Sample Data
-- Karnataka Police Department (based on supplied ER Diagram)
--
-- Notes on translation from the doc to PostgreSQL:
--   VARCHAR (no length given)  -> VARCHAR(255)
--   NVARCHAR(MAX)              -> TEXT
--   BIT                        -> BOOLEAN
--   DATETIME                   -> TIMESTAMP
--   DECIMAL (lat/long)         -> DECIMAL(10,6)
--   Two tables were referenced in the Relationship Matrix but not given a
--   column list in the doc (Inv_OccuranceTime, inv_arrestsurrenderaccused).
--   Reasonable minimal definitions are included for them, clearly marked.
-- ============================================================================

-- Clean slate (safe to re-run)
DROP TABLE IF EXISTS ChargesheetDetails, inv_arrestsurrenderaccused, ArrestSurrender,
    Accused, Victim, ActSectionAssociation, Inv_OccuranceTime, ComplainantDetails,
    CaseMaster, CrimeHeadActSection, Section, Act, CrimeSubHead, CrimeHead,
    GravityOffence, CaseCategory, Court, Employee, Designation, Rank, Unit,
    UnitType, District, State, CasteMaster, ReligionMaster, OccupationMaster,
    CaseStatusMaster CASCADE;

-- ============================================================================
-- 1. GEOGRAPHY: State -> District
-- ============================================================================

CREATE TABLE State (
    StateID     INT PRIMARY KEY,
    StateName   VARCHAR(255) NOT NULL,
    NationalityID INT,
    Active      BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO State (StateID, StateName, NationalityID, Active) VALUES
(1, 'Karnataka',    1, TRUE),
(2, 'Maharashtra',  1, TRUE),
(3, 'Tamil Nadu',   1, TRUE);

CREATE TABLE District (
    DistrictID   INT PRIMARY KEY,
    DistrictName VARCHAR(255) NOT NULL,
    StateID      INT NOT NULL REFERENCES State(StateID),
    Active       BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO District (DistrictID, DistrictName, StateID, Active) VALUES
(1, 'Bengaluru Urban', 1, TRUE),
(2, 'Mysuru',          1, TRUE),
(3, 'Belagavi',        1, TRUE),
(4, 'Mangaluru (DK)',  1, TRUE),
(5, 'Mumbai City',     2, TRUE);

-- ============================================================================
-- 2. UNITS / POLICE STATIONS
-- ============================================================================

CREATE TABLE UnitType (
    UnitTypeID    INT PRIMARY KEY,
    UnitTypeName  VARCHAR(255) NOT NULL,
    CityDistState VARCHAR(50),
    Hierarchy     INT,
    Active        BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO UnitType (UnitTypeID, UnitTypeName, CityDistState, Hierarchy, Active) VALUES
(1, 'Police Station', 'City',     4, TRUE),
(2, 'Circle Office',  'City',     3, TRUE),
(3, 'SP Office',      'District', 2, TRUE),
(4, 'DGP Office',     'State',    1, TRUE);

CREATE TABLE Unit (
    UnitID       INT PRIMARY KEY,
    UnitName     VARCHAR(255) NOT NULL,
    TypeID       INT REFERENCES UnitType(UnitTypeID),
    ParentUnit   INT REFERENCES Unit(UnitID),
    NationalityID INT,
    StateID      INT REFERENCES State(StateID),
    DistrictID   INT REFERENCES District(DistrictID),
    Active       BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO Unit (UnitID, UnitName, TypeID, ParentUnit, NationalityID, StateID, DistrictID, Active) VALUES
(1, 'Karnataka DGP Office',        4, NULL, 1, 1, 1, TRUE),
(2, 'Bengaluru Urban SP Office',   3, 1,    1, 1, 1, TRUE),
(3, 'Cubbon Park Circle',          2, 2,    1, 1, 1, TRUE),
(4, 'Cubbon Park PS',              1, 3,    1, 1, 1, TRUE),
(5, 'Jayanagar PS',                1, 3,    1, 1, 1, TRUE),
(6, 'Mysuru SP Office',            3, 1,    1, 1, 2, TRUE),
(7, 'Devaraja PS',                 1, 6,    1, 1, 2, TRUE),
(8, 'Belagavi SP Office',          3, 1,    1, 1, 3, TRUE),
(9, 'Tilakwadi PS',                1, 8,    1, 1, 3, TRUE);

-- ============================================================================
-- 3. EMPLOYEE-RELATED LOOKUPS + EMPLOYEE
-- ============================================================================

CREATE TABLE Rank (
    RankID    INT PRIMARY KEY,
    RankName  VARCHAR(255) NOT NULL,
    Hierarchy INT,
    Active    BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO Rank (RankID, RankName, Hierarchy, Active) VALUES
(1, 'Constable',       7, TRUE),
(2, 'Head Constable',  6, TRUE),
(3, 'ASI',             5, TRUE),
(4, 'SI',              4, TRUE),
(5, 'Inspector',       3, TRUE),
(6, 'DSP',             2, TRUE),
(7, 'SP',              1, TRUE);

CREATE TABLE Designation (
    DesignationID   INT PRIMARY KEY,
    DesignationName VARCHAR(255) NOT NULL,
    Active          BOOLEAN NOT NULL DEFAULT TRUE,
    SortOrder       INT
);

INSERT INTO Designation (DesignationID, DesignationName, Active, SortOrder) VALUES
(1, 'Investigating Officer', TRUE, 1),
(2, 'SHO',                   TRUE, 2),
(3, 'Beat Officer',          TRUE, 3),
(4, 'Records Clerk',         TRUE, 4);

CREATE TABLE Employee (
    EmployeeID          INT PRIMARY KEY,
    DistrictID          INT REFERENCES District(DistrictID),
    UnitID              INT REFERENCES Unit(UnitID),
    RankID              INT REFERENCES Rank(RankID),
    DesignationID       INT REFERENCES Designation(DesignationID),
    KGID                VARCHAR(50) UNIQUE,
    FirstName           VARCHAR(255) NOT NULL,
    EmployeeDOB         DATE,
    GenderID             INT,
    BloodGroupID         INT,
    PhysicallyChallenged BOOLEAN DEFAULT FALSE,
    AppointmentDate      DATE
);

INSERT INTO Employee (EmployeeID, DistrictID, UnitID, RankID, DesignationID, KGID, FirstName, EmployeeDOB, GenderID, BloodGroupID, PhysicallyChallenged, AppointmentDate) VALUES
(1, 1, 4, 5, 1, 'KGID1001', 'Ramesh',    '1980-04-12', 1, 1, FALSE, '2005-06-01'),
(2, 1, 4, 4, 2, 'KGID1002', 'Suresh',    '1985-09-23', 1, 2, FALSE, '2010-03-15'),
(3, 1, 5, 5, 1, 'KGID1003', 'Lakshmi',   '1982-01-30', 2, 3, FALSE, '2007-08-19'),
(4, 2, 7, 4, 1, 'KGID1004', 'Manjunath', '1988-11-05', 1, 1, FALSE, '2012-07-22'),
(5, 3, 9, 3, 3, 'KGID1005', 'Deepa',     '1990-02-14', 2, 4, FALSE, '2015-01-10'),
(6, 1, 3, 6, 2, 'KGID1006', 'Prakash',   '1975-06-18', 1, 2, FALSE, '2000-05-01'),
(7, 1, 2, 7, 2, 'KGID1007', 'Ananth',    '1970-12-25', 1, 1, FALSE, '1995-04-01');

-- ============================================================================
-- 4. COURTS
-- ============================================================================

CREATE TABLE Court (
    CourtID    INT PRIMARY KEY,
    CourtName  VARCHAR(255) NOT NULL,
    DistrictID INT REFERENCES District(DistrictID),
    StateID    INT REFERENCES State(StateID),
    Active     BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO Court (CourtID, CourtName, DistrictID, StateID, Active) VALUES
(1, 'City Civil & Sessions Court, Bengaluru', 1, 1, TRUE),
(2, 'Mysuru District & Sessions Court',       2, 1, TRUE),
(3, 'Belagavi District & Sessions Court',     3, 1, TRUE);

-- ============================================================================
-- 5. CASE-RELATED LOOKUPS
-- ============================================================================

CREATE TABLE CaseCategory (
    CaseCategoryID INT PRIMARY KEY,
    LookupValue    VARCHAR(50) NOT NULL
);

INSERT INTO CaseCategory (CaseCategoryID, LookupValue) VALUES
(1, 'FIR'),
(3, 'UDR'),
(8, 'Zero FIR'),
(4, 'PAR');

CREATE TABLE GravityOffence (
    GravityOffenceID INT PRIMARY KEY,
    LookupValue      VARCHAR(50) NOT NULL
);

INSERT INTO GravityOffence (GravityOffenceID, LookupValue) VALUES
(1, 'Heinous'),
(2, 'Non-Heinous');

CREATE TABLE CrimeHead (
    CrimeHeadID   INT PRIMARY KEY,
    CrimeGroupName VARCHAR(255) NOT NULL,
    Active        BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO CrimeHead (CrimeHeadID, CrimeGroupName, Active) VALUES
(1, 'Crimes Against Body',     TRUE),
(2, 'Crimes Against Property', TRUE),
(3, 'Crimes Against Women',    TRUE),
(4, 'Crimes Against Society',  TRUE);

CREATE TABLE CrimeSubHead (
    CrimeSubHeadID INT PRIMARY KEY,
    CrimeHeadID    INT NOT NULL REFERENCES CrimeHead(CrimeHeadID),
    CrimeHeadName  VARCHAR(255) NOT NULL,
    SeqID          INT
);

INSERT INTO CrimeSubHead (CrimeSubHeadID, CrimeHeadID, CrimeHeadName, SeqID) VALUES
(1, 1, 'Murder',              1),
(2, 1, 'Grievous Hurt',       2),
(3, 2, 'Robbery',             1),
(4, 2, 'Theft',               2),
(5, 3, 'Rape',                1),
(6, 4, 'Cheating & Forgery',  1);

CREATE TABLE CaseStatusMaster (
    CaseStatusID   INT PRIMARY KEY,
    CaseStatusName VARCHAR(100) NOT NULL
);

INSERT INTO CaseStatusMaster (CaseStatusID, CaseStatusName) VALUES
(1, 'Under Investigation'),
(2, 'Charge Sheeted'),
(3, 'Closed'),
(4, 'Undetected');

-- ============================================================================
-- 6. ACTS / SECTIONS
-- ============================================================================

CREATE TABLE Act (
    ActCode        VARCHAR(20) PRIMARY KEY,
    ActDescription VARCHAR(255) NOT NULL,
    ShortName      VARCHAR(50),
    Active         BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO Act (ActCode, ActDescription, ShortName, Active) VALUES
('A1', 'Indian Penal Code, 1860',                    'IPC',     TRUE),
('A2', 'Narcotic Drugs and Psychotropic Substances Act', 'NDPS', TRUE),
('A3', 'Information Technology Act, 2000',           'IT Act',  TRUE),
('A4', 'Motor Vehicles Act, 1988',                   'MV Act',  TRUE);

CREATE TABLE Section (
    ActCode           VARCHAR(20) NOT NULL REFERENCES Act(ActCode),
    SectionCode       VARCHAR(20) NOT NULL,
    SectionDescription VARCHAR(255),
    Active            BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (ActCode, SectionCode)
);

INSERT INTO Section (ActCode, SectionCode, SectionDescription, Active) VALUES
('A1', '302', 'Punishment for murder',                       TRUE),
('A1', '307', 'Attempt to murder',                            TRUE),
('A1', '379', 'Punishment for theft',                         TRUE),
('A1', '420', 'Cheating and dishonestly inducing delivery of property', TRUE),
('A2', '8',   'Prohibition of certain operations',            TRUE),
('A3', '66',  'Computer related offences',                    TRUE);

CREATE TABLE CrimeHeadActSection (
    CrimeHeadID INT NOT NULL REFERENCES CrimeHead(CrimeHeadID),
    ActCode     VARCHAR(20) NOT NULL,
    SectionCode VARCHAR(20) NOT NULL,
    PRIMARY KEY (CrimeHeadID, ActCode, SectionCode),
    FOREIGN KEY (ActCode, SectionCode) REFERENCES Section(ActCode, SectionCode)
);

INSERT INTO CrimeHeadActSection (CrimeHeadID, ActCode, SectionCode) VALUES
(1, 'A1', '302'),
(1, 'A1', '307'),
(2, 'A1', '379'),
(4, 'A1', '420'),
(4, 'A3', '66');

-- ============================================================================
-- 7. PERSON-RELATED LOOKUPS
-- ============================================================================

CREATE TABLE OccupationMaster (
    OccupationID   INT PRIMARY KEY,
    OccupationName VARCHAR(100) NOT NULL
);

INSERT INTO OccupationMaster (OccupationID, OccupationName) VALUES
(1, 'Farmer'),
(2, 'Government Employee'),
(3, 'Private Employee'),
(4, 'Business'),
(5, 'Student'),
(6, 'Homemaker'),
(7, 'Unemployed');

CREATE TABLE ReligionMaster (
    ReligionID   INT PRIMARY KEY,
    ReligionName VARCHAR(100) NOT NULL
);

INSERT INTO ReligionMaster (ReligionID, ReligionName) VALUES
(1, 'Hindu'),
(2, 'Muslim'),
(3, 'Christian'),
(4, 'Sikh'),
(5, 'Jain'),
(6, 'Others');

CREATE TABLE CasteMaster (
    caste_master_id   INT PRIMARY KEY,
    caste_master_name VARCHAR(100) NOT NULL
);

INSERT INTO CasteMaster (caste_master_id, caste_master_name) VALUES
(1, 'General'),
(2, 'OBC'),
(3, 'SC'),
(4, 'ST'),
(5, 'Others');

-- ============================================================================
-- 8. CASE MASTER (the core FIR table)
-- ============================================================================

CREATE TABLE CaseMaster (
    CaseMasterID        INT PRIMARY KEY,
    CrimeNo              VARCHAR(50) NOT NULL UNIQUE,
    CaseNo                VARCHAR(20) NOT NULL,
    CrimeRegisteredDate    DATE NOT NULL,
    PolicePersonID         INT REFERENCES Employee(EmployeeID),
    PoliceStationID        INT REFERENCES Unit(UnitID),
    CaseCategoryID         INT REFERENCES CaseCategory(CaseCategoryID),
    GravityOffenceID       INT REFERENCES GravityOffence(GravityOffenceID),
    CrimeMajorHeadID       INT REFERENCES CrimeHead(CrimeHeadID),
    CrimeMinorHeadID       INT REFERENCES CrimeSubHead(CrimeSubHeadID),
    CaseStatusID           INT REFERENCES CaseStatusMaster(CaseStatusID),
    CourtID                INT REFERENCES Court(CourtID),
    IncidentFromDate       TIMESTAMP,
    IncidentToDate         TIMESTAMP,
    InfoReceivedPSDate     TIMESTAMP,
    latitude               DECIMAL(10,6),
    longitude              DECIMAL(10,6),
    BriefFacts             TEXT
);

-- CrimeNo format: 1-digit CaseCategory + 4-digit DistrictID + 4-digit UnitID + 4-digit Year + 5-digit Serial
INSERT INTO CaseMaster (CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonID, PoliceStationID,
    CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID, CourtID,
    IncidentFromDate, IncidentToDate, InfoReceivedPSDate, latitude, longitude, BriefFacts) VALUES
(1, '100010004202600001', '202600001', '2026-01-05', 1, 4, 1, 1, 1, 1, 1, 1,
    '2026-01-04 21:30:00', '2026-01-04 22:00:00', '2026-01-05 06:15:00', 12.975000, 77.605000,
    'Complainant reports a fatal stabbing incident outside a bar on the night of 4th January 2026.'),
(2, '100010004202600002', '202600002', '2026-02-10', 2, 4, 1, 2, 2, 4, 1, 1,
    '2026-02-09 14:00:00', '2026-02-09 14:30:00', '2026-02-10 09:00:00', 12.976500, 77.606200,
    'Theft of two-wheeler reported from outside a residential complex.'),
(3, '100010005202600003', '202600003', '2026-02-20', 3, 5, 1, 1, 3, 5, 2, 1,
    '2026-02-19 20:00:00', '2026-02-19 21:00:00', '2026-02-20 08:30:00', 12.930000, 77.583000,
    'Complaint filed alleging sexual assault; investigation ongoing.'),
(4, '100020007202600004', '202600004', '2026-03-02', 4, 7, 1, 2, 4, 6, 1, 2,
    '2026-03-01 11:00:00', '2026-03-01 12:00:00', '2026-03-02 10:00:00', 12.295800, 76.639400,
    'Online fraud case; victim transferred money after being cheated by caller posing as bank official.'),
(5, '300030009202600005', '202600005', '2026-03-18', 5, 9, 3, 2, 1, 2, 3, 3,
    '2026-03-17 05:00:00', '2026-03-17 05:30:00', '2026-03-18 07:00:00', 15.851400, 74.499800,
    'Unnatural death report — body found near railway tracks, cause of death under inquiry.'),
(6, '800010004202600006', '202600006', '2026-04-01', 1, 4, 8, 1, 1, 1, 1, 1,
    '2026-03-31 23:00:00', '2026-04-01 00:15:00', '2026-04-01 01:00:00', 12.974200, 77.604100,
    'Zero FIR registered for a case occurring outside station jurisdiction, to be transferred.');

-- ============================================================================
-- 9. CASE-LINKED TABLES
-- ============================================================================

CREATE TABLE ComplainantDetails (
    ComplainantID     INT PRIMARY KEY,
    CaseMasterID      INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    ComplainantName   VARCHAR(255) NOT NULL,
    AgeYear           INT,
    OccupationID      INT REFERENCES OccupationMaster(OccupationID),
    ReligionID        INT REFERENCES ReligionMaster(ReligionID),
    CasteID           INT REFERENCES CasteMaster(caste_master_id),
    GenderID          INT
);

INSERT INTO ComplainantDetails (ComplainantID, CaseMasterID, ComplainantName, AgeYear, OccupationID, ReligionID, CasteID, GenderID) VALUES
(1, 1, 'Nagaraj K',      45, 4, 1, 2, 1),
(2, 2, 'Priya S',        29, 3, 1, 1, 2),
(3, 3, 'Anjali R',       24, 5, 3, 1, 2),
(4, 4, 'Mohammed Rafiq', 38, 3, 2, 5, 1),
(5, 5, 'Basavaraj P',    52, 1, 1, 2, 1),
(6, 6, 'Kavya M',        31, 2, 1, 1, 2);

CREATE TABLE ActSectionAssociation (
    CaseMasterID   INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    ActID          VARCHAR(20) NOT NULL,
    SectionID      VARCHAR(20) NOT NULL,
    ActOrderID     INT,
    SectionOrderID INT,
    PRIMARY KEY (CaseMasterID, ActID, SectionID),
    FOREIGN KEY (ActID) REFERENCES Act(ActCode),
    FOREIGN KEY (ActID, SectionID) REFERENCES Section(ActCode, SectionCode)
);

INSERT INTO ActSectionAssociation (CaseMasterID, ActID, SectionID, ActOrderID, SectionOrderID) VALUES
(1, 'A1', '302', 1, 1),
(2, 'A1', '379', 1, 1),
(3, 'A1', '307', 1, 1),
(4, 'A1', '420', 1, 1),
(4, 'A3', '66',  2, 1),
(6, 'A1', '302', 1, 1);

-- One-to-one with CaseMaster (referenced in Relationship Matrix, column list
-- not detailed in source doc — minimal reasonable definition below)
CREATE TABLE Inv_OccuranceTime (
    CaseMasterID    INT PRIMARY KEY REFERENCES CaseMaster(CaseMasterID),
    OccuranceFromTime TIMESTAMP,
    OccuranceToTime   TIMESTAMP,
    PlaceOfOccurrence VARCHAR(255)
);

INSERT INTO Inv_OccuranceTime (CaseMasterID, OccuranceFromTime, OccuranceToTime, PlaceOfOccurrence) VALUES
(1, '2026-01-04 21:30:00', '2026-01-04 22:00:00', 'Near XYZ Bar, MG Road'),
(2, '2026-02-09 14:00:00', '2026-02-09 14:30:00', 'Outside Residency Apartments'),
(3, '2026-02-19 20:00:00', '2026-02-19 21:00:00', 'Behind City Park'),
(4, '2026-03-01 11:00:00', '2026-03-01 12:00:00', 'Online / Bank Transfer'),
(5, '2026-03-17 05:00:00', '2026-03-17 05:30:00', 'Near Railway Track, Tilakwadi'),
(6, '2026-03-31 23:00:00', '2026-04-01 00:15:00', 'MG Road Junction');

CREATE TABLE Victim (
    VictimMasterID INT PRIMARY KEY,
    CaseMasterID   INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    VictimName     VARCHAR(255) NOT NULL,
    AgeYear        INT,
    GenderID       VARCHAR(5),
    VictimPolice   BOOLEAN DEFAULT FALSE
);

INSERT INTO Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID, VictimPolice) VALUES
(1, 1, 'Rajesh T',   34, 'M', FALSE),
(2, 2, 'Priya S',    29, 'F', FALSE),
(3, 3, 'Anjali R',   24, 'F', FALSE),
(4, 4, 'Mohammed Rafiq', 38, 'M', FALSE),
(5, 5, 'Unknown',    NULL, 'M', FALSE),
(6, 6, 'Ganesh V',   27, 'M', TRUE);

CREATE TABLE Accused (
    AccusedMasterID INT PRIMARY KEY,
    CaseMasterID    INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    AccusedName     VARCHAR(255) NOT NULL,
    AgeYear         INT,
    GenderID        VARCHAR(5),
    PersonID        VARCHAR(10)
);

INSERT INTO Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear, GenderID, PersonID) VALUES
(1, 1, 'Manoj Kumar', 30, 'M', 'A1'),
(2, 1, 'Santosh B',   28, 'M', 'A2'),
(3, 2, 'Unknown',     NULL, 'M', 'A1'),
(4, 3, 'Ravi D',      33, 'M', 'A1'),
(5, 4, 'Unknown Caller', NULL, 'M', 'A1'),
(6, 6, 'Kiran J',     26, 'M', 'A1');

-- ============================================================================
-- 10. ARREST / SURRENDER
-- ============================================================================

CREATE TABLE ArrestSurrender (
    ArrestSurrenderID     INT PRIMARY KEY,
    CaseMasterID          INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    ArrestSurrenderTypeID INT,   -- 1 = Arrest, 2 = Surrender (lookup value)
    ArrestSurrenderDate   DATE,
    ArrestSurrenderStateId    INT REFERENCES State(StateID),
    ArrestSurrenderDistrictId INT REFERENCES District(DistrictID),
    PoliceStationID       INT REFERENCES Unit(UnitID),
    IOID                  INT REFERENCES Employee(EmployeeID),
    CourtID               INT REFERENCES Court(CourtID),
    AccusedMasterID       INT REFERENCES Accused(AccusedMasterID),
    IsAccused             BOOLEAN DEFAULT TRUE,
    IsComplainantAccused  BOOLEAN DEFAULT FALSE
);

INSERT INTO ArrestSurrender (ArrestSurrenderID, CaseMasterID, ArrestSurrenderTypeID, ArrestSurrenderDate,
    ArrestSurrenderStateId, ArrestSurrenderDistrictId, PoliceStationID, IOID, CourtID, AccusedMasterID,
    IsAccused, IsComplainantAccused) VALUES
(1, 1, 1, '2026-01-06', 1, 1, 4, 1, 1, 1, TRUE, FALSE),
(2, 1, 1, '2026-01-07', 1, 1, 4, 1, 1, 2, TRUE, FALSE),
(3, 3, 1, '2026-02-22', 1, 1, 5, 3, 1, 4, TRUE, FALSE),
(4, 6, 2, '2026-04-02', 1, 1, 4, 1, 1, 6, TRUE, FALSE);

-- Junction table referenced in the Relationship Matrix (column list not
-- detailed in source doc — minimal reasonable definition below)
CREATE TABLE inv_arrestsurrenderaccused (
    ID                INT PRIMARY KEY,
    ArrestSurrenderID INT NOT NULL REFERENCES ArrestSurrender(ArrestSurrenderID),
    AccusedMasterID   INT NOT NULL REFERENCES Accused(AccusedMasterID)
);

INSERT INTO inv_arrestsurrenderaccused (ID, ArrestSurrenderID, AccusedMasterID) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 4),
(4, 4, 6);

-- ============================================================================
-- 11. CHARGESHEET
-- ============================================================================

CREATE TABLE ChargesheetDetails (
    CSID           INT PRIMARY KEY,
    CaseMasterID   INT NOT NULL REFERENCES CaseMaster(CaseMasterID),
    csdate         TIMESTAMP,
    cstype         CHAR(1) CHECK (cstype IN ('A','B','C')), -- A=Chargesheet, B=False Case, C=Undetected
    PolicePersonID INT REFERENCES Employee(EmployeeID)
);

INSERT INTO ChargesheetDetails (CSID, CaseMasterID, csdate, cstype, PolicePersonID) VALUES
(1, 1, '2026-03-01 10:00:00', 'A', 1),
(2, 2, '2026-04-05 11:30:00', 'C', 2),
(3, 3, '2026-05-01 09:00:00', 'A', 3),
(4, 5, '2026-04-20 15:00:00', 'B', 5);

-- ============================================================================
-- Quick sanity check
-- ============================================================================
-- SELECT cm.CrimeNo, cm.CaseNo, cc.LookupValue AS Category, csm.CaseStatusName,
--        e.FirstName AS RegisteredBy, u.UnitName AS Station
-- FROM CaseMaster cm
-- JOIN CaseCategory cc ON cc.CaseCategoryID = cm.CaseCategoryID
-- JOIN CaseStatusMaster csm ON csm.CaseStatusID = cm.CaseStatusID
-- JOIN Employee e ON e.EmployeeID = cm.PolicePersonID
-- JOIN Unit u ON u.UnitID = cm.PoliceStationID
-- ORDER BY cm.CaseMasterID;
