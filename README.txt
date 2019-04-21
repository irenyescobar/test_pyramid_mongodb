
Getting Started
---------------

- Change directory into your newly created project.

    cd test_pyramid_mongodb

- Create a Python virtual environment.

    python -m venv env

- Upgrade packaging tools.

-change directory to env/Scripts and run the commands in sequence:

    pip install --upgrade pip setuptools   

    pip install -e <path your project> 

    python setup.py develop

- Run your project.

    pserve development.ini

- look at http://localhost:6543
