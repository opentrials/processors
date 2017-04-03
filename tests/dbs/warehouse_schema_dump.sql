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

DROP TRIGGER IF EXISTS takeda_set_meta_updated ON public.takeda;
DROP TRIGGER IF EXISTS pubmed_set_meta_updated ON public.pubmed;
DROP TRIGGER IF EXISTS pfizer_set_meta_updated ON public.pfizer;
DROP TRIGGER IF EXISTS nct_set_meta_updated ON public.nct;
DROP TRIGGER IF EXISTS jprn_set_meta_updated ON public.jprn;
DROP TRIGGER IF EXISTS isrctn_set_meta_updated ON public.isrctn;
DROP TRIGGER IF EXISTS ictrp_set_meta_updated ON public.ictrp;
DROP TRIGGER IF EXISTS icdpcs_set_meta_updated ON public.icdpcs;
DROP TRIGGER IF EXISTS icdcm_set_meta_updated ON public.icdcm;
DROP TRIGGER IF EXISTS hra_set_meta_updated ON public.hra;
DROP TRIGGER IF EXISTS gsk_set_meta_updated ON public.gsk;
DROP TRIGGER IF EXISTS fdadl_set_meta_updated ON public.fdadl;
DROP TRIGGER IF EXISTS fda_dap_set_meta_updated ON public.fda_dap;
DROP TRIGGER IF EXISTS euctr_set_meta_updated ON public.euctr;
DROP TRIGGER IF EXISTS cochrane_reviews_set_meta_updated ON public.cochrane_reviews;
DROP TRIGGER IF EXISTS actrn_set_meta_updated ON public.actrn;
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
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
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
DROP FUNCTION IF EXISTS public.set_meta_updated();
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

--
-- Name: set_meta_updated(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION set_meta_updated() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                    BEGIN
                      NEW.meta_updated := now();
                      RETURN NEW;
                    END;
                    $$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: actrn; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE actrn (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    trial_id text NOT NULL,
    ethics_application_status text,
    date_submitted date,
    date_registered date,
    type_of_registration text,
    public_title text,
    scientific_title text,
    secondary_ids text[],
    universal_trial_number_utn text,
    trial_acronym text,
    health_conditions_or_problems_studied text,
    condition_category text,
    condition_code text,
    study_type text,
    patient_registry boolean,
    target_follow_up_duration integer,
    target_follow_up_type text,
    description_of_intervention_s_exposure text,
    intervention_codes text[],
    comparator_control_treatment text,
    control_group text,
    primary_outcomes jsonb,
    secondary_outcomes jsonb,
    key_inclusion_criteria text,
    minimum_age text,
    maximum_age text,
    gender text,
    can_healthy_volunteers_participate boolean,
    key_exclusion_criteria text,
    purpose_of_the_study text,
    allocation_to_intervention text,
    procedure_for_enrolling_a_subject_and_allocating_the_treatment_ text,
    methods_used_to_generate_the_sequence_in_which_subjects_will_be text,
    masking_blinding text,
    who_is_are_masked_blinded text,
    intervention_assignment text,
    other_design_features text,
    phase text,
    type_of_endpoint_s text,
    purpose text,
    duration text,
    selection text,
    timing text,
    statistical_methods_analysis text,
    anticipated_date_of_first_participant_enrolment date,
    actual_date_of_first_participant_enrolment date,
    anticipated_date_last_participant_enrolled date,
    actual_date_last_participant_enrolled date,
    target_sample_size integer,
    actual_sample_size integer,
    recruitment_status text,
    recruitment_state_s text,
    primary_sponsor jsonb,
    sponsors jsonb,
    ethics_applications jsonb,
    brief_summary text,
    trial_website text,
    trial_related_presentations_publications text,
    public_notes text,
    attachments text[],
    principal_investigator jsonb,
    public_queries jsonb,
    scientific_queries jsonb
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    eudract_number_with_country text NOT NULL,
    other_identifiers text,
    national_competent_authority text,
    clinical_trial_type text,
    trial_status text,
    date_on_which_this_record_was_first_entered_in_the_eudract_data date,
    trial_results text,
    member_state_concerned text,
    eudract_number text,
    full_title_of_the_trial text,
    title_of_the_trial_for_lay_people_in_easily_understood_i_e_non_ text,
    name_or_abbreviated_title_of_the_trial_where_available text,
    sponsor_s_protocol_code_number text,
    us_nct_clinicaltrials_gov_registry_number text,
    who_universal_trial_reference_number_utrn text,
    isrctn_international_standard_randomised_controlled_trial_numbe text,
    trial_is_part_of_a_paediatric_investigation_plan boolean,
    ema_decision_number_of_paediatric_investigation_plan text,
    sponsors jsonb,
    imps jsonb,
    placebos jsonb,
    trial_medical_condition_s_being_investigated text,
    trial_medical_condition_in_easily_understood_language text,
    trial_therapeutic_area text,
    trial_version text,
    trial_level text,
    trial_classification_code text,
    trial_term text,
    trial_system_organ_class text,
    trial_condition_being_studied_is_a_rare_disease text,
    trial_main_objective_of_the_trial text,
    trial_secondary_objectives_of_the_trial text,
    trial_trial_contains_a_sub_study boolean,
    trial_full_title_date_and_version_of_each_sub_study_and_their_r text,
    trial_principal_inclusion_criteria text,
    trial_principal_exclusion_criteria text,
    trial_primary_end_point_s text,
    trial_timepoint_s_of_evaluation_of_this_end_point text,
    trial_secondary_end_point_s text,
    trial_diagnosis boolean,
    trial_prophylaxis boolean,
    trial_therapy boolean,
    trial_safety boolean,
    trial_efficacy boolean,
    trial_pharmacokinetic boolean,
    trial_pharmacodynamic boolean,
    trial_bioequivalence boolean,
    trial_dose_response boolean,
    trial_pharmacogenetic boolean,
    trial_pharmacogenomic boolean,
    trial_pharmacoeconomic boolean,
    trial_others boolean,
    trial_other_scope_of_the_trial_description text,
    trial_human_pharmacology_phase_i boolean,
    trial_first_administration_to_humans boolean,
    trial_bioequivalence_study boolean,
    trial_other_trial_type_description text,
    trial_other boolean,
    trial_therapeutic_exploratory_phase_ii boolean,
    trial_therapeutic_confirmatory_phase_iii boolean,
    trial_therapeutic_use_phase_iv boolean,
    trial_controlled boolean,
    trial_randomised boolean,
    trial_open boolean,
    trial_single_blind boolean,
    trial_double_blind boolean,
    trial_parallel_group boolean,
    trial_cross_over boolean,
    trial_other_trial_design_description text,
    trial_other_medicinal_product_s boolean,
    trial_placebo boolean,
    trial_comparator_description text,
    trial_number_of_treatment_arms_in_the_trial integer,
    trial_the_trial_involves_single_site_in_the_member_state_concer boolean,
    trial_the_trial_involves_multiple_sites_in_the_member_state_con boolean,
    trial_number_of_sites_anticipated_in_member_state_concerned integer,
    trial_the_trial_involves_multiple_member_states boolean,
    trial_number_of_sites_anticipated_in_the_eea integer,
    trial_trial_being_conducted_both_within_and_outside_the_eea boolean,
    trial_trial_being_conducted_completely_outside_of_the_eea boolean,
    trial_specify_the_countries_outside_of_the_eea_in_which_trial_s text,
    trial_if_e_8_6_1_or_e_8_6_2_are_yes_specify_the_regions_in_whic text,
    trial_trial_has_a_data_monitoring_committee boolean,
    trial_definition_of_the_end_of_the_trial_and_justification_wher text,
    trial_in_the_member_state_concerned_years integer,
    trial_in_the_member_state_concerned_months integer,
    trial_in_the_member_state_concerned_days integer,
    trial_in_all_countries_concerned_by_the_trial_years integer,
    trial_in_all_countries_concerned_by_the_trial_months integer,
    trial_in_all_countries_concerned_by_the_trial_days integer,
    subject_childs integer,
    subject_adults integer,
    subject_elderly integer,
    subject_female boolean,
    subject_male boolean,
    subject_healthy_volunteers boolean,
    subject_patients boolean,
    subject_specific_vulnerable_populations boolean,
    subject_women_of_childbearing_potential_not_using_contraception boolean,
    subject_women_of_childbearing_potential_using_contraception boolean,
    subject_pregnant_women boolean,
    subject_nursing_women boolean,
    subject_emergency_situation boolean,
    subject_subjects_incapable_of_giving_consent_personally boolean,
    subject_details_of_subjects_incapable_of_giving_consent text,
    subject_others boolean,
    subject_details_of_other_specific_vulnerable_populations boolean,
    subject_in_the_member_state integer,
    subject_in_the_eea integer,
    subject_in_the_whole_clinical_trial integer,
    subject_plans_for_treatment_or_care_after_the_subject_has_ended text,
    competent_authority_decision text,
    date_of_competent_authority_decision date,
    ethics_committee_opinion_of_the_trial_application text,
    ethics_committee_opinion_reason_s_for_unfavourable_opinion text,
    date_of_ethics_committee_opinion date,
    end_of_trial_status text,
    date_of_the_global_end_of_the_trial date,
    trial_results_url text
);


--
-- Name: fda_dap; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE fda_dap (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    study_id text NOT NULL,
    study_title text,
    patient_level_data text,
    clinicaltrials_gov_identifier text,
    sponsor text,
    collaborators text[],
    study_recruitment_status text,
    generic_name text,
    trade_name text,
    study_indication text,
    first_received date,
    last_updated date,
    title text,
    phase text,
    acronym text,
    secondary_ids text[],
    fda_regulated_intervention boolean,
    section_801_clinical_trial boolean,
    delayed_posting boolean,
    ind_ide_protocol text,
    ind_ide_grantor text,
    ind_ide_number text,
    ind_ide_serial_number text,
    has_expanded_access boolean,
    study_type text,
    oversight_authority text[],
    brief_summary text,
    detailed_description text,
    record_verification_date date,
    status text,
    why_study_stopped text,
    study_start_date date,
    study_completion_date date,
    study_completion_date_type text,
    primary_completion_date date,
    primary_completion_date_type text,
    primary_purpose text,
    study_design text,
    time_perspective text,
    biospecimen_retention text,
    biospecimen_description text,
    allocation text,
    masking text,
    masked_subject boolean,
    masked_caregiver boolean,
    masked_investigator boolean,
    masked_assessor boolean,
    study_design_assignment text,
    study_classification_endpoint text,
    primary_outcomes jsonb,
    secondary_outcomes jsonb,
    arms jsonb,
    interventions jsonb,
    conditions text[],
    keywords text[],
    study_population text,
    sampling_method text,
    eligibility_criteria text,
    gender text,
    minimum_age text,
    maximum_age text,
    enrollment integer,
    enrollment_type text,
    healthy_volunteers boolean,
    central_contact text,
    central_contact_phone text,
    central_contact_email text,
    overall_study_official text,
    overall_study_official_affiliation text,
    overall_study_official_role text,
    responsible_party_name_official_title text,
    responsible_party_organization text,
    contact_name text,
    contact_phone text,
    contact_email text,
    protocol_id text,
    clinical_study_id text,
    official_study_title text,
    study_indication_or_diseases text,
    trade_name_product_name text,
    study_indications text,
    citation text,
    publication_type text,
    results_url text
);


--
-- Name: hra; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE hra (
    meta_id text,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    isrctn_id text NOT NULL,
    doi_isrctn_id text,
    title text,
    condition_category text,
    date_applied date,
    date_assigned date,
    last_edited date,
    prospective_retrospective text,
    overall_trial_status text,
    recruitment_status text,
    plain_english_summary text,
    trial_website text,
    contacts jsonb,
    eudract_number text,
    clinicaltrials_gov_number text,
    protocol_serial_number text,
    scientific_title text,
    acronym text,
    study_hypothesis text,
    ethics_approval text,
    study_design text,
    primary_study_design text,
    secondary_study_design text,
    trial_setting text,
    trial_type text,
    patient_information_sheet text,
    condition text,
    intervention text,
    intervention_type text,
    phase text,
    drug_names text,
    primary_outcome_measures text,
    secondary_outcome_measures text,
    overall_trial_start_date date,
    overall_trial_end_date date,
    reason_abandoned text,
    participant_inclusion_criteria text,
    participant_type text,
    age_group text,
    gender text,
    target_number_of_participants text,
    participant_exclusion_criteria text,
    recruitment_start_date date,
    recruitment_end_date date,
    countries_of_recruitment text,
    trial_participating_centre text,
    sponsors jsonb,
    funders jsonb,
    publication_and_dissemination_plan text,
    intention_to_publish_date date,
    participant_level_data text,
    results_basic_reporting text,
    publication_summary text,
    publication_citations text
);


--
-- Name: jprn; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE jprn (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    recruitment_status text,
    unique_trial_number text NOT NULL,
    title_of_the_study text,
    date_of_formal_registrationdate_of_icmje_and_who date,
    date_and_time_of_last_update timestamp with time zone,
    official_scientific_title_of_the_study text,
    title_of_the_study_brief_title text,
    region text,
    condition text,
    classification_by_specialty text,
    classification_by_malignancy text,
    genomic_information boolean,
    narrative_objectives1 text,
    basic_objectives2 text,
    basic_objectives_others text,
    trial_characteristics_1 text,
    trial_characteristics_2 text,
    developmental_phase text,
    primary_outcomes text,
    key_secondary_outcomes text,
    study_type text,
    basic_design text,
    randomization text,
    randomization_unit text,
    blinding text,
    control text,
    stratification text,
    dynamic_allocation text,
    institution_consideration text,
    blocking text,
    concealment text,
    no_of_arms integer,
    purpose_of_intervention text,
    type_of_intervention text,
    interventions text[],
    agelower_limit text,
    ageupper_limit text,
    gender text,
    key_inclusion_criteria text,
    key_exclusion_criteria text,
    target_sample_size integer,
    research_name_of_lead_principal_investigator text,
    research_organization text,
    research_division_name text,
    research_address text,
    research_tel text,
    research_homepage_url text,
    research_email text,
    public_name_of_contact_person text,
    public_organization text,
    public_division_name text,
    public_address text,
    public_tel text,
    public_homepage_url text,
    public_email text,
    name_of_primary_sponsor text,
    source_of_funding text,
    category_of_org text,
    nation_of_funding text,
    cosponsor text,
    name_of_secondary_funers text,
    secondary_study_ids boolean,
    secondary_study_id_1 text,
    org_issuing_secondary_study_id_1 text,
    secondary_study_id_2 text,
    org_issuing_secondary_study_id_2 text,
    ind_to_mhlw text,
    institutions text,
    date_of_protocol_fixation date,
    anticipated_trial_start_date date,
    last_followup_date date,
    date_of_closure_to_data_entry date,
    date_trial_data_considered_complete date,
    date_analysis_concluded date,
    url_releasing_protocol text,
    publication_of_results text,
    url_releasing_results text,
    results text,
    other_related_information text,
    date_of_registration date,
    date_of_last_update timestamp with time zone,
    urljapanese text,
    urlenglish text
);


--
-- Name: nct; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE nct (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
    download_date text,
    link_text text,
    url text,
    org_study_id text,
    nct_id text NOT NULL,
    secondary_ids text[],
    nct_aliases text[],
    brief_title text,
    acronym text,
    official_title text,
    sponsors jsonb,
    source text,
    oversight_info jsonb,
    brief_summary text,
    detailed_description text,
    overall_status text,
    why_stopped text,
    start_date date,
    completion_date_actual date,
    completion_date_anticipated date,
    primary_completion_date_actual date,
    primary_completion_date_anticipated date,
    phase text,
    study_type text,
    study_design text,
    target_duration text,
    primary_outcomes jsonb,
    secondary_outcomes jsonb,
    other_outcomes jsonb,
    number_of_arms integer,
    number_of_groups integer,
    enrollment_actual integer,
    enrollment_anticipated integer,
    conditions text[],
    arm_groups jsonb,
    interventions jsonb,
    biospec_retention text,
    biospec_desrc text,
    eligibility jsonb,
    overall_officials jsonb,
    overall_contact jsonb,
    overall_contact_backup jsonb,
    locations jsonb,
    location_countries text[],
    removed_countries text[],
    links jsonb,
    "references" jsonb,
    results_references jsonb,
    verification_date date,
    lastchanged_date date,
    firstreceived_date date,
    firstreceived_results_date date,
    responsible_party jsonb,
    keywords text[],
    is_fda_regulated boolean,
    is_section_801 boolean,
    has_expanded_access boolean,
    condition_browse jsonb,
    intervention_browse jsonb,
    clinical_results jsonb,
    results_exemption_date date
);


--
-- Name: pfizer; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE pfizer (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
    article_ids jsonb,
    mesh_headings jsonb,
    registry_ids jsonb
);


--
-- Name: takeda; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE takeda (
    meta_id uuid,
    meta_source text,
    meta_created timestamp with time zone DEFAULT now() NOT NULL,
    meta_updated timestamp with time zone DEFAULT now() NOT NULL,
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
-- Name: alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace:
--

ALTER TABLE ONLY alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


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


--
-- Name: actrn_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER actrn_set_meta_updated BEFORE UPDATE ON actrn FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: cochrane_reviews_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER cochrane_reviews_set_meta_updated BEFORE UPDATE ON cochrane_reviews FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: euctr_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER euctr_set_meta_updated BEFORE UPDATE ON euctr FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: fda_dap_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER fda_dap_set_meta_updated BEFORE UPDATE ON fda_dap FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: fdadl_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER fdadl_set_meta_updated BEFORE UPDATE ON fdadl FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: gsk_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER gsk_set_meta_updated BEFORE UPDATE ON gsk FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: hra_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER hra_set_meta_updated BEFORE UPDATE ON hra FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: icdcm_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER icdcm_set_meta_updated BEFORE UPDATE ON icdcm FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: icdpcs_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER icdpcs_set_meta_updated BEFORE UPDATE ON icdpcs FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: ictrp_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ictrp_set_meta_updated BEFORE UPDATE ON ictrp FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: isrctn_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER isrctn_set_meta_updated BEFORE UPDATE ON isrctn FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: jprn_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER jprn_set_meta_updated BEFORE UPDATE ON jprn FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: nct_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER nct_set_meta_updated BEFORE UPDATE ON nct FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: pfizer_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER pfizer_set_meta_updated BEFORE UPDATE ON pfizer FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: pubmed_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER pubmed_set_meta_updated BEFORE UPDATE ON pubmed FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- Name: takeda_set_meta_updated; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER takeda_set_meta_updated BEFORE UPDATE ON takeda FOR EACH ROW EXECUTE PROCEDURE set_meta_updated();


--
-- PostgreSQL database dump complete
--
