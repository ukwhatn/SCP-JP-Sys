-- create database
CREATE DATABASE master
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE master
    IS 'scp-jp-sys master database';

-- use database
\c master;

-- create schema
CREATE SCHEMA system;
ALTER SCHEMA system OWNER TO admin;

-- create table
CREATE TABLE system.users
(
    id                  integer                                   NOT NULL,
    name                character varying(50)                     NOT NULL,
    is_available        boolean                     DEFAULT true  NOT NULL,
    icon_url            character varying(100)      DEFAULT NULL::character varying,
    privilege_level     smallint                    DEFAULT 0     NOT NULL,
    created_at          timestamp without time zone DEFAULT now() NOT NULL,
    latest_updated_at   timestamp without time zone DEFAULT now() NOT NULL,
    latest_logged_in_at timestamp without time zone DEFAULT now()
);
ALTER TABLE system.users
    OWNER TO admin;
COMMENT ON TABLE system.users IS 'SCP-JP Management System Users Information Table';
COMMENT ON COLUMN system.users.id IS '一意な内部ユーザID';
COMMENT ON COLUMN system.users.name IS 'ユーザ名';
COMMENT ON COLUMN system.users.is_available IS 'ユーザが有効か';
COMMENT ON COLUMN system.users.icon_url IS 'システム内アイコンURL';
COMMENT ON COLUMN system.users.privilege_level IS '権限レベル(デフォルトで0)';
COMMENT ON COLUMN system.users.created_at IS 'アカウント作成日';
COMMENT ON COLUMN system.users.latest_updated_at IS 'アカウント最終更新日';
COMMENT ON COLUMN system.users.latest_logged_in_at IS 'アカウント最終ログイン日';

-- create serial sequence
CREATE SEQUENCE system.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE system.users_id_seq
    OWNER TO admin;
ALTER SEQUENCE system.users_id_seq OWNED BY system.users.id;
ALTER TABLE ONLY system.users
    ALTER COLUMN id SET DEFAULT nextval('system.users_id_seq'::regclass);

SELECT pg_catalog.setval('system.users_id_seq', 1, false);

-- create primary key
ALTER TABLE ONLY system.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

-- create name index
CREATE INDEX users_name ON system.users USING btree (name);

-- grant privileges
GRANT SELECT ON TABLE system.users TO application_users;
GRANT SELECT, INSERT, UPDATE ON TABLE system.users TO api;
ALTER DEFAULT PRIVILEGES FOR ROLE admin IN SCHEMA system GRANT SELECT ON TABLES TO application_users;
