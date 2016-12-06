CREATE TABLE knex_migrations (
	id SERIAL NOT NULL, 
	name VARCHAR(255), 
	batch INTEGER, 
	migration_time TIMESTAMP WITH TIME ZONE, 
	CONSTRAINT knex_migrations_pkey PRIMARY KEY (id)
);
CREATE TABLE sources (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	type TEXT, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_url TEXT, 
	terms_and_conditions_url TEXT, 
	CONSTRAINT sources_pkey PRIMARY KEY (id), 
	CONSTRAINT sources_name_type_unique UNIQUE (name, type)
);
CREATE TABLE knex_migrations_lock (
	is_locked INTEGER
);
CREATE TABLE files (
	id UUID NOT NULL, 
	documentcloud_id TEXT, 
	sha1 TEXT NOT NULL, 
	source_url TEXT NOT NULL, 
	pages TEXT[], 
	CONSTRAINT files_pkey PRIMARY KEY (id), 
	CONSTRAINT files_documentcloud_id_unique UNIQUE (documentcloud_id), 
	CONSTRAINT files_sha1_unique UNIQUE (sha1), 
	CONSTRAINT files_source_url_unique UNIQUE (source_url)
);
CREATE TABLE risk_of_bias_criterias (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT risk_of_bias_criterias_pkey PRIMARY KEY (id), 
	CONSTRAINT risk_of_bias_criterias_name_unique UNIQUE (name)
);
CREATE TABLE organisations (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_id TEXT, 
	slug TEXT, 
	CONSTRAINT organisations_pkey PRIMARY KEY (id), 
	CONSTRAINT organisations_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT organisations_slug_unique UNIQUE (slug), 
	CONSTRAINT organisations_name_unique UNIQUE (name)
);
CREATE TABLE locations (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	type TEXT, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_id TEXT, 
	slug TEXT, 
	CONSTRAINT locations_pkey PRIMARY KEY (id), 
	CONSTRAINT locations_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT locations_slug_unique UNIQUE (slug), 
	CONSTRAINT locations_name_type_unique UNIQUE (name, type)
);
CREATE TABLE trials (
	id UUID NOT NULL, 
	identifiers JSONB NOT NULL, 
	registration_date DATE, 
	public_title TEXT NOT NULL, 
	brief_summary TEXT, 
	scientific_title TEXT, 
	description TEXT, 
	recruitment_status TEXT, 
	eligibility_criteria JSONB, 
	target_sample_size INTEGER, 
	first_enrollment_date DATE, 
	study_type TEXT, 
	study_design TEXT, 
	study_phase TEXT, 
	primary_outcomes JSONB, 
	secondary_outcomes JSONB, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	has_published_results BOOLEAN, 
	gender TEXT, 
	source_id TEXT, 
	status TEXT, 
	completion_date DATE, 
	CONSTRAINT trials_pkey PRIMARY KEY (id), 
	CONSTRAINT trials_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE
);
CREATE TABLE conditions (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_id TEXT, 
	slug TEXT, 
	description TEXT, 
	icdcm_code TEXT, 
	CONSTRAINT problems_pkey PRIMARY KEY (id), 
	CONSTRAINT problems_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT problems_slug_unique UNIQUE (slug)
);
CREATE TABLE persons (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_id TEXT, 
	slug TEXT, 
	CONSTRAINT persons_pkey PRIMARY KEY (id), 
	CONSTRAINT persons_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT persons_slug_unique UNIQUE (slug)
);
CREATE TABLE publications (
	id UUID NOT NULL, 
	source_id TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_url TEXT NOT NULL, 
	title TEXT NOT NULL, 
	abstract TEXT NOT NULL, 
	authors TEXT[], 
	journal TEXT, 
	date DATE, 
	slug TEXT, 
	CONSTRAINT publications_pkey PRIMARY KEY (id), 
	CONSTRAINT publications_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT publications_slug_unique UNIQUE (slug)
);
CREATE TABLE trials_publications (
	trial_id UUID NOT NULL, 
	publication_id UUID NOT NULL, 
	CONSTRAINT trials_publications_pkey PRIMARY KEY (trial_id, publication_id), 
	CONSTRAINT trials_publications_publication_id_foreign FOREIGN KEY(publication_id) REFERENCES publications (id), 
	CONSTRAINT trials_publications_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE
);
CREATE TABLE trials_persons (
	trial_id UUID NOT NULL, 
	person_id UUID NOT NULL, 
	role TEXT, 
	CONSTRAINT trials_persons_pkey PRIMARY KEY (trial_id, person_id), 
	CONSTRAINT trials_persons_person_id_foreign FOREIGN KEY(person_id) REFERENCES persons (id), 
	CONSTRAINT trials_persons_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE
);
CREATE TABLE trials_locations (
	trial_id UUID NOT NULL, 
	location_id UUID NOT NULL, 
	role TEXT, 
	CONSTRAINT trials_locations_pkey PRIMARY KEY (trial_id, location_id), 
	CONSTRAINT trials_locations_location_id_foreign FOREIGN KEY(location_id) REFERENCES locations (id), 
	CONSTRAINT trials_locations_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE
);
CREATE TABLE trials_conditions (
	trial_id UUID NOT NULL, 
	condition_id UUID NOT NULL, 
	CONSTRAINT trials_problems_pkey PRIMARY KEY (trial_id, condition_id), 
	CONSTRAINT trials_conditions_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE, 
	CONSTRAINT trials_problems_problem_id_foreign FOREIGN KEY(condition_id) REFERENCES conditions (id)
);
CREATE TABLE risk_of_biases (
	id UUID NOT NULL, 
	trial_id UUID NOT NULL, 
	source_id TEXT NOT NULL, 
	source_url TEXT NOT NULL, 
	study_id TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT risk_of_biases_pkey PRIMARY KEY (id), 
	CONSTRAINT risk_of_biases_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id), 
	CONSTRAINT risk_of_biases_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id), 
	CONSTRAINT risk_of_biases_study_id_source_url_unique UNIQUE (study_id, source_url)
);
CREATE TABLE fda_applications (
	id TEXT NOT NULL, 
	organisation_id UUID, 
	drug_name TEXT, 
	active_ingredients TEXT, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT fda_applications_pkey PRIMARY KEY (id), 
	CONSTRAINT fda_applications_organisation_id_foreign FOREIGN KEY(organisation_id) REFERENCES organisations (id)
);
CREATE TABLE records (
	id UUID NOT NULL, 
	source_id TEXT NOT NULL, 
	source_url TEXT NOT NULL, 
	source_data JSONB NOT NULL, 
	identifiers JSONB NOT NULL, 
	registration_date DATE, 
	public_title TEXT NOT NULL, 
	brief_summary TEXT, 
	scientific_title TEXT, 
	description TEXT, 
	recruitment_status TEXT, 
	eligibility_criteria JSONB, 
	target_sample_size INTEGER, 
	first_enrollment_date DATE, 
	study_type TEXT, 
	study_design TEXT, 
	study_phase TEXT, 
	primary_outcomes JSONB, 
	secondary_outcomes JSONB, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	has_published_results BOOLEAN, 
	gender TEXT, 
	trial_id UUID, 
	status TEXT, 
	completion_date DATE, 
	CONSTRAINT trialrecords_pkey PRIMARY KEY (id), 
	CONSTRAINT trialrecords_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT trialrecords_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id)
);
CREATE INDEX trialrecords_trial_id_index ON records (trial_id);
CREATE INDEX records_identifiers_index ON records USING gin (identifiers);
CREATE TABLE trials_organisations (
	trial_id UUID NOT NULL, 
	organisation_id UUID NOT NULL, 
	role TEXT, 
	CONSTRAINT trials_organisations_pkey PRIMARY KEY (trial_id, organisation_id), 
	CONSTRAINT trials_organisations_organisation_id_foreign FOREIGN KEY(organisation_id) REFERENCES organisations (id), 
	CONSTRAINT trials_organisations_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE
);
CREATE TABLE interventions (
	id UUID NOT NULL, 
	name TEXT NOT NULL, 
	type TEXT, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	source_id TEXT, 
	slug TEXT, 
	description TEXT, 
	icdpcs_code TEXT, 
	ndc_code TEXT, 
	fda_application_id TEXT, 
	CONSTRAINT interventions_pkey PRIMARY KEY (id), 
	CONSTRAINT interventions_fda_application_id_foreign FOREIGN KEY(fda_application_id) REFERENCES fda_applications (id) ON UPDATE CASCADE, 
	CONSTRAINT interventions_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT interventions_name_type_unique UNIQUE (name, type), 
	CONSTRAINT interventions_slug_unique UNIQUE (slug)
);
CREATE INDEX interventions_fda_application_number_index ON interventions (fda_application_id);
CREATE TABLE risk_of_biases_risk_of_bias_criterias (
	risk_of_bias_id UUID NOT NULL, 
	risk_of_bias_criteria_id UUID NOT NULL, 
	value TEXT NOT NULL, 
	CONSTRAINT risk_of_biases_risk_of_bias_criterias_pkey PRIMARY KEY (risk_of_bias_id, risk_of_bias_criteria_id), 
	CONSTRAINT risk_of_biases_risk_of_bias_criterias_risk_of_bias_criteria_id_ FOREIGN KEY(risk_of_bias_criteria_id) REFERENCES risk_of_bias_criterias (id), 
	CONSTRAINT risk_of_biases_risk_of_bias_criterias_risk_of_bias_id_foreign FOREIGN KEY(risk_of_bias_id) REFERENCES risk_of_biases (id)
);
CREATE TABLE fda_approvals (
	id TEXT NOT NULL, 
	supplement_number INTEGER NOT NULL, 
	type TEXT NOT NULL, 
	action_date DATE NOT NULL, 
	notes TEXT, 
	created_at TIMESTAMP WITH TIME ZONE, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	fda_application_id TEXT NOT NULL, 
	CONSTRAINT fda_approvals_pkey PRIMARY KEY (id), 
	CONSTRAINT fda_approvals_fda_application_id_foreign FOREIGN KEY(fda_application_id) REFERENCES fda_applications (id) ON UPDATE CASCADE, 
	CONSTRAINT fda_approvals_fda_application_id_supplement_number_unique UNIQUE (fda_application_id, supplement_number)
);
CREATE INDEX fda_approvals_type_index ON fda_approvals (type);
CREATE TABLE documents (
	id UUID NOT NULL, 
	source_id TEXT, 
	name TEXT NOT NULL, 
	type TEXT NOT NULL, 
	fda_approval_id TEXT, 
	file_id UUID, 
	source_url TEXT, 
	CONSTRAINT documents_pkey PRIMARY KEY (id), 
	CONSTRAINT documents_fda_approval_id_foreign FOREIGN KEY(fda_approval_id) REFERENCES fda_approvals (id), 
	CONSTRAINT documents_file_id_foreign FOREIGN KEY(file_id) REFERENCES files (id), 
	CONSTRAINT documents_source_id_foreign FOREIGN KEY(source_id) REFERENCES sources (id) ON UPDATE CASCADE, 
	CONSTRAINT documents_fda_approval_id_file_id_name_unique UNIQUE (fda_approval_id, file_id, name)
);
CREATE UNIQUE INDEX non_fda_documents_type_file_id_unique ON documents (type, file_id);
CREATE UNIQUE INDEX non_fda_documents_type_source_url_unique ON documents (type, source_url);
CREATE TABLE trials_interventions (
	trial_id UUID NOT NULL, 
	intervention_id UUID NOT NULL, 
	CONSTRAINT trials_interventions_pkey PRIMARY KEY (trial_id, intervention_id), 
	CONSTRAINT trials_interventions_intervention_id_foreign FOREIGN KEY(intervention_id) REFERENCES interventions (id), 
	CONSTRAINT trials_interventions_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id) ON DELETE CASCADE
);
CREATE TABLE trials_documents (
	trial_id UUID NOT NULL, 
	document_id UUID NOT NULL, 
	CONSTRAINT trials_documents_pkey PRIMARY KEY (trial_id, document_id), 
	CONSTRAINT trials_documents_document_id_foreign FOREIGN KEY(document_id) REFERENCES documents (id), 
	CONSTRAINT trials_documents_trial_id_foreign FOREIGN KEY(trial_id) REFERENCES trials (id)
);
CREATE INDEX trials_documents_document_id_index ON trials_documents (document_id);
