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

ALTER TABLE IF EXISTS ONLY public.trials DROP CONSTRAINT IF EXISTS trials_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_publications DROP CONSTRAINT IF EXISTS trials_publications_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_publications DROP CONSTRAINT IF EXISTS trials_publications_publication_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_conditions DROP CONSTRAINT IF EXISTS trials_problems_problem_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_persons DROP CONSTRAINT IF EXISTS trials_persons_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_persons DROP CONSTRAINT IF EXISTS trials_persons_person_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_organisations DROP CONSTRAINT IF EXISTS trials_organisations_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_organisations DROP CONSTRAINT IF EXISTS trials_organisations_organisation_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_locations DROP CONSTRAINT IF EXISTS trials_locations_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_locations DROP CONSTRAINT IF EXISTS trials_locations_location_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_interventions DROP CONSTRAINT IF EXISTS trials_interventions_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_interventions DROP CONSTRAINT IF EXISTS trials_interventions_intervention_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_documents DROP CONSTRAINT IF EXISTS trials_documents_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_documents DROP CONSTRAINT IF EXISTS trials_documents_document_id_foreign;
ALTER TABLE IF EXISTS ONLY public.trials_conditions DROP CONSTRAINT IF EXISTS trials_conditions_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.records DROP CONSTRAINT IF EXISTS trialrecords_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.records DROP CONSTRAINT IF EXISTS trialrecords_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases DROP CONSTRAINT IF EXISTS risk_of_biases_trial_id_foreign;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases DROP CONSTRAINT IF EXISTS risk_of_biases_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases_risk_of_bias_criterias DROP CONSTRAINT IF EXISTS risk_of_biases_risk_of_bias_criterias_risk_of_bias_id_foreign;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases_risk_of_bias_criterias DROP CONSTRAINT IF EXISTS risk_of_biases_risk_of_bias_criterias_risk_of_bias_criteria_id_;
ALTER TABLE IF EXISTS ONLY public.publications DROP CONSTRAINT IF EXISTS publications_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.conditions DROP CONSTRAINT IF EXISTS problems_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.persons DROP CONSTRAINT IF EXISTS persons_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.locations DROP CONSTRAINT IF EXISTS locations_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.interventions DROP CONSTRAINT IF EXISTS interventions_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.interventions DROP CONSTRAINT IF EXISTS interventions_fda_application_id_foreign;
ALTER TABLE IF EXISTS ONLY public.fda_approvals DROP CONSTRAINT IF EXISTS fda_approvals_fda_application_id_foreign;
ALTER TABLE IF EXISTS ONLY public.fda_applications DROP CONSTRAINT IF EXISTS fda_applications_organisation_id_foreign;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_source_id_foreign;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_file_id_foreign;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_fda_approval_id_foreign;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_document_category_id_foreign;
DROP INDEX IF EXISTS public.trials_documents_document_id_index;
DROP INDEX IF EXISTS public.trialrecords_trial_id_index;
DROP INDEX IF EXISTS public.records_identifiers_index;
DROP INDEX IF EXISTS public.interventions_fda_application_number_index;
DROP INDEX IF EXISTS public.fda_approvals_type_index;
ALTER TABLE IF EXISTS ONLY public.trials_publications DROP CONSTRAINT IF EXISTS trials_publications_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_conditions DROP CONSTRAINT IF EXISTS trials_problems_pkey;
ALTER TABLE IF EXISTS ONLY public.trials DROP CONSTRAINT IF EXISTS trials_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_persons DROP CONSTRAINT IF EXISTS trials_persons_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_organisations DROP CONSTRAINT IF EXISTS trials_organisations_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_locations DROP CONSTRAINT IF EXISTS trials_locations_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_interventions DROP CONSTRAINT IF EXISTS trials_interventions_pkey;
ALTER TABLE IF EXISTS ONLY public.trials_documents DROP CONSTRAINT IF EXISTS trials_documents_pkey;
ALTER TABLE IF EXISTS ONLY public.records DROP CONSTRAINT IF EXISTS trialrecords_pkey;
ALTER TABLE IF EXISTS ONLY public.sources DROP CONSTRAINT IF EXISTS sources_pkey;
ALTER TABLE IF EXISTS ONLY public.sources DROP CONSTRAINT IF EXISTS sources_name_type_unique;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases DROP CONSTRAINT IF EXISTS risk_of_biases_study_id_source_url_unique;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases_risk_of_bias_criterias DROP CONSTRAINT IF EXISTS risk_of_biases_risk_of_bias_criterias_pkey;
ALTER TABLE IF EXISTS ONLY public.risk_of_biases DROP CONSTRAINT IF EXISTS risk_of_biases_pkey;
ALTER TABLE IF EXISTS ONLY public.risk_of_bias_criterias DROP CONSTRAINT IF EXISTS risk_of_bias_criterias_pkey;
ALTER TABLE IF EXISTS ONLY public.risk_of_bias_criterias DROP CONSTRAINT IF EXISTS risk_of_bias_criterias_name_unique;
ALTER TABLE IF EXISTS ONLY public.records DROP CONSTRAINT IF EXISTS records_source_url_unique;
ALTER TABLE IF EXISTS ONLY public.publications DROP CONSTRAINT IF EXISTS publications_slug_unique;
ALTER TABLE IF EXISTS ONLY public.publications DROP CONSTRAINT IF EXISTS publications_pkey;
ALTER TABLE IF EXISTS ONLY public.conditions DROP CONSTRAINT IF EXISTS problems_slug_unique;
ALTER TABLE IF EXISTS ONLY public.conditions DROP CONSTRAINT IF EXISTS problems_pkey;
ALTER TABLE IF EXISTS ONLY public.persons DROP CONSTRAINT IF EXISTS persons_slug_unique;
ALTER TABLE IF EXISTS ONLY public.persons DROP CONSTRAINT IF EXISTS persons_pkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_slug_unique;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_pkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_name_unique;
ALTER TABLE IF EXISTS ONLY public.locations DROP CONSTRAINT IF EXISTS locations_slug_unique;
ALTER TABLE IF EXISTS ONLY public.locations DROP CONSTRAINT IF EXISTS locations_pkey;
ALTER TABLE IF EXISTS ONLY public.locations DROP CONSTRAINT IF EXISTS locations_name_type_unique;
ALTER TABLE IF EXISTS ONLY public.knex_migrations DROP CONSTRAINT IF EXISTS knex_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.interventions DROP CONSTRAINT IF EXISTS interventions_slug_unique;
ALTER TABLE IF EXISTS ONLY public.interventions DROP CONSTRAINT IF EXISTS interventions_pkey;
ALTER TABLE IF EXISTS ONLY public.interventions DROP CONSTRAINT IF EXISTS interventions_name_type_unique;
ALTER TABLE IF EXISTS ONLY public.files DROP CONSTRAINT IF EXISTS files_source_url_unique;
ALTER TABLE IF EXISTS ONLY public.files DROP CONSTRAINT IF EXISTS files_sha1_unique;
ALTER TABLE IF EXISTS ONLY public.files DROP CONSTRAINT IF EXISTS files_pkey;
ALTER TABLE IF EXISTS ONLY public.files DROP CONSTRAINT IF EXISTS files_documentcloud_id_unique;
ALTER TABLE IF EXISTS ONLY public.fda_approvals DROP CONSTRAINT IF EXISTS fda_approvals_pkey;
ALTER TABLE IF EXISTS ONLY public.fda_approvals DROP CONSTRAINT IF EXISTS fda_approvals_fda_application_id_supplement_number_unique;
ALTER TABLE IF EXISTS ONLY public.fda_applications DROP CONSTRAINT IF EXISTS fda_applications_pkey;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_pkey;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_fda_approval_id_file_id_name_unique;
ALTER TABLE IF EXISTS ONLY public.document_categories DROP CONSTRAINT IF EXISTS document_categories_pkey;
ALTER TABLE IF EXISTS ONLY public.document_categories DROP CONSTRAINT IF EXISTS document_categories_name_group_unique;
ALTER TABLE IF EXISTS public.knex_migrations ALTER COLUMN id DROP DEFAULT;
DROP TABLE IF EXISTS public.trials_publications;
DROP TABLE IF EXISTS public.trials_persons;
DROP TABLE IF EXISTS public.trials_organisations;
DROP TABLE IF EXISTS public.trials_locations;
DROP TABLE IF EXISTS public.trials_interventions;
DROP TABLE IF EXISTS public.trials_documents;
DROP TABLE IF EXISTS public.trials_conditions;
DROP TABLE IF EXISTS public.trials;
DROP TABLE IF EXISTS public.sources;
DROP TABLE IF EXISTS public.risk_of_biases_risk_of_bias_criterias;
DROP TABLE IF EXISTS public.risk_of_biases;
DROP TABLE IF EXISTS public.risk_of_bias_criterias;
DROP TABLE IF EXISTS public.records;
DROP TABLE IF EXISTS public.publications;
DROP TABLE IF EXISTS public.persons;
DROP TABLE IF EXISTS public.organisations;
DROP TABLE IF EXISTS public.locations;
DROP TABLE IF EXISTS public.knex_migrations_lock;
DROP SEQUENCE IF EXISTS public.knex_migrations_id_seq;
DROP TABLE IF EXISTS public.knex_migrations;
DROP TABLE IF EXISTS public.interventions;
DROP TABLE IF EXISTS public.files;
DROP TABLE IF EXISTS public.fda_approvals;
DROP TABLE IF EXISTS public.fda_applications;
DROP TABLE IF EXISTS public.documents;
DROP TABLE IF EXISTS public.document_categories;
DROP TABLE IF EXISTS public.conditions;
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
-- Name: conditions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE conditions (
    id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_id text,
    slug text,
    description text,
    icdcm_code text
);


--
-- Name: document_categories; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE document_categories (
    id integer NOT NULL,
    name text NOT NULL,
    "group" text
);


--
-- Name: documents; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE documents (
    id uuid NOT NULL,
    source_id text,
    name text NOT NULL,
    fda_approval_id text,
    file_id uuid,
    source_url text,
    document_category_id integer NOT NULL,
    CONSTRAINT file_id_xor_source_url_check CHECK ((((file_id IS NULL) AND (source_url IS NOT NULL)) OR ((file_id IS NOT NULL) AND (source_url IS NULL))))
);


--
-- Name: fda_applications; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE fda_applications (
    id text NOT NULL,
    organisation_id uuid,
    drug_name text,
    active_ingredients text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: fda_approvals; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE fda_approvals (
    id text NOT NULL,
    supplement_number integer NOT NULL,
    type text NOT NULL,
    action_date date NOT NULL,
    notes text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    fda_application_id text NOT NULL
);


--
-- Name: files; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE files (
    id uuid NOT NULL,
    documentcloud_id text,
    sha1 text NOT NULL,
    source_url text NOT NULL,
    pages text[]
);


--
-- Name: interventions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE interventions (
    id uuid NOT NULL,
    name text NOT NULL,
    type text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_id text,
    slug text,
    description text,
    icdpcs_code text,
    ndc_code text,
    fda_application_id text,
    CONSTRAINT interventions_type_check CHECK ((type = ANY (ARRAY['drug'::text, 'procedure'::text, 'other'::text])))
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
-- Name: locations; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE locations (
    id uuid NOT NULL,
    name text NOT NULL,
    type text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_id text,
    slug text,
    CONSTRAINT locations_type_check CHECK ((type = ANY (ARRAY['country'::text, 'city'::text, 'other'::text])))
);


--
-- Name: organisations; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE organisations (
    id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_id text,
    slug text
);


--
-- Name: persons; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE persons (
    id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_id text,
    slug text
);


--
-- Name: publications; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE publications (
    id uuid NOT NULL,
    source_id text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_url text NOT NULL,
    title text NOT NULL,
    abstract text NOT NULL,
    authors text[],
    journal text,
    date date,
    slug text
);


--
-- Name: records; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE records (
    id uuid NOT NULL,
    source_id text NOT NULL,
    source_url text NOT NULL,
    identifiers jsonb NOT NULL,
    registration_date date,
    public_title text NOT NULL,
    brief_summary text,
    scientific_title text,
    description text,
    recruitment_status text,
    eligibility_criteria jsonb,
    target_sample_size integer,
    first_enrollment_date date,
    study_type text,
    study_design text,
    study_phase text,
    primary_outcomes jsonb,
    secondary_outcomes jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    has_published_results boolean,
    gender text,
    trial_id uuid,
    status text,
    completion_date date,
    results_exemption_date date,
    last_verification_date date,
    is_primary boolean DEFAULT false,
    CONSTRAINT records_recruitment_status_check CHECK ((recruitment_status = ANY (ARRAY['recruiting'::text, 'not_recruiting'::text, 'unknown'::text, 'other'::text]))),
    CONSTRAINT records_status_check CHECK ((status = ANY (ARRAY['ongoing'::text, 'withdrawn'::text, 'suspended'::text, 'terminated'::text, 'complete'::text, 'other'::text]))),
    CONSTRAINT trialrecords_gender_check CHECK ((gender = ANY (ARRAY['both'::text, 'male'::text, 'female'::text])))
);

--
-- Name: risk_of_bias_criterias; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE risk_of_bias_criterias (
    id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: risk_of_biases; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE risk_of_biases (
    id uuid NOT NULL,
    trial_id uuid NOT NULL,
    source_id text NOT NULL,
    source_url text NOT NULL,
    study_id text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: risk_of_biases_risk_of_bias_criterias; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE risk_of_biases_risk_of_bias_criterias (
    risk_of_bias_id uuid NOT NULL,
    risk_of_bias_criteria_id uuid NOT NULL,
    value text NOT NULL,
    CONSTRAINT risk_of_biases_risk_of_bias_criterias_value_check CHECK ((value = ANY (ARRAY['yes'::text, 'no'::text, 'unknown'::text])))
);


--
-- Name: sources; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE sources (
    id text NOT NULL,
    name text NOT NULL,
    type text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    source_url text,
    terms_and_conditions_url text,
    CONSTRAINT sources_type_check CHECK ((type = ANY (ARRAY['register'::text, 'other'::text])))
);

--
-- Name: trials; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials (
    id uuid NOT NULL,
    identifiers jsonb NOT NULL,
    registration_date date,
    public_title text NOT NULL,
    brief_summary text,
    scientific_title text,
    description text,
    recruitment_status text,
    eligibility_criteria jsonb,
    target_sample_size integer,
    first_enrollment_date date,
    study_type text,
    study_design text,
    study_phase text,
    primary_outcomes jsonb,
    secondary_outcomes jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    has_published_results boolean,
    gender text,
    source_id text,
    status text,
    completion_date date,
    results_exemption_date date,
    CONSTRAINT trials_gender_check CHECK ((gender = ANY (ARRAY['both'::text, 'male'::text, 'female'::text]))),
    CONSTRAINT trials_recruitment_status_check CHECK ((recruitment_status = ANY (ARRAY['recruiting'::text, 'not_recruiting'::text, 'unknown'::text, 'other'::text]))),
    CONSTRAINT trials_status_check CHECK ((status = ANY (ARRAY['ongoing'::text, 'withdrawn'::text, 'suspended'::text, 'terminated'::text, 'complete'::text, 'other'::text])))
);


--
-- Name: trials_conditions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_conditions (
    trial_id uuid NOT NULL,
    condition_id uuid NOT NULL
);


--
-- Name: trials_documents; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_documents (
    trial_id uuid NOT NULL,
    document_id uuid NOT NULL
);


--
-- Name: trials_interventions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_interventions (
    trial_id uuid NOT NULL,
    intervention_id uuid NOT NULL
);


--
-- Name: trials_locations; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_locations (
    trial_id uuid NOT NULL,
    location_id uuid NOT NULL,
    role text,
    CONSTRAINT trials_locations_role_check CHECK ((role = ANY (ARRAY['recruitment_countries'::text, 'other'::text])))
);


--
-- Name: trials_organisations; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_organisations (
    trial_id uuid NOT NULL,
    organisation_id uuid NOT NULL,
    role text,
    CONSTRAINT trials_organisations_role_check CHECK ((role = ANY (ARRAY['primary_sponsor'::text, 'sponsor'::text, 'funder'::text, 'other'::text])))
);


--
-- Name: trials_persons; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_persons (
    trial_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role text,
    CONSTRAINT trials_persons_role_check CHECK ((role = ANY (ARRAY['principal_investigator'::text, 'public_queries'::text, 'scientific_queries'::text, 'other'::text])))
);


--
-- Name: trials_publications; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE trials_publications (
    trial_id uuid NOT NULL,
    publication_id uuid NOT NULL
);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY knex_migrations ALTER COLUMN id SET DEFAULT nextval('knex_migrations_id_seq'::regclass);


--
-- Name: document_categories_name_group_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY document_categories
    ADD CONSTRAINT document_categories_name_group_unique UNIQUE (name, "group");


--
-- Name: document_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY document_categories
    ADD CONSTRAINT document_categories_pkey PRIMARY KEY (id);


--
-- Name: documents_fda_approval_id_file_id_name_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_fda_approval_id_file_id_name_unique UNIQUE (fda_approval_id, file_id, name);


--
-- Name: documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: fda_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fda_applications
    ADD CONSTRAINT fda_applications_pkey PRIMARY KEY (id);


--
-- Name: fda_approvals_fda_application_id_supplement_number_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fda_approvals
    ADD CONSTRAINT fda_approvals_fda_application_id_supplement_number_unique UNIQUE (fda_application_id, supplement_number);


--
-- Name: fda_approvals_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fda_approvals
    ADD CONSTRAINT fda_approvals_pkey PRIMARY KEY (id);


--
-- Name: files_documentcloud_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_documentcloud_id_unique UNIQUE (documentcloud_id);


--
-- Name: files_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: files_sha1_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_sha1_unique UNIQUE (sha1);


--
-- Name: files_source_url_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_source_url_unique UNIQUE (source_url);


--
-- Name: interventions_name_type_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY interventions
    ADD CONSTRAINT interventions_name_type_unique UNIQUE (name, type);


--
-- Name: interventions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY interventions
    ADD CONSTRAINT interventions_pkey PRIMARY KEY (id);


--
-- Name: interventions_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY interventions
    ADD CONSTRAINT interventions_slug_unique UNIQUE (slug);


--
-- Name: knex_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY knex_migrations
    ADD CONSTRAINT knex_migrations_pkey PRIMARY KEY (id);


--
-- Name: locations_name_type_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY locations
    ADD CONSTRAINT locations_name_type_unique UNIQUE (name, type);


--
-- Name: locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: locations_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY locations
    ADD CONSTRAINT locations_slug_unique UNIQUE (slug);


--
-- Name: organisations_name_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY organisations
    ADD CONSTRAINT organisations_name_unique UNIQUE (name);


--
-- Name: organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY organisations
    ADD CONSTRAINT organisations_pkey PRIMARY KEY (id);


--
-- Name: organisations_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY organisations
    ADD CONSTRAINT organisations_slug_unique UNIQUE (slug);


--
-- Name: persons_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- Name: persons_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_slug_unique UNIQUE (slug);


--
-- Name: problems_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY conditions
    ADD CONSTRAINT problems_pkey PRIMARY KEY (id);


--
-- Name: problems_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY conditions
    ADD CONSTRAINT problems_slug_unique UNIQUE (slug);


--
-- Name: publications_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (id);


--
-- Name: publications_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY publications
    ADD CONSTRAINT publications_slug_unique UNIQUE (slug);


--
-- Name: records_source_url_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY records
    ADD CONSTRAINT records_source_url_unique UNIQUE (source_url);


--
-- Name: risk_of_bias_criterias_name_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY risk_of_bias_criterias
    ADD CONSTRAINT risk_of_bias_criterias_name_unique UNIQUE (name);


--
-- Name: risk_of_bias_criterias_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY risk_of_bias_criterias
    ADD CONSTRAINT risk_of_bias_criterias_pkey PRIMARY KEY (id);


--
-- Name: risk_of_biases_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY risk_of_biases
    ADD CONSTRAINT risk_of_biases_pkey PRIMARY KEY (id);


--
-- Name: risk_of_biases_risk_of_bias_criterias_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY risk_of_biases_risk_of_bias_criterias
    ADD CONSTRAINT risk_of_biases_risk_of_bias_criterias_pkey PRIMARY KEY (risk_of_bias_id, risk_of_bias_criteria_id);


--
-- Name: risk_of_biases_study_id_source_url_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY risk_of_biases
    ADD CONSTRAINT risk_of_biases_study_id_source_url_unique UNIQUE (study_id, source_url);


--
-- Name: sources_name_type_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY sources
    ADD CONSTRAINT sources_name_type_unique UNIQUE (name, type);


--
-- Name: sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (id);


--
-- Name: trialrecords_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY records
    ADD CONSTRAINT trialrecords_pkey PRIMARY KEY (id);


--
-- Name: trials_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_documents
    ADD CONSTRAINT trials_documents_pkey PRIMARY KEY (trial_id, document_id);


--
-- Name: trials_interventions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_interventions
    ADD CONSTRAINT trials_interventions_pkey PRIMARY KEY (trial_id, intervention_id);


--
-- Name: trials_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_locations
    ADD CONSTRAINT trials_locations_pkey PRIMARY KEY (trial_id, location_id);


--
-- Name: trials_organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_organisations
    ADD CONSTRAINT trials_organisations_pkey PRIMARY KEY (trial_id, organisation_id);


--
-- Name: trials_persons_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_persons
    ADD CONSTRAINT trials_persons_pkey PRIMARY KEY (trial_id, person_id);


--
-- Name: trials_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials
    ADD CONSTRAINT trials_pkey PRIMARY KEY (id);


--
-- Name: trials_problems_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_conditions
    ADD CONSTRAINT trials_problems_pkey PRIMARY KEY (trial_id, condition_id);


--
-- Name: trials_publications_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY trials_publications
    ADD CONSTRAINT trials_publications_pkey PRIMARY KEY (trial_id, publication_id);


--
-- Name: fda_approvals_type_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX fda_approvals_type_index ON fda_approvals USING btree (type);


--
-- Name: interventions_fda_application_number_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX interventions_fda_application_number_index ON interventions USING btree (fda_application_id);


--
-- Name: records_identifiers_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX records_identifiers_index ON records USING gin (identifiers);


--
-- Name: trialrecords_trial_id_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX trialrecords_trial_id_index ON records USING btree (trial_id);


--
-- Name: trials_documents_document_id_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX trials_documents_document_id_index ON trials_documents USING btree (document_id);


--
-- Name: documents_document_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_document_category_id_foreign FOREIGN KEY (document_category_id) REFERENCES document_categories(id);


--
-- Name: documents_fda_approval_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_fda_approval_id_foreign FOREIGN KEY (fda_approval_id) REFERENCES fda_approvals(id);


--
-- Name: documents_file_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_file_id_foreign FOREIGN KEY (file_id) REFERENCES files(id);


--
-- Name: documents_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY documents
    ADD CONSTRAINT documents_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: fda_applications_organisation_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY fda_applications
    ADD CONSTRAINT fda_applications_organisation_id_foreign FOREIGN KEY (organisation_id) REFERENCES organisations(id);


--
-- Name: fda_approvals_fda_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY fda_approvals
    ADD CONSTRAINT fda_approvals_fda_application_id_foreign FOREIGN KEY (fda_application_id) REFERENCES fda_applications(id) ON UPDATE CASCADE;


--
-- Name: interventions_fda_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY interventions
    ADD CONSTRAINT interventions_fda_application_id_foreign FOREIGN KEY (fda_application_id) REFERENCES fda_applications(id) ON UPDATE CASCADE;


--
-- Name: interventions_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY interventions
    ADD CONSTRAINT interventions_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: locations_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY locations
    ADD CONSTRAINT locations_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: organisations_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY organisations
    ADD CONSTRAINT organisations_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: persons_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: problems_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY conditions
    ADD CONSTRAINT problems_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: publications_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY publications
    ADD CONSTRAINT publications_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: risk_of_biases_risk_of_bias_criterias_risk_of_bias_criteria_id_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY risk_of_biases_risk_of_bias_criterias
    ADD CONSTRAINT risk_of_biases_risk_of_bias_criterias_risk_of_bias_criteria_id_ FOREIGN KEY (risk_of_bias_criteria_id) REFERENCES risk_of_bias_criterias(id);


--
-- Name: risk_of_biases_risk_of_bias_criterias_risk_of_bias_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY risk_of_biases_risk_of_bias_criterias
    ADD CONSTRAINT risk_of_biases_risk_of_bias_criterias_risk_of_bias_id_foreign FOREIGN KEY (risk_of_bias_id) REFERENCES risk_of_biases(id);


--
-- Name: risk_of_biases_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY risk_of_biases
    ADD CONSTRAINT risk_of_biases_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id);


--
-- Name: risk_of_biases_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY risk_of_biases
    ADD CONSTRAINT risk_of_biases_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id);


--
-- Name: trialrecords_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY records
    ADD CONSTRAINT trialrecords_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- Name: trialrecords_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY records
    ADD CONSTRAINT trialrecords_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id);


--
-- Name: trials_conditions_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_conditions
    ADD CONSTRAINT trials_conditions_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_documents_document_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_documents
    ADD CONSTRAINT trials_documents_document_id_foreign FOREIGN KEY (document_id) REFERENCES documents(id);


--
-- Name: trials_documents_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_documents
    ADD CONSTRAINT trials_documents_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id);


--
-- Name: trials_interventions_intervention_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_interventions
    ADD CONSTRAINT trials_interventions_intervention_id_foreign FOREIGN KEY (intervention_id) REFERENCES interventions(id);


--
-- Name: trials_interventions_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_interventions
    ADD CONSTRAINT trials_interventions_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_locations_location_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_locations
    ADD CONSTRAINT trials_locations_location_id_foreign FOREIGN KEY (location_id) REFERENCES locations(id);


--
-- Name: trials_locations_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_locations
    ADD CONSTRAINT trials_locations_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_organisations_organisation_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_organisations
    ADD CONSTRAINT trials_organisations_organisation_id_foreign FOREIGN KEY (organisation_id) REFERENCES organisations(id);


--
-- Name: trials_organisations_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_organisations
    ADD CONSTRAINT trials_organisations_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_persons_person_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_persons
    ADD CONSTRAINT trials_persons_person_id_foreign FOREIGN KEY (person_id) REFERENCES persons(id);


--
-- Name: trials_persons_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_persons
    ADD CONSTRAINT trials_persons_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_problems_problem_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_conditions
    ADD CONSTRAINT trials_problems_problem_id_foreign FOREIGN KEY (condition_id) REFERENCES conditions(id);


--
-- Name: trials_publications_publication_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_publications
    ADD CONSTRAINT trials_publications_publication_id_foreign FOREIGN KEY (publication_id) REFERENCES publications(id);


--
-- Name: trials_publications_trial_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials_publications
    ADD CONSTRAINT trials_publications_trial_id_foreign FOREIGN KEY (trial_id) REFERENCES trials(id) ON DELETE CASCADE;


--
-- Name: trials_source_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY trials
    ADD CONSTRAINT trials_source_id_foreign FOREIGN KEY (source_id) REFERENCES sources(id) ON UPDATE CASCADE;


--
-- PostgreSQL database dump complete
--

