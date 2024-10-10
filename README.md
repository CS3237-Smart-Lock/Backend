This is the backend repository for the smart lock project for CS3237. This repository includes codes involving

- REST server (Flask)
- Database (SQLite3)
- Potentially Websocket to come

I use `just` as a script runner, but you can also take a look in the `justfile` and run the commands separately
First, create a virtual environment and install dependencies

```shell
python -m venv venv
just install-all
```

Then start the server with 

``shell
just serve
``

