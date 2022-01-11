### PerseusChallenge

The project aim is creating a database structure and API views that can ingest three different type of objects Users, Course and Certficates.

API views and the data model were developed on [Django Rest Framework](https://www.django-rest-framework.org/). 

Pandas, SQLalchemy, and Matplotlib libraries were used for analysis and visualizations.

The following table shows overview of the REST APIs:

|    Methods    |         Urls           |                    Actions                      |
| ------------- | ---------------------  | ----------------------------------------------- |
|     POST      | api/userCreate/        |              create new User                    |
|     POST      | api/courseCreate/      |              create new Course                  |
|     POST      | api/certificateCreate/ |            create new Certificate               |

### Installation

To get the project up and running in your local, go to the file location you want to install and run the following command.

```python
git clone https://github.com/oguzkirazdiken/PerseusChallenge.git
```

It is highly recommended to run on virtual environment. Firstly, set your virtual env and activate it.

```python
python3 -m venv env
source env/bin/activate
```

Change current working directory to the directory where requirements.txt is located and run the following cone in your shell.

```python
cd challenge
pip3 install -r requirements.txt
```
We have a SQLite database. So it is good to start with initial migration before running our Django Rest API.

```python
python3 manage.py makemigrations
python3 manage.py migrate
```

```python
python3 manage.py runserver
```


### Data Analysis and Visualizations

The example data consists of 50 Users, 6 Courses and 500 Certificates.



