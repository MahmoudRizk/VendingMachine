# Vending Machine

An API service for a vending machine, allowing users with multiple roles to interact with.

## Overview

The solution is inspired in its implementation by the Onion Architecture & DDD. It is divided into three main layers
which are the domain, service & api layers.
<br>

Each Domain has its own repository so that the database model is separated from the domain model which provides a good
decoupling for the business logic from the database layer & its technologies.

SQLAlchemy ORM is used in implementing the domain's repository, taking advantage if its powerful capabilities in
defining the database models, and the ability to switch from database vendor to another.

Relational database is used with SQlite for simplicity.

### Domain

Domain layer is the layer where the main entities of the project lives. We are having three main entities which are

* Users
    * The people who interact with the vending machine to buy or sell products.
* Products
    * The definition of the products which is being sold in the vending machine.
* Vending Machine
    * The main part of the project, which contains the inventory of the product being sold.

### Service

Is the layer which have the complex business logic and acts as the bridge between the API and the domain.

### API

The outer layer which has the API that interacts with the outer world.

## Setup

Requirements

```
python >= 3.8
```

* Create virtual environment
    ```commandline
    python -m venv env
    ```

* Activate the virtual environment

  ```commandline
  source env/bin/activate
  ```

* Install requirements

  ```commandline
  pip install -r requirments.txt
  ```

* Run Setup Script
  ```commandline
  python setup.py
  ```
  * The script will create the database with all the tables along with the administrator user.

* Run the server
  ```commandline
  python main.py  
  ```