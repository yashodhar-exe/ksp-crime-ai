Police FIR System - Synthetic Dataset (100,000 rows per table)
================================================================

Contents:
  00_create_schema.sql   - creates all 28 tables (empty) + a small handwritten sample (from earlier)
  load_data.sql          - psql script that TRUNCATEs the tables and bulk-loads the CSVs via \copy
  <TableName>.csv         - 100,000 synthetic rows for each table, headers included

How to load into PostgreSQL:
  1. createdb police_fir
  2. psql -d police_fir -f 00_create_schema.sql
  3. cd into this folder, then: psql -d police_fir -f load_data.sql

Notes:
  - All foreign keys reference valid primary keys in their parent tables (random draws
    within each parent's ID range of 1..100000).
  - Section and CrimeHeadActSection have composite primary keys; uniqueness is
    guaranteed by construction (SectionCode is a globally unique row id).
  - CrimeNo in CaseMaster embeds the CaseMasterID as its serial component, so
    CrimeNo values are guaranteed unique even though category/district/unit digits
    are randomized.
  - Data is synthetic (Faker-generated names/places) - not real case data.
  - Inv_OccuranceTime and inv_arrestsurrenderaccused are the two tables that were
    referenced in the original Relationship Matrix but not given a column list in
    the source doc; minimal reasonable definitions were used (see 00_create_schema.sql).
