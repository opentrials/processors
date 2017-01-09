# Overview

OpenTrials project has 4 main components:
  - [Collectors](https://github.com/opentrials/collectors): contains logic for gathering data (e.g. scrapers)
  and manages the schema for our `warehouse` database that keeps the data collected from different sources
  - [Processors](https://github.com/opentrials/processors): contains logic for processing and inserting data from `warehouse` into our API `database`
  - [OpenTrials API](https://github.com/opentrials/api): manages the schema for our `database` and contains logic for exposing and indexing the data inside it
  - [OpenTrials Explorer](https://github.com/opentrials/opentrials): displays data from our API and manages the `explorer` database that keeps users and user-related data

This system is responsible with normalizing and enriching data in our `warehouse` and API `database` and managing our file storage.

----

### Stack
Processors are fully compatible with Python2.7.

We use PostgreSQL for our databases and [Docker Cloud](https://github.com/respect31/docker-cloud-example) to deploy and run the processors in production.

## Processors

Processors are independent python modules that share the following signature:

```python
def process(conf, conn, *args):
    pass
```

Where arguments are:
- `conf` - config dict
- `conn` - connections dict
- `args` - processor arguments

To run a processor from the command line:
```
$ make start <name> [<args>]
```

This code will trigger `processors.<name>.process(conf, conn, *args)` call.

### Extractors

One of the most common use cases for processors is to extract and standardize data from our
`warehouse` database into entities that comply with the structure of our API `database`.

Extractors are functions that map entity representations in different registries to OpenTrials API `database` schema.

e.g. Given two registries NCT and EUCTR and their corresponding extractors: [NCT trial extractor](https://github.com/opentrials/processors/blob/master/processors/nct/extractors.py#L23) and [EUCTR trial extractor](https://github.com/opentrials/processors/blob/master/processors/euctr/extractors.py#L23)

```python
# NCT
nct_record = {
    'nct_number': 'nct15',
    'main_title': 'name1',
    ...
}
trial = extract_trial(nct_record)
print(trial)
{
    'primary_id': 'nct15',
    'public_title': 'name1',
     ...
}

# EUCTR
euctr_record = {
    'trial_id': 'euctr2004',
    'euro_title': 'name3',
     ...
}
trial = extract_trial(euctr_record)
print(trial)
{
    'primary_id': 'euctr20014',
    'public_title': 'name3',
     ...
}
```

### Writers

Writers are modules that hold logic for creating and updating entities in `database` *without creating duplicates*.

In the folder `processors/base/writers` we already have writers for different database entities (e.g. `trial`, `person`, etc.) that you can use. See documentation in source code for how to use them.

### Base processors

In the folder `processors/base/processors` there are a few lower level processors
that contain the logic surrounding certain API `database` entities (e.g.  `trial`,  `publication` etc.). Their main role is to manage the Extractors and Writers.

These base processors cannot be directly invoked from the command line, they are meant for use in other processors.

e.g. `trial` processor extracts and writes a `trial` and also creates and links the `trial`'s related entities. It contains the following function:

```python
def process_trials(conn, table, extractors):
    pass
```
Where arguments are:
  - conn - connection dict
  - table - name of table from `warehouse` that contains unstructured records
  - extractors - dict of functions that map the unstructured records into `trials`, `documents` and other `trial`-related entities


### What can go into a processor?

Processors can perform any operation needed to manage data stores: removing records, linking records etc. Just make sure to keep the logic for gathering data
from outside sources in the [Collectors](https://github.com/opentrials/collectors).
