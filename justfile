set dotenv-load

default:
  just --list

run args:
  ./venv/bin/python3 {{args}}

serve:
  ./venv/bin/python3 -m flask --app ./App/server/server run

install-all:
  ./venv/bin/pip install -r requirements.txt

install args:
  ./venv/bin/pip3 install {{args}}
  ./venv/bin/pip3 freeze > requirements.txt

