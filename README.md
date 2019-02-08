# Politico

Politico is a web application to handle elections. Politico enables a wide range of users including administrators and normal users(voters and politicians). Users can either register or login. A voter can vote and view the politicians they have voted for. A voter can become a politician by expressing interest in a political office. The admin adds political offices, political parties and admin users. 

[![Coverage Status](https://coveralls.io/repos/github/mogoria/Politico/badge.svg?branch=develop)](https://coveralls.io/github/mogoria/Politico?branch=develop)
[![Build Status](https://travis-ci.org/mogoria/Politico.svg?branch=develop)](https://travis-ci.org/mogoria/Politico)
[![Maintainability](https://api.codeclimate.com/v1/badges/1341fcb8087f9f135ab7/maintainability)](https://codeclimate.com/github/mogoria/Politico/maintainability)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

You can find a live demo of the application [here](https://politico-nbo-cycle-37.herokuapp.com/api/v1)

### Prerequisites

You need the following in order for the application to run effectively.

```
python 3.6
postman
```

### Installing

Clone this repository
```
git clone https://github.com/mogoria/politico
```

You'll need to set up a virtual environment.

Use the following command in order to create one. First off, navigate to the root of the project. Type the command

```
virtual env 
```

This creates a virtual environment called env.
Next, activate the environment using the command.

```
source env/bin/activate
```
Finally, you need to install the packages.
Run the command.

```
pip install  requirements.txt
```
set up environental variables
```
export FLASK_APP=run.py

export FLASK_DEBUG=1

export FLASK_ENVIRONMENT=development
```
## Running the tests

pytest is the recommended test runner for this application.
To run tests, use the command
```
pytest app/tests
```

in order to view coverage, run
```
pytest --cov=app app/tests
```

## Endpoints
|   METHOD       |    URL                      | FUNCTION
|  ------------  | ----------                   |  ---------
|   POST         | /api/v1/offices           |  create an office 
|   POST         | /api/v1/parties           |  create a party
|   GET          | /api/v1/offices           |  find all offices
|   GET          | /api/v1/parties           | find all parties
|   GET          | /api/v1/offices/<int:office_id> | find a specific office with the office_id
|   GET          | /api/v1/parties/<int:party_id>  | find a specific party with the party_id
|   DELETE       | /api/v1/offices/<int:office_id> | delete a specific office with the office_id
|   DELETE       | /api/v1/parties/<int:party_id>  | delete a specific party with  the party_id

## Authors

* **Tukmen Mogoria** - *Initial work* - 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


