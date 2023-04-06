# tech-interview-cafeto-software
Repository with the technical interview test for Cafeto Software


## Build and Local Deployment

For building the application on a local enviroment, the following steps must be carried out

```bash
$ # First, clone the repo
$ git clone https://github.com/scf-12/tech-interview-cafeto-software.git
$ cd tech-interview-cafeto-software-5
$
$ # Define a virtual environment
$ python3 -m venv venv
$ . venv/bin/activate
$
$ # Install requirements
$ pip3 install -r requirements.txt
$
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the UI in browser: http://127.0.0.1:5000/
```

<br />

## Code-base structure

The project has a simple structure, represented as bellow:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |  __init__.py
   |    |  handlers.py
   |    |  models.py
   |    |  views.py
   |
   |-- postman/
   |    |  CafetoSoftware_Interview.postman_collection.json
   |
   |-- .gitignore
   |-- LICENSE
   |-- README.md
   |-- requirements.md
```

<br />
