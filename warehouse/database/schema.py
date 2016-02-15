# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sqlalchemy as sa
from functools import partial
from sqlalchemy.dialects.postgresql import ARRAY, JSONB


engine = sa.create_engine(os.environ['OPENTRIALS_DATABASE_URL'])
metadata = sa.MetaData(bind=engine, reflect=True)
Column = partial(sa.Column, nullable=False)


# Meta tables

sa.Table('source', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'register',
            'other',
            name='source_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name', 'type'),

)


# Data tables

sa.Table('trial', metadata,

        # Columns

        # Meta
        Column('uuid', sa.Text),

        # General
        Column('primary_register', sa.Text),
        Column('primary_id', sa.Text),
        Column('secondary_ids', JSONB),
        Column('registration_date', sa.Date),
        Column('public_title', sa.Text),
        Column('brief_summary', sa.Text),
        Column('scientific_title', sa.Text, nullable=True),
        Column('description', sa.Text, nullable=True),

        # Recruitment
        Column('recruitment_status', sa.Text),
        Column('eligibility_criteria', JSONB),
        Column('target_sample_size', sa.Integer, nullable=True),
        Column('first_enrollment_date', sa.Date, nullable=True),

        # Study design
        Column('study_type', sa.Text),
        Column('study_design', sa.Text),
        Column('study_phase', sa.Text),

        # Outcomes
        Column('primary_outcomes', JSONB, nullable=True),
        Column('secondary_outcomes', JSONB, nullable=True),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('primary_register', 'primary_id'),

)


sa.Table('record', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('source_uuid', sa.Text),
        Column('type', sa.Enum(
            'trial',
            'other',
            name='record_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        # uuid from warehouse
        sa.PrimaryKeyConstraint('uuid'),
        sa.ForeignKeyConstraint(['source_uuid'], ['source.uuid']),

)


sa.Table('trial_record', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('record_uuid', sa.Text),
        Column('role', sa.Enum(
            'primary',
            'secondary',
            'other',
            name='trial_record_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'record_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['record_uuid'], ['record.uuid']),

)


sa.Table('publication', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('source_uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'other',
            name='publication_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.ForeignKeyConstraint(['source_uuid'], ['source.uuid']),
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('trial_publication', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('publication_uuid', sa.Text),
        Column('role', sa.Enum(
            'other',
            name='trial_publication_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'publication_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['publication_uuid'], ['publication.uuid']),

)


sa.Table('document', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('source_uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'other',
            name='publication_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.ForeignKeyConstraint(['source_uuid'], ['source.uuid']),
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('trial_document', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('document_uuid', sa.Text),
        Column('role', sa.Enum(
            'other',
            name='trial_document_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'document_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['document_uuid'], ['document.uuid']),

)


# Reference tables

sa.Table('problem', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'condition',
            'other',
            name='problem_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('trial_problem', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('problem_uuid', sa.Text),
        Column('role', sa.Enum(
            'other',
            name='trial_problem_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'problem_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['problem_uuid'], ['problem.uuid']),

)


sa.Table('intervention', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'drug',
            'other',
            name='intervention_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('trial_intervention', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('intervention_uuid', sa.Text),
        Column('role', sa.Enum(
            'other',
            name='trial_intervention_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'intervention_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['intervention_uuid'], ['intervention.uuid']),

)


sa.Table('location', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'country',
            'city',
            'other',
            name='location_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name', 'type'),

)


sa.Table('trial_location', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('location_uuid', sa.Text),
        Column('role', sa.Enum(
            'recruitment_countries',
            'other',
            name='trial_location_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'location_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['location_uuid'], ['location.uuid']),

)


sa.Table('organisation', metadata,

        # Columns

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'other',
            name='organisation_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        # Deduplication strategy for testing purposes
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name'),

)


sa.Table('trial_organisation', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('organisation_uuid', sa.Text),
        Column('role', sa.Enum(
            'primary_sponsor',
            'sponsor',
            'funder',
            'other',
            name='trial_organisation_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'organisation_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['organisation_uuid'], ['organisation.uuid']),

)


sa.Table('person', metadata,

        Column('uuid', sa.Text),
        Column('name', sa.Text),
        Column('type', sa.Enum(
            'other',
            name='person_type',
        ), nullable=True),
        Column('data', JSONB),

        # Constraints

        # Deduplication strategy for testing purposes
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('name'),

)


sa.Table('trial_person', metadata,

        # Columns

        Column('trial_uuid', sa.Text),
        Column('person_uuid', sa.Text),
        Column('role', sa.Enum(
            'principal_investigator',
            'public_queries',
            'scientific_queries',
            'other',
            name='trial_person_role',
        ), nullable=True),
        Column('context', JSONB),

        # Constraints

        sa.PrimaryKeyConstraint('trial_uuid', 'person_uuid'),
        sa.ForeignKeyConstraint(['trial_uuid'], ['trial.uuid']),
        sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid']),

)


metadata.create_all()
