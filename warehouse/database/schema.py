# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB


engine = sa.create_engine(os.environ['OPENTRIALS_DATABASE_URL'])
metadata = sa.MetaData(bind=engine, reflect=True)


# Main tables

sa.Table('trial', metadata,

        # Columns

        # Meta
        sa.Column('uuid', sa.Text, primary_key=True),

        # General
        sa.Column('primary_register', sa.Text),
        sa.Column('primary_id', sa.Text),
        sa.Column('secondary_ids', JSONB),
        sa.Column('registration_date', sa.Date),
        sa.Column('public_title', sa.Text),
        sa.Column('scientific_title', sa.Text),
        sa.Column('description', sa.Text),

        # Recruitment
        sa.Column('eligibility_criteria', sa.Text),
        sa.Column('target_sample_size', sa.Integer),
        sa.Column('first_enrollment_date', sa.Date),
        sa.Column('recruitment_status', sa.Text),

        # Study design
        sa.Column('study_type', sa.Text),
        sa.Column('study_design', sa.Text),
        sa.Column('study_phase', sa.Text),

        # Constraints

        sa.UniqueConstraint('primary_register', 'primary_id'),

)


sa.Table('trial_outcome', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('role', sa.Enum(
            'primary',
            'secondary',
            'other',
            name='trial_outcome_role',
        )),
        sa.Column('order', sa.Integer),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'role', 'order'),

)


sa.Table('trial_record', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('record_uuid', sa.Text, sa.ForeignKey('record.uuid')),
        sa.Column('role', sa.Enum(
            'primary',
            'secondary',
            name='trial_record_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'record_uuid'),

)


sa.Table('trial_publication', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('publication_uuid', sa.Text, sa.ForeignKey('publication.uuid')),
        sa.Column('role', sa.Enum(
            'associated',
            name='trial_publication_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'publication_uuid'),

)


sa.Table('trial_document', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('document_uuid', sa.Text, sa.ForeignKey('document.uuid')),
        sa.Column('role', sa.Enum(
            'associated',
            name='trial_document_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'document_uuid'),

)


sa.Table('trial_problem', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('problem_uuid', sa.Text, sa.ForeignKey('problem.uuid')),
        sa.Column('role', sa.Enum(
            'studied',
            name='trial_problem_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'problem_uuid'),

)


sa.Table('trial_intervention', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('intervention_uuid', sa.Text, sa.ForeignKey('intervention.uuid')),
        sa.Column('role', sa.Enum(
            'studied',
            name='trial_intervention_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'intervention_uuid'),

)


sa.Table('trial_location', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('location_uuid', sa.Text, sa.ForeignKey('location.uuid')),
        sa.Column('role', sa.Enum(
            'recruitment_countries',
            'other',
            name='trial_location_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'location_uuid'),

)


sa.Table('trial_organisation', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('organisation_uuid', sa.Text, sa.ForeignKey('organisation.uuid')),
        sa.Column('role', sa.Enum(
            'primary_sponsor',
            'sponsor',
            'funder',
            'other',
            name='trial_organisation_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'organisation_uuid'),

)


sa.Table('trial_person', metadata,

        # Columns

        sa.Column('trial_uuid', sa.Text, sa.ForeignKey('trial.uuid')),
        sa.Column('person_uuid', sa.Text, sa.ForeignKey('person.uuid')),
        sa.Column('role', sa.Enum(
            'principal_investigator',
            'public_queries',
            'scientific_queries',
            'other',
            name='trial_person_role',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'person_uuid'),

)


sa.Table('record', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('source_uuid', sa.Text, sa.ForeignKey('source.uuid')),
        sa.Column('data', JSONB),

)


sa.Table('publication', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('source_uuid', sa.Text, sa.ForeignKey('source.uuid')),
        sa.Column('name', sa.Text),

)


sa.Table('document', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('source_uuid', sa.Text, sa.ForeignKey('source.uuid')),
        sa.Column('name', sa.Text),

)


# Reference tables

sa.Table('source', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'register',
            'other',
            name='source_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.UniqueConstraint('name', 'type'),

)


sa.Table('problem', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'condition',
            'other',
            name='problem_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.UniqueConstraint('name', 'type'),

)


sa.Table('intervention', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'drug',
            'other',
            name='intervention_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.UniqueConstraint('name', 'type'),

)


sa.Table('location', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'country',
            'city',
            'other',
            name='location_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        sa.UniqueConstraint('name', 'type'),

)


sa.Table('organisation', metadata,

        # Columns

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'other',
            name='organisation_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        # Deduplication strategy for testing purposes
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('person', metadata,

        sa.Column('uuid', sa.Text, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('type', sa.Enum(
            'other',
            name='person_type',
        )),
        sa.Column('data', JSONB),

        # Constraints

        # Deduplication strategy for testing purposes
        sa.UniqueConstraint('name', 'type'),

)


metadata.create_all()
