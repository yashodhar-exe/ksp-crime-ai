-- =============================================================================
-- KSP Crime AI — Postgres schema
-- Matches columns/dtypes in dataset/processed/*.csv exactly.
-- Load order (parents -> children) mirrors dataset/seed/load_database.py.
-- =============================================================================

BEGIN;

-- Drop in reverse dependency order (safe to re-run during dev)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS search_index CASCADE;
DROP TABLE IF EXISTS timeline CASCADE;
DROP TABLE IF EXISTS investigation_notes CASCADE;
DROP TABLE IF EXISTS criminal_relationships CASCADE;
DROP TABLE IF EXISTS digital_evidence CASCADE;
DROP TABLE IF EXISTS evidence CASCADE;
DROP TABLE IF EXISTS bank_accounts CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS victims CASCADE;
DROP TABLE IF EXISTS suspects CASCADE;
DROP TABLE IF EXISTS cases CASCADE;
DROP TABLE IF EXISTS crime_patterns CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS officers CASCADE;
DROP TABLE IF EXISTS citizens CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS police_stations CASCADE;

-- =============================================================================
-- 1. police_stations
-- =============================================================================
CREATE TABLE police_stations (
    station_id      VARCHAR(10)  PRIMARY KEY,
    station_name    VARCHAR(150) NOT NULL,
    district        VARCHAR(100) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    phone           VARCHAR(15)  NOT NULL
);

-- =============================================================================
-- 2. roles
-- =============================================================================
CREATE TABLE roles (
    role_id                  VARCHAR(10) PRIMARY KEY,
    role_name                VARCHAR(50) NOT NULL UNIQUE,
    level                    INTEGER     NOT NULL,
    can_view_all_districts   BOOLEAN     NOT NULL DEFAULT FALSE,
    can_export               BOOLEAN     NOT NULL DEFAULT FALSE,
    can_edit_case            BOOLEAN     NOT NULL DEFAULT FALSE,
    can_manage_users         BOOLEAN     NOT NULL DEFAULT FALSE
);

-- =============================================================================
-- 3. citizens
-- =============================================================================
CREATE TABLE citizens (
    citizen_id        VARCHAR(12)  PRIMARY KEY,
    first_name        VARCHAR(100) NOT NULL,
    last_name         VARCHAR(100) NOT NULL,
    gender            VARCHAR(20)  NOT NULL,
    age               INTEGER      NOT NULL CHECK (age >= 0 AND age <= 120),
    phone             VARCHAR(15)  NOT NULL,
    email             VARCHAR(255),
    address           TEXT,
    city              VARCHAR(100) NOT NULL,
    district          VARCHAR(100) NOT NULL,
    demo_citizen_id   VARCHAR(20)
);

CREATE INDEX idx_citizens_city     ON citizens (city);
CREATE INDEX idx_citizens_district ON citizens (district);
CREATE INDEX idx_citizens_phone    ON citizens (phone);

-- =============================================================================
-- 4. officers
-- =============================================================================
CREATE TABLE officers (
    officer_id   VARCHAR(10) PRIMARY KEY,
    name         VARCHAR(150) NOT NULL,
    rank         VARCHAR(50)  NOT NULL,
    station_id   VARCHAR(10)  NOT NULL REFERENCES police_stations (station_id),
    phone        VARCHAR(15)  NOT NULL,
    email        VARCHAR(255)
);

CREATE INDEX idx_officers_station ON officers (station_id);

-- =============================================================================
-- 5. users (login accounts, tied to officers + roles)
-- =============================================================================
CREATE TABLE users (
    user_id      VARCHAR(10) PRIMARY KEY,
    officer_id   VARCHAR(10) REFERENCES officers (officer_id),   -- nullable: top-level Admin/SP accounts
    username     VARCHAR(100) NOT NULL UNIQUE,
    role_id      VARCHAR(10)  NOT NULL REFERENCES roles (role_id),
    station_id   VARCHAR(10)  REFERENCES police_stations (station_id),
    status       VARCHAR(20)  NOT NULL DEFAULT 'Active',
    last_login   DATE
    -- hashed_password is NOT added here: schema.sql models the seeded demo
    -- dataset, which has no credentials. It's added by
    -- backend/alembic/versions/0001_add_users_hashed_password.py — run
    -- `alembic upgrade head` after loading this schema. See backend/README.md.
);

CREATE INDEX idx_users_role ON users (role_id);

-- =============================================================================
-- 6. crime_patterns
-- =============================================================================
CREATE TABLE crime_patterns (
    pattern_id       VARCHAR(10) PRIMARY KEY,
    crime_type       VARCHAR(50) NOT NULL,
    modus_operandi   VARCHAR(150),
    communication    VARCHAR(50),   -- 'None' literal string where not applicable
    payment_method   VARCHAR(50),   -- 'None' literal string where not applicable
    risk_level       VARCHAR(20)  NOT NULL
);

CREATE INDEX idx_crime_patterns_type ON crime_patterns (crime_type);

-- =============================================================================
-- 7. cases
-- =============================================================================
CREATE TABLE cases (
    case_id           VARCHAR(12)  PRIMARY KEY,
    fir_number        VARCHAR(20)  NOT NULL UNIQUE,
    crime_type        VARCHAR(50)  NOT NULL,
    station_id        VARCHAR(10)  NOT NULL REFERENCES police_stations (station_id),
    officer_id        VARCHAR(10)  NOT NULL REFERENCES officers (officer_id),
    status            VARCHAR(30)  NOT NULL,
    priority          VARCHAR(20)  NOT NULL,
    incident_date     DATE         NOT NULL,
    registered_date   DATE         NOT NULL,
    city              VARCHAR(100) NOT NULL,
    district          VARCHAR(100) NOT NULL,
    description       TEXT,                       -- legacy placeholder text; prefer complaint_text
    estimated_loss    BIGINT       NOT NULL DEFAULT 0,
    complaint_text    TEXT         NOT NULL,       -- FIR-style narrative; use this for RAG/chatbot
    pattern_id        VARCHAR(10)  REFERENCES crime_patterns (pattern_id)  -- nullable: not every crime_type has a defined pattern
);

CREATE INDEX idx_cases_station     ON cases (station_id);
CREATE INDEX idx_cases_officer     ON cases (officer_id);
CREATE INDEX idx_cases_crime_type  ON cases (crime_type);
CREATE INDEX idx_cases_status      ON cases (status);
CREATE INDEX idx_cases_district    ON cases (district);
CREATE INDEX idx_cases_city        ON cases (city);
CREATE INDEX idx_cases_pattern     ON cases (pattern_id);
CREATE INDEX idx_cases_incident_dt ON cases (incident_date);
-- full-text search over the narrative, for the chatbot / search feature
CREATE INDEX idx_cases_complaint_fts ON cases USING gin (to_tsvector('english', complaint_text));

-- =============================================================================
-- 8. suspects
-- =============================================================================
CREATE TABLE suspects (
    suspect_id      VARCHAR(12) PRIMARY KEY,
    case_id         VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    citizen_id      VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    role            VARCHAR(50) NOT NULL,
    arrest_status   VARCHAR(30) NOT NULL
);

CREATE INDEX idx_suspects_case    ON suspects (case_id);
CREATE INDEX idx_suspects_citizen ON suspects (citizen_id);

-- =============================================================================
-- 9. victims
-- =============================================================================
CREATE TABLE victims (
    victim_id      VARCHAR(12) PRIMARY KEY,
    case_id        VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    citizen_id     VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    injury_level   VARCHAR(30) NOT NULL
);

CREATE INDEX idx_victims_case    ON victims (case_id);
CREATE INDEX idx_victims_citizen ON victims (citizen_id);

-- =============================================================================
-- 10. phones
-- =============================================================================
CREATE TABLE phones (
    phone_id       VARCHAR(10) PRIMARY KEY,
    citizen_id     VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    phone_number   VARCHAR(15) NOT NULL,
    provider       VARCHAR(50)
);

CREATE INDEX idx_phones_citizen ON phones (citizen_id);
CREATE INDEX idx_phones_number  ON phones (phone_number);

-- =============================================================================
-- 11. vehicles
-- =============================================================================
CREATE TABLE vehicles (
    vehicle_id       VARCHAR(10) PRIMARY KEY,
    citizen_id       VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    vehicle_number   VARCHAR(20) NOT NULL,
    vehicle_type     VARCHAR(30)
);

CREATE INDEX idx_vehicles_citizen ON vehicles (citizen_id);
CREATE INDEX idx_vehicles_number  ON vehicles (vehicle_number);

-- =============================================================================
-- 12. bank_accounts
-- =============================================================================
CREATE TABLE bank_accounts (
    account_id       VARCHAR(10) PRIMARY KEY,
    citizen_id       VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    bank_name        VARCHAR(100) NOT NULL,
    account_number   VARCHAR(30) NOT NULL,
    ifsc             CHAR(11)
);

CREATE INDEX idx_bank_accounts_citizen ON bank_accounts (citizen_id);

-- =============================================================================
-- 13. evidence
-- =============================================================================
CREATE TABLE evidence (
    evidence_id     VARCHAR(10) PRIMARY KEY,
    case_id         VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    evidence_type   VARCHAR(50) NOT NULL,
    description     TEXT,
    status          VARCHAR(30) NOT NULL,
    collected_by    VARCHAR(10) REFERENCES officers (officer_id)
);

CREATE INDEX idx_evidence_case ON evidence (case_id);

-- =============================================================================
-- 14. digital_evidence
-- =============================================================================
CREATE TABLE digital_evidence (
    digital_evidence_id   VARCHAR(10) PRIMARY KEY,
    case_id               VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    file_type             VARCHAR(50) NOT NULL,
    file_name             VARCHAR(200),
    phone_number          VARCHAR(15),
    email                 VARCHAR(255),
    ip_address            VARCHAR(45),
    uploaded_by           VARCHAR(10) REFERENCES officers (officer_id),
    status                VARCHAR(30) NOT NULL,
    extracted_entities    TEXT   -- OCR/NER-style summary; populate via pipeline later
);

CREATE INDEX idx_digital_evidence_case ON digital_evidence (case_id);

-- =============================================================================
-- 15. criminal_relationships (network graph edges)
-- =============================================================================
CREATE TABLE criminal_relationships (
    relationship_id      VARCHAR(12) PRIMARY KEY,
    citizen_1            VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    citizen_2            VARCHAR(12) NOT NULL REFERENCES citizens (citizen_id),
    relationship_type    VARCHAR(50) NOT NULL,
    CHECK (citizen_1 <> citizen_2)
);

CREATE INDEX idx_criminal_rel_c1 ON criminal_relationships (citizen_1);
CREATE INDEX idx_criminal_rel_c2 ON criminal_relationships (citizen_2);

-- =============================================================================
-- 16. investigation_notes
-- =============================================================================
CREATE TABLE investigation_notes (
    note_id       VARCHAR(12) PRIMARY KEY,
    case_id       VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    officer_id    VARCHAR(10) NOT NULL REFERENCES officers (officer_id),
    note          TEXT NOT NULL
);

CREATE INDEX idx_investigation_notes_case ON investigation_notes (case_id);
CREATE INDEX idx_investigation_notes_fts  ON investigation_notes USING gin (to_tsvector('english', note));

-- =============================================================================
-- 17. timeline
-- =============================================================================
CREATE TABLE timeline (
    event_id   VARCHAR(12) PRIMARY KEY,
    case_id    VARCHAR(12) NOT NULL REFERENCES cases (case_id),
    event      VARCHAR(200) NOT NULL
);

CREATE INDEX idx_timeline_case ON timeline (case_id);

-- =============================================================================
-- 18. search_index (entity_value -> case_id lookups; see augment_dataset.py
--     for how this is built from real victim/suspect/officer linkages)
-- =============================================================================
CREATE TABLE search_index (
    search_id      VARCHAR(12) PRIMARY KEY,
    entity_type    VARCHAR(20) NOT NULL,   -- Citizen | Phone | Vehicle | Bank | Officer | Case
    entity_value   VARCHAR(100) NOT NULL,
    case_id        VARCHAR(12) NOT NULL REFERENCES cases (case_id)
);

CREATE INDEX idx_search_index_entity_value ON search_index (entity_value);
CREATE INDEX idx_search_index_entity_type  ON search_index (entity_type);
CREATE INDEX idx_search_index_type_value   ON search_index (entity_type, entity_value);

-- =============================================================================
-- 19. audit_logs
-- =============================================================================
CREATE TABLE audit_logs (
    log_id       VARCHAR(12) PRIMARY KEY,
    user_id      VARCHAR(10) NOT NULL REFERENCES users (user_id),
    action       VARCHAR(50) NOT NULL,   -- Viewed Case | Downloaded Report | Updated Evidence | Searched Entity | Viewed Suspect Profile
    case_id      VARCHAR(12) REFERENCES cases (case_id),   -- nullable: 'Searched Entity' actions have no case_id
    timestamp    TIMESTAMP   NOT NULL,
    ip_address   VARCHAR(45) NOT NULL
);

CREATE INDEX idx_audit_logs_user      ON audit_logs (user_id);
CREATE INDEX idx_audit_logs_case      ON audit_logs (case_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs (timestamp);

-- =============================================================================
-- Done. Load with: python dataset/seed/load_database.py
-- =============================================================================

COMMIT;