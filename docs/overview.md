# Overview

This system is responsible for data processing
in `warehouse`, `database`, `datastore` and possible other storages.

## Stacks

The system provides the following stacks:
- `make-initial-processing` - process anything initially
- `processors` - continuous processing of updated elements

About Docker Cloud deployment see -
https://github.com/respect31/docker-cloud-example.

## Processors

The system's processors are independent python modules
compatible to the following signature:

```python
def process(conf, conn, *args):
    pass
```

Where arguments are:
- `conf` - config dict
- `conn` - connections dict
- `args` - processor arguments

To run one of processors from command line:
```
make start <name> [<args>]
```

This code will trigger `processors.<name>.process(conf, conn, *args)` call.

## Base library

For developers convenient in a `processors.base` module
there are shared library of reusable components to write processors.

### Processors

There are a few lower level processors based on
main entity they process:
- trial
- publication
- etc

So if you're going to process trials from `warehouse`
to `database` you could use this shared component.

```python
def process_trial(conn, table, extractors):
    pass
```

Where `extractors` is a dictionary of functions
getting `record` dict and returning dict of normalized
data. For example extracting from `nct` record
data about interventions.

Extractor is a bridge between ideal entity representations
and items stored in `warehouse`. It extracts unified
data from not structured items. So extractor hides differenced
between item representation in different registers:

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
trial = extract_record(euctr_record)
print(trial)
{
    'primary_id': 'euctr20014',
    'public_title': 'name3',
     ...
}
```

### Readers

There are storage readers:
- record
- object

`record` reader just read records from `warehouse`
optimizing memory and network usage.

`object` reader reads data from `database` based
on filters. It's a part of deduplication system.

It gets `slug` and `facts` about some object
and finds it in `database` (also `filter` could be applied).

For example trial's `facts` is slugified register identifiers
and scientific titles:
```
['nct21231', 'isrct23412', 'scientific_title']
```

On deduplication stage reader finds trials with this facts
(we need to use GIN index here to do not have full scan in postgress)
to associate item from some other register with one living in our database.

If there is a match facts will be merged on a writing stage:
```
['nct21231', 'isrct23412', 'sa35434525', 'euctr2224']
```

The same for the persons for example where facts will be
slugified `phones`, `email` etc (not fully implemented). But for persons
we also check slugified `name` equality. Persons with the same slug and
one of the facts equal is a one person:
```
'mr_smith'
AND
['53242345432', 'simthgailcom', 'nct13243241']
```

### Writers

For many of entities there are ready writers:
- trial
- person
- publication
- etc

Writers write normalized data to `database`
updating deduplication system elements etc.

See documentation in source code to use it.
