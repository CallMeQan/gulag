# Gulag

Vietnamese-German University Labor Camp for multi-disciplinary project

## Development

### Pre-prerequisites

-   Linux-based or Windows with WSL2 enabled
-   Python 3.12.10
-   Docker 28.0.4 (Optional)
-   PostgreSQL with port open at `5432`

### Step-by-Step

-   Clone project using `git clone https://github.com/CallMeQan/gulag.git` or Github Desktop
-   Create environment with `python -m venv venv`
-   Active environment `.\venv\Scripts\activate` or `. venv/bin/activate` on Unix-based
-   Create file `.env` from [.env.example](./.env.example)
-   Get Map API Key from [Map tiler](https://cloud.maptiler.com/account/keys/)
-   Install all packages `pip3 install -r requirements.txt`
-   In your PostgreSQL, run all command in [mock_data.txt](./mock_data.txt) to generate data
-   Run server with `python3 run.py`

### Structure

```bash
<root>
    |
    |-- app/
    |   |
    |   |-- __init__.py # Root of Flask Webapp, initial everything here
    |   |-- models.py # Database
    |   |-- config.py # All Flask config
    |   |-- extensions.py # Init every services
    |   |
    |   |-- static/
    |   |   |
    |   |   |-- < css, JS, images > # CSS files, Javascripts files
    |   |
    |   |-- templates/
    |   |   |
    |   |   |-- < pages, folder pages >
    |   |
    |   |-- socketio_events/
    |   |   |
    |   |   |-- __init__.py # Empty file to init folder as module
    |   |   |-- events.py # Main socketIO server
    |   |
    |   |-- route/ # Blueprint, act like route
    |   |
    |   |-- modules/
    |   |   |
    |   |   |-- __init__.py
    |   |   |-- data_module/ # data calculation function
    |   |   |-- forgot_module/ # Forgot password function
    |
    |-- gulag-android/ # https://github.com/CallMeQan/gulag-android
    |
    |-- README.md
    |-- credentials.json # Google API Credentials
    |-- .env # Environment variable
    |-- requirements.txt
    |-- run.py
```

## Contributors

### Châu Minh Quân (Leader)

-   Worked on Android and backend Socket.IO

### Hồ Nguyễn Phú (Lead backend)

-   Worked on backend mainly

### Phạm Trọng Quý (Frontend Designer)

-   Frontend & Figma

### Hồng Nguyên Phúc (Full-stack Dev)

-   Mainly frontend & Figma, did on forgot-password function with Phú

### Cao Tuệ Anh (Designer)

-   Frontend & Figma
