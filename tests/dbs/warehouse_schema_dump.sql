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

DROP INDEX IF EXISTS public.ix_nct_9502f58393a4fc6d;
DROP INDEX IF EXISTS public.ix_jprn_4e2a0ce8f4508948;
DROP INDEX IF EXISTS public.ix_isrctn_5630355bbd51c4b7;
DROP INDEX IF EXISTS public.ix_gsk_ae14dbea0172b852;
DROP INDEX IF EXISTS public.ix_euctr_86a28cd2542cd0c4;
DROP INDEX IF EXISTS public.ix_actrn_9b88700fa823eea2;
ALTER TABLE IF EXISTS ONLY public.takeda DROP CONSTRAINT IF EXISTS takeda_pkey;
ALTER TABLE IF EXISTS ONLY public.takeda DROP CONSTRAINT IF EXISTS takeda_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.pubmed DROP CONSTRAINT IF EXISTS pubmed_pkey;
ALTER TABLE IF EXISTS ONLY public.pubmed DROP CONSTRAINT IF EXISTS pubmed_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.pfizer DROP CONSTRAINT IF EXISTS pfizer_pkey;
ALTER TABLE IF EXISTS ONLY public.pfizer DROP CONSTRAINT IF EXISTS pfizer_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.nct DROP CONSTRAINT IF EXISTS nct_pkey;
ALTER TABLE IF EXISTS ONLY public.nct DROP CONSTRAINT IF EXISTS nct_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.jprn DROP CONSTRAINT IF EXISTS jprn_pkey;
ALTER TABLE IF EXISTS ONLY public.jprn DROP CONSTRAINT IF EXISTS jprn_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.isrctn DROP CONSTRAINT IF EXISTS isrctn_pkey;
ALTER TABLE IF EXISTS ONLY public.isrctn DROP CONSTRAINT IF EXISTS isrctn_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.ictrp DROP CONSTRAINT IF EXISTS ictrp_pkey;
ALTER TABLE IF EXISTS ONLY public.ictrp DROP CONSTRAINT IF EXISTS ictrp_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.icdpcs DROP CONSTRAINT IF EXISTS icdpcs_pkey;
ALTER TABLE IF EXISTS ONLY public.icdpcs DROP CONSTRAINT IF EXISTS icdpcs_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.icdcm DROP CONSTRAINT IF EXISTS icdcm_pkey;
ALTER TABLE IF EXISTS ONLY public.icdcm DROP CONSTRAINT IF EXISTS icdcm_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.hra DROP CONSTRAINT IF EXISTS hra_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.gsk DROP CONSTRAINT IF EXISTS gsk_pkey;
ALTER TABLE IF EXISTS ONLY public.gsk DROP CONSTRAINT IF EXISTS gsk_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.fdadl DROP CONSTRAINT IF EXISTS fda_pkey;
ALTER TABLE IF EXISTS ONLY public.fdadl DROP CONSTRAINT IF EXISTS fda_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.fda_dap DROP CONSTRAINT IF EXISTS fda_dap_meta_id_key;
ALTER TABLE IF EXISTS ONLY public.fda_dap DROP CONSTRAINT IF EXISTS fda_dap_id_key;
ALTER TABLE IF EXISTS ONLY public.euctr DROP CONSTRAINT IF EXISTS euctr_pkey;
ALTER TABLE IF EXISTS ONLY public.euctr DROP CONSTRAINT IF EXISTS euctr_meta_id_unique;
ALTER TABLE IF EXISTS ONLY public.cochrane_reviews DROP CONSTRAINT IF EXISTS cochrane_reviews_pkey;
ALTER TABLE IF EXISTS ONLY public.actrn DROP CONSTRAINT IF EXISTS actrn_pkey;
ALTER TABLE IF EXISTS ONLY public.actrn DROP CONSTRAINT IF EXISTS actrn_meta_id_unique;
DROP TABLE IF EXISTS public.takeda;
DROP TABLE IF EXISTS public.pubmed;
DROP TABLE IF EXISTS public.pfizer;
DROP TABLE IF EXISTS public.nct;
DROP TABLE IF EXISTS public.jprn;
DROP TABLE IF EXISTS public.isrctn;
DROP TABLE IF EXISTS public.ictrp;
DROP TABLE IF EXISTS public.icdpcs;
DROP TABLE IF EXISTS public.icdcm;
DROP TABLE IF EXISTS public.hra;
DROP TABLE IF EXISTS public.gsk;
DROP TABLE IF EXISTS public.fdadl;
DROP TABLE IF EXISTS public.fda_dap;
DROP TABLE IF EXISTS public.euctr;
DROP TABLE IF EXISTS public.cochrane_reviews;
DROP TABLE IF EXISTS public.alembic_version;
DROP TABLE IF EXISTS public.actrn;
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
-- Name: actrn; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE actrn (
    trial_id character varying(255) NOT NULL,
    scientific_title text,
    comparator_control_treatment text,
    selection text,
    attachments text[],
    public_title text,
    maximum_age text,
    actual_date_of_first_participant_enrolment date,
    can_healthy_volunteers_participate boolean,
    duration text,
    ethics_applications jsonb,
    type_of_registration text,
    key_exclusion_criteria text,
    meta_updated timestamp with time zone,
    key_inclusion_criteria text,
    meta_created timestamp with time zone,
    public_queries jsonb,
    target_follow_up_type text,
    meta_source text,
    actual_date_last_participant_enrolled date,
    health_conditions_or_problems_studied text,
    study_type text,
    primary_outcomes jsonb,
    patient_registry boolean,
    target_sample_size integer,
    scientific_queries jsonb,
    condition_code text,
    meta_id uuid,
    description_of_intervention_s_exposure text,
    trial_related_presentations_publications text,
    date_submitted date,
    sponsors jsonb,
    minimum_age text,
    purpose text,
    timing text,
    date_registered date,
    secondary_ids text[],
    principal_investigator jsonb,
    secondary_outcomes jsonb,
    universal_trial_number_utn text,
    condition_category text,
    actual_sample_size integer,
    intervention_codes text[],
    control_group text,
    gender text,
    brief_summary text,
    ethics_application_status text,
    primary_sponsor jsonb,
    recruitment_status text,
    allocation_to_intervention text,
    anticipated_date_of_first_participant_enrolment date,
    purpose_of_the_study text,
    methods_used_to_generate_the_sequence_in_which_subjects_will_be text,
    masking_blinding text,
    phase text,
    who_is_are_masked_blinded text,
    recruitment_state_s text,
    type_of_endpoint_s text,
    intervention_assignment text,
    procedure_for_enrolling_a_subject_and_allocating_the_treatment_ text,
    anticipated_date_last_participant_enrolled date,
    trial_website text,
    statistical_methods_analysis text,
    other_design_features text,
    trial_acronym text,
    target_follow_up_duration integer,
    public_notes text
);


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: cochrane_reviews; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cochrane_reviews (
    meta_id text,
    meta_created timestamp with time zone DEFAULT now(),
    meta_updated timestamp with time zone DEFAULT now(),
    meta_source text,
    id uuid NOT NULL,
    study_type text,
    file_name text,
    robs jsonb,
    study_id text,
    refs jsonb,
    doi_id text
);


--
-- Name: euctr; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE euctr (
    eudract_number_with_country character varying(255) NOT NULL,
    date_of_competent_authority_decision date,
    trial_dose_response boolean,
    trial_others boolean,
    trial_the_trial_involves_single_site_in_the_member_state_concer boolean,
    subject_women_of_childbearing_potential_not_using_contraception boolean,
    clinical_trial_type text,
    trial_is_part_of_a_paediatric_investigation_plan boolean,
    trial_open boolean,
    trial_cross_over boolean,
    placebos jsonb,
    member_state_concerned text,
    trial_primary_end_point_s text,
    trial_trial_being_conducted_both_within_and_outside_the_eea boolean,
    trial_therapy boolean,
    trial_single_blind boolean,
    trial_secondary_objectives_of_the_trial text,
    end_of_trial_status text,
    ethics_committee_opinion_of_the_trial_application text,
    trial_the_trial_involves_multiple_sites_in_the_member_state_con boolean,
    meta_updated timestamp with time zone,
    trial_trial_contains_a_sub_study boolean,
    trial_prophylaxis boolean,
    meta_created timestamp with time zone,
    trial_therapeutic_use_phase_iv boolean,
    national_competent_authority text,
    subject_pregnant_women boolean,
    eudract_number text,
    subject_male boolean,
    meta_source text,
    trial_in_the_member_state_concerned_years integer,
    trial_safety boolean,
    trial_therapeutic_exploratory_phase_ii boolean,
    trial_diagnosis boolean,
    trial_human_pharmacology_phase_i boolean,
    trial_bioequivalence_study boolean,
    subject_healthy_volunteers boolean,
    trial_the_trial_involves_multiple_member_states boolean,
    trial_efficacy boolean,
    trial_principal_exclusion_criteria text,
    meta_id uuid,
    trial_medical_condition_s_being_investigated text,
    trial_pharmacogenomic boolean,
    trial_bioequivalence boolean,
    trial_pharmacodynamic boolean,
    sponsors jsonb,
    sponsor_s_protocol_code_number text,
    trial_first_administration_to_humans boolean,
    trial_pharmacogenetic boolean,
    trial_therapeutic_confirmatory_phase_iii boolean,
    subject_in_the_member_state integer,
    date_on_which_this_record_was_first_entered_in_the_eudract_data date,
    subject_others boolean,
    trial_controlled boolean,
    trial_trial_being_conducted_completely_outside_of_the_eea boolean,
    trial_placebo boolean,
    subject_subjects_incapable_of_giving_consent_personally boolean,
    subject_in_the_eea integer,
    subject_women_of_childbearing_potential_using_contraception boolean,
    trial_principal_inclusion_criteria text,
    imps jsonb,
    trial_parallel_group boolean,
    trial_pharmacoeconomic boolean,
    trial_status text,
    trial_condition_being_studied_is_a_rare_disease text,
    subject_in_the_whole_clinical_trial integer,
    trial_other_medicinal_product_s boolean,
    competent_authority_decision text,
    subject_female boolean,
    trial_pharmacokinetic boolean,
    full_title_of_the_trial text,
    trial_in_all_countries_concerned_by_the_trial_years integer,
    subject_nursing_women boolean,
    trial_double_blind boolean,
    trial_trial_has_a_data_monitoring_committee boolean,
    subject_emergency_situation boolean,
    trial_randomised boolean,
    subject_specific_vulnerable_populations boolean,
    subject_patients boolean,
    trial_main_objective_of_the_trial text,
    date_of_ethics_committee_opinion date,
    trial_in_all_countries_concerned_by_the_trial_months integer,
    trial_definition_of_the_end_of_the_trial_and_justification_wher text,
    trial_in_the_member_state_concerned_months integer,
    name_or_abbreviated_title_of_the_trial_where_available text,
    subject_plans_for_treatment_or_care_after_the_subject_has_ended text,
    subject_details_of_subjects_incapable_of_giving_consent text,
    trial_version text,
    trial_level text,
    trial_classification_code text,
    isrctn_international_standard_randomised_controlled_trial_numbe text,
    trial_comparator_description text,
    trial_number_of_sites_anticipated_in_the_eea integer,
    date_of_the_global_end_of_the_trial date,
    trial_number_of_sites_anticipated_in_member_state_concerned integer,
    trial_term text,
    trial_other_trial_design_description text,
    trial_other_trial_type_description text,
    trial_other_scope_of_the_trial_description text,
    trial_full_title_date_and_version_of_each_sub_study_and_their_r text,
    trial_therapeutic_area text,
    trial_system_organ_class text,
    trial_number_of_treatment_arms_in_the_trial integer,
    trial_in_the_member_state_concerned_days integer,
    subject_childs integer,
    subject_details_of_other_specific_vulnerable_populations boolean,
    trial_in_all_countries_concerned_by_the_trial_days integer,
    subject_elderly integer,
    us_nct_clinicaltrials_gov_registry_number text,
    trial_medical_condition_in_easily_understood_language text,
    title_of_the_trial_for_lay_people_in_easily_understood_i_e_non_ text,
    subject_adults integer,
    trial_secondary_end_point_s text,
    trial_if_e_8_6_1_or_e_8_6_2_are_yes_specify_the_regions_in_whic text,
    trial_timepoint_s_of_evaluation_of_this_end_point text,
    ethics_committee_opinion_reason_s_for_unfavourable_opinion text,
    ema_decision_number_of_paediatric_investigation_plan text,
    trial_specify_the_countries_outside_of_the_eea_in_which_trial_s text,
    who_universal_trial_reference_number_utrn text,
    other_identifiers text,
    trial_results text,
    trial_other boolean,
    trial_results_url text
);


--
-- Name: fda_dap; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE fda_dap (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    id text,
    documents jsonb,
    approval_type text,
    supplement_number integer,
    action_date date,
    fda_application_num text,
    notes text,
    drug_name text,
    active_ingredients text,
    company text
);


--
-- Name: fdadl; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE fdadl (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    product_ndc text NOT NULL,
    product_type text,
    generic_name text,
    brand_name text,
    last_updated date,
    fda_application_number text
);


--
-- Name: gsk; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gsk (
    study_id character varying(255) NOT NULL,
    study_indication text,
    collaborators text[],
    meta_created timestamp with time zone,
    generic_name text,
    meta_source text,
    citation text,
    meta_id uuid,
    study_recruitment_status text,
    trade_name text,
    sponsor text,
    study_title text,
    meta_updated timestamp with time zone,
    record_verification_date date,
    last_updated date,
    eligibility_criteria text,
    first_received date,
    masked_subject boolean,
    overall_study_official_affiliation text,
    masked_investigator boolean,
    patient_level_data text,
    title text,
    masked_caregiver boolean,
    official_study_title text,
    responsible_party_organization text,
    conditions text[],
    responsible_party_name_official_title text,
    study_type text,
    clinical_study_id text,
    phase text,
    protocol_id text,
    masked_assessor boolean,
    overall_study_official text,
    overall_study_official_role text,
    study_indication_or_diseases text,
    publication_type text,
    clinicaltrials_gov_identifier text,
    trade_name_product_name text,
    study_indications text,
    maximum_age text,
    oversight_authority text[],
    keywords text[],
    contact_name text,
    study_completion_date date,
    ind_ide_protocol text,
    sampling_method text,
    fda_regulated_intervention boolean,
    primary_completion_date date,
    primary_outcomes jsonb,
    study_completion_date_type text,
    contact_phone text,
    status text,
    primary_completion_date_type text,
    ind_ide_number text,
    study_population text,
    time_perspective text,
    minimum_age text,
    contact_email text,
    study_start_date date,
    central_contact_phone text,
    central_contact text,
    study_design text,
    enrollment_type text,
    enrollment integer,
    ind_ide_serial_number text,
    healthy_volunteers boolean,
    biospecimen_retention text,
    gender text,
    brief_summary text,
    central_contact_email text,
    interventions jsonb,
    arms jsonb,
    primary_purpose text,
    detailed_description text,
    has_expanded_access boolean,
    study_classification_endpoint text,
    delayed_posting boolean,
    masking text,
    secondary_outcomes jsonb,
    allocation text,
    section_801_clinical_trial boolean,
    secondary_ids text[],
    study_design_assignment text,
    ind_ide_grantor text,
    acronym text,
    biospecimen_description text,
    why_study_stopped text,
    results_url text
);


--
-- Name: hra; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hra (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    hra_id text,
    publication_date date,
    updated_date date,
    comittee_name text,
    comittee_ref_number text,
    iras_proj_id text,
    contact_name text,
    contact_email text,
    application_title text,
    study_type_id text,
    study_type text,
    sponsor_org text,
    research_programme text,
    data_coll_arrangements text,
    establishment_org text,
    establishment_org_address_1 text,
    establishment_org_address_2 text,
    establishment_org_address_3 text,
    establishment_org_post_code text,
    decision text,
    decision_date timestamp with time zone,
    human_tissue_license text,
    rtb_title text,
    research_database_title text,
    application_full_title text,
    isrctn_id text,
    nct_id text,
    additional_ref_numbers text,
    duration_of_study_in_uk text,
    research_summary text,
    euctr_id text,
    social_value text,
    recuitment_arrangements text,
    risk_and_benefit text,
    participants_protection_and_care text,
    informed_consent text,
    applicant_and_staff_suitability text,
    independent_review text,
    supporting_info_suitability text,
    other_comments text,
    research_summary_suitability text
);


--
-- Name: icdcm; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE icdcm (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    name text NOT NULL,
    "desc" text,
    terms text[],
    version text,
    last_updated date
);


--
-- Name: icdpcs; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE icdpcs (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    code text NOT NULL,
    is_header boolean,
    short_description text,
    long_description text,
    version text,
    last_updated date
);


--
-- Name: ictrp; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ictrp (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    register text NOT NULL,
    last_refreshed_on date,
    main_id text NOT NULL,
    date_of_registration text,
    primary_sponsor text,
    public_title text,
    scientific_title text,
    date_of_first_enrollment text,
    target_sample_size integer,
    recruitment_status text,
    url text,
    study_type text,
    study_design text,
    study_phase text,
    countries_of_recruitment text[],
    contacts jsonb,
    key_inclusion_exclusion_criteria text,
    health_conditions_or_problems_studied text[],
    interventions text[],
    primary_outcomes text[],
    secondary_outcomes text[],
    secondary_ids text[],
    sources_of_monetary_support text[],
    secondary_sponsors text[]
);


--
-- Name: isrctn; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE isrctn (
    isrctn_id character varying(255) NOT NULL,
    scientific_title text,
    target_number_of_participants text,
    participant_inclusion_criteria text,
    protocol_serial_number text,
    clinicaltrials_gov_number text,
    funders jsonb,
    prospective_retrospective text,
    age_group text,
    participant_level_data text,
    date_assigned date,
    intervention text,
    meta_created timestamp with time zone,
    participant_exclusion_criteria text,
    eudract_number text,
    title text,
    meta_source text,
    recruitment_start_date date,
    trial_setting text,
    secondary_outcome_measures text,
    study_hypothesis text,
    meta_updated timestamp with time zone,
    intention_to_publish_date date,
    meta_id uuid,
    ethics_approval text,
    acronym text,
    trial_participating_centre text,
    plain_english_summary text,
    sponsors jsonb,
    overall_trial_start_date date,
    overall_trial_status text,
    recruitment_status text,
    doi_isrctn_id text,
    last_edited date,
    overall_trial_end_date date,
    condition text,
    trial_type text,
    secondary_study_design text,
    study_design text,
    countries_of_recruitment text,
    intervention_type text,
    gender text,
    contacts jsonb,
    primary_outcome_measures text,
    date_applied date,
    recruitment_end_date date,
    condition_category text,
    participant_type text,
    patient_information_sheet text,
    publication_and_dissemination_plan text,
    primary_study_design text,
    trial_website text,
    publication_summary text,
    phase text,
    drug_names text,
    reason_abandoned text,
    publication_citations text,
    results_basic_reporting text
);


--
-- Name: jprn; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE jprn (
    unique_trial_number character varying(255) NOT NULL,
    control text,
    type_of_intervention text,
    source_of_funding text,
    interventions text[],
    secondary_study_ids boolean,
    condition text,
    agelower_limit text,
    research_tel text,
    ageupper_limit text,
    date_of_formal_registrationdate_of_icmje_and_who date,
    anticipated_trial_start_date date,
    key_exclusion_criteria text,
    research_division_name text,
    meta_created timestamp with time zone,
    title_of_the_study_brief_title text,
    basic_objectives2 text,
    meta_source text,
    randomization text,
    research_organization text,
    key_inclusion_criteria text,
    date_of_registration date,
    primary_outcomes text,
    date_and_time_of_last_update timestamp with time zone,
    date_of_last_update timestamp with time zone,
    target_sample_size integer,
    classification_by_specialty text,
    meta_updated timestamp with time zone,
    narrative_objectives1 text,
    urljapanese text,
    meta_id uuid,
    no_of_arms integer,
    public_name_of_contact_person text,
    study_type text,
    official_scientific_title_of_the_study text,
    genomic_information boolean,
    recruitment_status text,
    category_of_org text,
    title_of_the_study text,
    research_name_of_lead_principal_investigator text,
    research_email text,
    blinding text,
    urlenglish text,
    gender text,
    region text,
    publication_of_results text,
    name_of_primary_sponsor text,
    classification_by_malignancy text,
    basic_design text,
    purpose_of_intervention text,
    research_address text,
    date_of_protocol_fixation date,
    dynamic_allocation text,
    trial_characteristics_2 text,
    nation_of_funding text,
    concealment text,
    trial_characteristics_1 text,
    developmental_phase text,
    last_followup_date date,
    randomization_unit text,
    key_secondary_outcomes text,
    institution_consideration text,
    institutions text,
    cosponsor text,
    stratification text,
    blocking text,
    url_releasing_results text,
    basic_objectives_others text,
    other_related_information text,
    date_analysis_concluded date,
    date_of_closure_to_data_entry date,
    date_trial_data_considered_complete date,
    results text,
    public_email text,
    public_tel text,
    public_homepage_url text,
    name_of_secondary_funers text,
    url_releasing_protocol text,
    secondary_study_id_1 text,
    org_issuing_secondary_study_id_1 text,
    research_homepage_url text,
    ind_to_mhlw text,
    org_issuing_secondary_study_id_2 text,
    secondary_study_id_2 text,
    public_division_name text,
    public_address text,
    public_organization text
);


--
-- Name: nct; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE nct (
    nct_id character varying(255) NOT NULL,
    is_fda_regulated boolean,
    interventions jsonb,
    link_text text,
    locations jsonb,
    responsible_party jsonb,
    keywords text[],
    has_expanded_access boolean,
    meta_created timestamp with time zone,
    source text,
    overall_contact jsonb,
    meta_source text,
    eligibility jsonb,
    primary_outcomes jsonb,
    org_study_id text,
    enrollment_anticipated integer,
    conditions text[],
    start_date date,
    arm_groups jsonb,
    meta_id uuid,
    download_date text,
    acronym text,
    sponsors jsonb,
    study_type text,
    study_design text,
    overall_status text,
    phase text,
    firstreceived_date date,
    meta_updated timestamp with time zone,
    location_countries text[],
    url text,
    condition_browse jsonb,
    oversight_info jsonb,
    number_of_groups integer,
    official_title text,
    intervention_browse jsonb,
    brief_title text,
    verification_date date,
    brief_summary text,
    lastchanged_date date,
    is_section_801 boolean,
    detailed_description text,
    overall_officials jsonb,
    secondary_outcomes jsonb,
    secondary_ids text[],
    number_of_arms integer,
    biospec_retention text,
    links jsonb,
    other_outcomes jsonb,
    overall_contact_backup jsonb,
    enrollment_actual integer,
    primary_completion_date_actual date,
    primary_completion_date_anticipated date,
    completion_date_anticipated date,
    completion_date_actual date,
    "references" jsonb,
    target_duration text,
    results_references jsonb,
    why_stopped text,
    firstreceived_results_date date,
    clinical_results jsonb,
    nct_aliases text[],
    removed_countries text[],
    biospec_desrc text,
    results_exemption_date date
);


--
-- Name: pfizer; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pfizer (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    title text,
    study_type text,
    organization_id text,
    nct_id text NOT NULL,
    status text,
    study_start_date date,
    study_end_date date,
    eligibility_criteria text,
    gender text,
    age_range text,
    healthy_volunteers_allowed boolean
);


--
-- Name: pubmed; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pubmed (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    pmid text NOT NULL,
    date_created date,
    date_completed date,
    date_revised date,
    country text,
    medline_ta text,
    nlm_unique_id text,
    issn_linking text,
    journal_issn text,
    journal_title text,
    journal_iso text,
    article_title text,
    article_abstract text,
    article_authors text[],
    article_language text,
    article_publication_type_list text[],
    article_vernacular_title text,
    article_date date,
    publication_status text,
    identifiers_list jsonb,
    mesh_headings jsonb
);


--
-- Name: takeda; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE takeda (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone,
    meta_updated timestamp with time zone,
    official_title text,
    takeda_trial_id text NOT NULL,
    trial_phase text,
    condition text,
    compound text[],
    recruitment_status text,
    nct_number text,
    trial_type text,
    other_trial_ids text,
    acronym text,
    brief_summary text,
    detailed_description text,
    trial_design text,
    primary_outcome_measures text,
    secondary_outcome_measures text,
    trial_arms_groups_or_cohorts text,
    gender text,
    ages text,
    enrollment_number_of_participants integer,
    locations text[],
    responsible_party text,
    trial_sponsor text,
    start_date date,
    completion_date date,
    eligibility_criteria text,
    download_the_clinical_trial_summary text,
    other_available_languages text
);


--
-- Name: actrn_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY actrn
    ADD CONSTRAINT actrn_meta_id_unique UNIQUE (meta_id);


--
-- Name: actrn_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY actrn
    ADD CONSTRAINT actrn_pkey PRIMARY KEY (trial_id);


--
-- Name: cochrane_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cochrane_reviews
    ADD CONSTRAINT cochrane_reviews_pkey PRIMARY KEY (id);


--
-- Name: euctr_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY euctr
    ADD CONSTRAINT euctr_meta_id_unique UNIQUE (meta_id);


--
-- Name: euctr_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY euctr
    ADD CONSTRAINT euctr_pkey PRIMARY KEY (eudract_number_with_country);


--
-- Name: fda_dap_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fda_dap
    ADD CONSTRAINT fda_dap_id_key UNIQUE (id);


--
-- Name: fda_dap_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fda_dap
    ADD CONSTRAINT fda_dap_meta_id_key UNIQUE (meta_id);


--
-- Name: fda_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fdadl
    ADD CONSTRAINT fda_meta_id_key UNIQUE (meta_id);


--
-- Name: fda_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY fdadl
    ADD CONSTRAINT fda_pkey PRIMARY KEY (product_ndc);


--
-- Name: gsk_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gsk
    ADD CONSTRAINT gsk_meta_id_unique UNIQUE (meta_id);


--
-- Name: gsk_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gsk
    ADD CONSTRAINT gsk_pkey PRIMARY KEY (study_id);


--
-- Name: hra_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hra
    ADD CONSTRAINT hra_meta_id_key UNIQUE (meta_id);


--
-- Name: icdcm_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY icdcm
    ADD CONSTRAINT icdcm_meta_id_key UNIQUE (meta_id);


--
-- Name: icdcm_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY icdcm
    ADD CONSTRAINT icdcm_pkey PRIMARY KEY (name);


--
-- Name: icdpcs_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY icdpcs
    ADD CONSTRAINT icdpcs_meta_id_key UNIQUE (meta_id);


--
-- Name: icdpcs_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY icdpcs
    ADD CONSTRAINT icdpcs_pkey PRIMARY KEY (code);


--
-- Name: ictrp_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ictrp
    ADD CONSTRAINT ictrp_meta_id_unique UNIQUE (meta_id);


--
-- Name: ictrp_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ictrp
    ADD CONSTRAINT ictrp_pkey PRIMARY KEY (main_id);


--
-- Name: isrctn_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY isrctn
    ADD CONSTRAINT isrctn_meta_id_unique UNIQUE (meta_id);


--
-- Name: isrctn_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY isrctn
    ADD CONSTRAINT isrctn_pkey PRIMARY KEY (isrctn_id);


--
-- Name: jprn_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY jprn
    ADD CONSTRAINT jprn_meta_id_unique UNIQUE (meta_id);


--
-- Name: jprn_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY jprn
    ADD CONSTRAINT jprn_pkey PRIMARY KEY (unique_trial_number);


--
-- Name: nct_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY nct
    ADD CONSTRAINT nct_meta_id_unique UNIQUE (meta_id);


--
-- Name: nct_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY nct
    ADD CONSTRAINT nct_pkey PRIMARY KEY (nct_id);


--
-- Name: pfizer_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pfizer
    ADD CONSTRAINT pfizer_meta_id_unique UNIQUE (meta_id);


--
-- Name: pfizer_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pfizer
    ADD CONSTRAINT pfizer_pkey PRIMARY KEY (nct_id);


--
-- Name: pubmed_meta_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pubmed
    ADD CONSTRAINT pubmed_meta_id_key UNIQUE (meta_id);


--
-- Name: pubmed_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pubmed
    ADD CONSTRAINT pubmed_pkey PRIMARY KEY (pmid);


--
-- Name: takeda_meta_id_unique; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY takeda
    ADD CONSTRAINT takeda_meta_id_unique UNIQUE (meta_id);


--
-- Name: takeda_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY takeda
    ADD CONSTRAINT takeda_pkey PRIMARY KEY (takeda_trial_id);


--
-- Name: ix_actrn_9b88700fa823eea2; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_actrn_9b88700fa823eea2 ON actrn USING btree (trial_id);


--
-- Name: ix_euctr_86a28cd2542cd0c4; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_euctr_86a28cd2542cd0c4 ON euctr USING btree (eudract_number_with_country);


--
-- Name: ix_gsk_ae14dbea0172b852; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_gsk_ae14dbea0172b852 ON gsk USING btree (study_id);


--
-- Name: ix_isrctn_5630355bbd51c4b7; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_isrctn_5630355bbd51c4b7 ON isrctn USING btree (isrctn_id);


--
-- Name: ix_jprn_4e2a0ce8f4508948; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_jprn_4e2a0ce8f4508948 ON jprn USING btree (unique_trial_number);


--
-- Name: ix_nct_9502f58393a4fc6d; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ix_nct_9502f58393a4fc6d ON nct USING btree (nct_id);


--
-- PostgreSQL database dump complete
--

