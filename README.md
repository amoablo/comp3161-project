# comp3161-project
A system for meal plannng

## Dependices
- python 3
- python3 virtualenv
- Flask

## Getting Started

**Setup Virtual Environment**
```
python -m venv venv
```

**Activate Virtual Environemtn**
```
source venv/bin/activate (linux)

venv\Scripts\activate (Windows)
```

**Install Flask Requirements**
```
pip install -r requirements.txt 
```

**If any additional packages is added, update the requirements file with**
```
pip freeze > requirements.txt
```

**Run Flask**
```
python run.py
```

**Run Migration**
```
 python flask-migrate.py db init 
 python flask-migrate.py db migrate
 python flask-migrate.py db upgrade
```