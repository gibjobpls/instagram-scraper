# instagram-scraper

scrapes one instagram profile for all comments on posts

## Getting Started

Packages used include: selenium, dotenv, pandas, os, time

```
pip install -r requirements.txt
```

- create a `.env` file:
  USERNAME_VAR="your username"
  PASSWORD_VAR="your password"
  TARGET_VAR="profile you want to scrape"
- Run python script

If you are using Mac and come across the error:

```python
from openpyxl import Workbook
ImportError: No module named 'openpyxl'
```

use this command if you've not aliased python3 to something else:

```python
python3 -m pip install --user xlsxwriter
```
