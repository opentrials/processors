--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

ALTER TABLE IF EXISTS ONLY public.oauth_credentials DROP CONSTRAINT IF EXISTS oauth_credentials_user_id_foreign;
ALTER TABLE IF EXISTS ONLY public.data_contributions DROP CONSTRAINT IF EXISTS data_contributions_user_id_foreign;
ALTER TABLE IF EXISTS ONLY public.data_contributions DROP CONSTRAINT IF EXISTS data_contributions_data_category_id_foreign;
DROP INDEX IF EXISTS public.users_email_index;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_unique;
ALTER TABLE IF EXISTS ONLY public.oauth_credentials DROP CONSTRAINT IF EXISTS oauth_credentials_provider_id_user_id_unique;
ALTER TABLE IF EXISTS ONLY public.knex_migrations DROP CONSTRAINT IF EXISTS knex_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.data_contributions DROP CONSTRAINT IF EXISTS data_contributions_url_unique;
ALTER TABLE IF EXISTS ONLY public.data_contributions DROP CONSTRAINT IF EXISTS data_contributions_pkey;
ALTER TABLE IF EXISTS ONLY public.data_categories DROP CONSTRAINT IF EXISTS data_categories_pkey;
ALTER TABLE IF EXISTS ONLY public.data_categories DROP CONSTRAINT IF EXISTS data_categories_name_group_unique;
ALTER TABLE IF EXISTS public.knex_migrations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.data_categories ALTER COLUMN id DROP DEFAULT;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.oauth_credentials;
DROP TABLE IF EXISTS public.knex_migrations_lock;
DROP SEQUENCE IF EXISTS public.knex_migrations_id_seq;
DROP TABLE IF EXISTS public.knex_migrations;
DROP TABLE IF EXISTS public.data_contributions;
DROP SEQUENCE IF EXISTS public.data_categories_id_seq;
DROP TABLE IF EXISTS public.data_categories;
DROP EXTENSION IF EXISTS plpgsql;
DROP SCHEMA IF EXISTS public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: data_categories; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE data_categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "group" text
);


--
-- Name: data_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE data_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: data_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE data_categories_id_seq OWNED BY data_categories.id;


--
-- Name: data_contributions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE data_contributions (
    id uuid NOT NULL,
    user_id uuid,
    trial_id uuid,
    data_url character varying(255),
    comments text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    approved boolean,
    curation_comments text,
    url character varying(255),
    data_category_id integer,
    document_id uuid
);


--
-- Name: knex_migrations; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE knex_migrations (
    id integer NOT NULL,
    name character varying(255),
    batch integer,
    migration_time timestamp with time zone
);


--
-- Name: knex_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE knex_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: knex_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE knex_migrations_id_seq OWNED BY knex_migrations.id;


--
-- Name: knex_migrations_lock; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE knex_migrations_lock (
    is_locked integer
);


--
-- Name: oauth_credentials; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE oauth_credentials (
    provider character varying(255) NOT NULL,
    id character varying(255) NOT NULL,
    user_id uuid NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE users (
    id uuid NOT NULL,
    email character varying(255),
    name character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    role text,
    CONSTRAINT users_role_check CHECK ((role = ANY (ARRAY['curator'::text, 'admin'::text])))
);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY data_categories ALTER COLUMN id SET DEFAULT nextval('data_categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY knex_migrations ALTER COLUMN id SET DEFAULT nextval('knex_migrations_id_seq'::regclass);


--
-- Name: data_categories_name_group_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY data_categories
    ADD CONSTRAINT data_categories_name_group_unique UNIQUE (name, "group");


--
-- Name: data_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY data_categories
    ADD CONSTRAINT data_categories_pkey PRIMARY KEY (id);


--
-- Name: data_contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY data_contributions
    ADD CONSTRAINT data_contributions_pkey PRIMARY KEY (id);


--
-- Name: data_contributions_url_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY data_contributions
    ADD CONSTRAINT data_contributions_url_unique UNIQUE (data_url);


--
-- Name: knex_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY knex_migrations
    ADD CONSTRAINT knex_migrations_pkey PRIMARY KEY (id);


--
-- Name: oauth_credentials_provider_id_user_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY oauth_credentials
    ADD CONSTRAINT oauth_credentials_provider_id_user_id_unique UNIQUE (provider, id, user_id);


--
-- Name: users_email_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_email_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX users_email_index ON users USING btree (email);


--
-- Name: data_contributions_data_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY data_contributions
    ADD CONSTRAINT data_contributions_data_category_id_foreign FOREIGN KEY (data_category_id) REFERENCES data_categories(id);


--
-- Name: data_contributions_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY data_contributions
    ADD CONSTRAINT data_contributions_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: oauth_credentials_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY oauth_credentials
    ADD CONSTRAINT oauth_credentials_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id);


--
-- PostgreSQL database dump complete
--

