-- create master database
CREATE DATABASE master
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
-- commenting
COMMENT ON DATABASE master
    IS 'scp-jp-sys master database';
-- give permission to create schema to user "api"
GRANT CREATE ON DATABASE master TO api;

-- use database master
\c master;

-- create "system" schema
CREATE SCHEMA system;
ALTER SCHEMA system OWNER TO admin;
-- give all permissions to "api"
GRANT ALL PRIVILEGES ON SCHEMA system TO api;
