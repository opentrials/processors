# contrib

This processor extracts documents from `exprorerdb.data_contributions` table
and save it to S3 bucket in half-automated way.

## Configuration

In `config.py` there is a mapping to describe how we extract documents
from downloaded (and automatically unzipped if needed) contributions:

```python
CONTRIB = {
    # Contribution ID
    '9e4f1280-41bf-11e6-8971-f99af8d5a820': {
        # Contribution type
        'csr': [
            # Regex to extract primary_id from filename
            r'(?P<primary_id>nct\d{3,})\.pdf',
            # Hard-coded mapping for primary_id
            ('some_document.pdf', 'ISRCT12345678'),
        ],
    },
}
```

## Possible Improvements

This configuration dict could be read from source like Google Spreadsheets to
improve user interface for contribution uploading. It could be temporal solution
before proper UI will be built or persistent solution for massive contributions
which need an automation.

## S3 files naming

Uploaded documents have keys based on the following pattern:
```
documents/<SHA1-hash>.<extension>
```
