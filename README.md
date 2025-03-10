# Gulag

Vietnamese-German University Labor Camp for multi-disciplinary project

## Development

- Clone project using `git clone https://github.com/CallMeQan/gulag.git` or Github Desktop
- Create environment with `python -m venv venv`
- Active environment `.\venv\Scripts\activate`
- Create file `.env` from [.env.example](./.env.example)
- Setup Google Gmail API and put the json file into `credentials.json`
- Install all packages `pip install -r requirements.txt`

### Structure

```bash
<root>
    |
    |-- app/
    |   |
    |   |-- __init__.py # Init everything
    |   |-- models.py # Lmao
    |   |-- config.py # All Flask config
    |   |
    |   |-- static/
    |   |   |
    |   |   |-- < css, JS, images > # CSS files, Javascripts files
    |   |
    |   |-- templates/
    |   |   |
    |   |   |-- < pages, folder pages >
    |   |
    |   |-- services/
    |   |   |
    |   |   |-- api/ # IoT API
    |   |   |-- authentication/ # Login, Logout, Register logic
    |   |
    |   |-- route/ # Blueprint, act like route
    |
    |-- README.md
    |-- credentials.json # Google API Credentials
    |-- .env # Environment variable
    |-- requirements.txt
    |-- run.py
```
