set dotenv-load

default:
  just --list

run args:
  ./venv/bin/python3 {{args}}

serve args="":
  ./venv/bin/python3 -m App.server.server

install-all:
  ./venv/bin/pip install -r requirements.txt

install args:
  ./venv/bin/pip3 install {{args}}
  ./venv/bin/pip3 freeze > requirements.txt


init-db:
  ./venv/bin/python3 scripts/init_db.py
