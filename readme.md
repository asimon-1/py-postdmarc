# py-postdmarc

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=scuriosity_py-postdmarc&metric=alert_status)](https://sonarcloud.io/dashboard?id=scuriosity_py-postdmarc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A Python interface for the [Postmark DMARC monitoring API](https://dmarc.postmarkapp.com/).

---

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Example

```bat
set POSTMARK_API_KEY="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
postdmarc get_record
postdmarc export_all_reports --from_date 2020-01-01 --to_date 2020-01-08 --filepath reports.json
```

---

## Installation

```
pip install py-postdmarc
```

### Clone

Clone this repo to your local machine using `https://github.com/scuriosity/py-postdmarc`, then install locally with pip:
```
git clone https://github.com/scuriosity/py-postdmarc
pip install .
```

---

## Features

Implements the 10 API methods provided by the [API Documentation](https://dmarc.postmarkapp.com/api/):

- Create a record
- Get a record
- Update a record
- Get DNS snippet
- Verify DNS
- Delete a record
- List DMARC reports
- Get a specific DMARC report by ID
- Recover API token
- Rotate API token

As well as

- Export all forensic reports within a given timeframe to a JSON file.

## Usage

### API Key

For most commands, your Postmark API key is required. The py-postdmarc package can load your API key either from the `POSTMARK_API_KEY` environment variable or the file `PM_API.key` in the package root. The API key should be a hexadecimal string like this:

> aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

```
py-postdmarc/
+-- postdmarc/
|   +-- __init__.py
|   +-- pdm_exceptions.py
|   └-- postdmarc.py
|
+-- tests/
|   +-- __init__.py
|   +-- test_meta.py
|   └-- test_postdmarc.py
|
+-- license.txt
+-- PM_API.key
+-- readme.md
+-- requirements.txt
+-- setup.py
```

If the key isn't set in one of these two locations, an APIKeyMissingError will be raised.

### Syntax

**Create a record**

```
postdmarc create_record --email EMAIL@domain.com --domain domain.com
```

**Get a record**

```
postdmarc get_record
```

**Update a record**

```
postdmarc update_record --email EMAIL@domeng.com
```

**Get DNS snippet**

```
postdmarc get_dns_snippet
```

**Verify DNS**

```
postdmarc verify_dns
```

**Delete a record**

```
postdmarc delete_record
```

**List DMARC reports**

```
postdmarc list_reports --from_date 01-01-2020 --to_date 01-02-2020
```

Optional flags for "after", "before" and "reverse" are provided.

**Get a specific DMARC report by ID**

```
postdmarc get_report --id 1234567
```

```
postdmarc get_report --id 1234567 --fmt xml
```

**Recover API token**

```
postdmarc recover_token --owner domain.com
```

**Rotate API token**

```
postdmarc rotate_token
```

**Export all forensic reports**

```
postdmarc export_all_reports --from_date 2020-01-01 --to_date 2020-01-08 --filepath reports.json
```

---

## Contributing

Issues and pull requests are welcome. Create a new pull request using [https://github.com/scuriosity/py-postdmarc/compare](https://github.com/scuriosity/py-postdmarc/compare)

---

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © [Scuriosity](https://github.com/scuriosity).
