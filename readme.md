# py-postdmarc

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
python postdmarc/postdmarc.py
```

---

## Installation

TODO

### Clone

- Clone this repo to your local machine using `https://github.com/scuriosity/py-postdmarc`

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

- Export all forensic reports within a given timeframe.

## Usage

TODO

---

## Contributing

Issues and pull requests are welcome. Create a new pull request using <a href="https://github.com/scuriosity/py-postdmarc/compare" target="_blank">`https://github.com/scuriosity/py-postdmarc/compare`</a>.

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://github.com/scuriosity" target="_blank">Scuriosity</a>.
