# Mapper

Mapper maps data from `warehouse` to `database` (or otherwise).

## Status

Mapper is work in progress.
Overall dataflow logic could be improved,
concrete mappings to warehouse should be improved.

## Stacks

Mapper provides the following stacks:
- `make-initial-mapping` - map all items
- `mapper` - map updated items (under development)

## Components

Mapper consists of the following components.

### Mapper

> Mapper uses Translators.

External interface available via cli.
Mapper gets `translator` and `extractor` names and map the data.

```python
mapper = Mapper(warehouse, database)
mapper.map('trial', 'nct')
```

### Translators

> Translators uses Extractors, Pipiline and Finder.

Translator is a concrete task for mapper. For example
`TrialTranslator` translates data related to trials from
`warehouse` to `database`.

```python
translator = TrialTranslator(warehouse, database, 'nct')
translator.translate()
```

### Extractors

Extractor is a bridge between ideal entity representations
and items stored in `warehouse`. It extracts unified
data from not structured items. So extractor hides differenced
between item representation in different registers:

```python
# NCT
nct_item = {
    'nct_number': 'nct15',
    'main_title': 'name1',
    ...
}
extractor = NctExtractor()
trial = extractor.extract('trial', item)
print(trial)
{
    'primary_id': 'nct15',
    'public_title': 'name1',
     ...
}

# EUCTR
euctr_item = {
    'trial_id': 'euctr2004',
    'euro_title': 'name3',
     ...
}
extractor = EuctrExtractor()
trial = extractor.extract('trial', item)
print(trial)
{
    'primary_id': 'euctr20014',
    'public_title': 'name3',
     ...
}
```

### Pipeline

Pipiline is a abstraction to read from source (e.g. `warehouse`)
and write to target (e.g `databae`).

```python
pipeline = Pipeline(source=warehouse, target=database)
pipeline.read(table)
pipelint.write(table, keys, **data)
...
```

### Finder

Finder is a main component of deduplication system.

Finder gets `filter`, `links` and `facts` about some entity
and finds it in `database`:
- if entity exists Finder updated search fields and returns
- if entity doesn't exist Finder create entity draft and returns

For example trial `facts` is slugified register indentifiers
and hashed/slugified scientific titles:
`['nct21231', 'isrct23412', 'sa35434525']`

On deduplication stage finder finds trials with this facts
(we need to use GIN index here to do not have full scan in postgress)
to associate item from some other register with one living in our database.

If there is a match facts will be merged:
`['nct21231', 'isrct23412', 'sa35434525', 'euctr2224']`

The same for the persons for example where facts will be
slugified `phones`, `email` etc (not fully implemented). But for persons
we also check `name` equality. Persons with the same name and
one of the facts equal is a one person:
`'Mr. Smith'`
`AND`
`['53242345432', 'simthgailcom']`

Other concept is `links` - here stored trial uuids for entities like
persons - if no facts are match but name is the same and persons
used to be part of the same trial - it'is a one person:
`'Mr. Smith'`
`AND`
`['<trial_id>']`

It's quite WIP but the best approack I've found for now to have
robust and flexible dedup system for all entities we need.

```python
finder = Finder(database)

# Existent
entity, existent = finder.find('trials', facts=['nct15'])
print(existent)
True
print(entity)
{
    'id': 'abc'
    'links': [],
    'facts': ['nct15', ...],
    'created': ...,
    'updated': ...
    'primary_id': 'nct15',
    'public_title': 'name1',
    ...
}

# Non existent
entity, existent = finder.find('trials', facts=['nct77'])
print(existent)
False
print(entity)
{
    'id': 'sfa'
    'links': [],
    'facts': ['nct77', ...]
    'created': ...,
    'updated': ...
}
```
