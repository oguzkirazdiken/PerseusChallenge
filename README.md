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

Change current working directory to the directory where requirements.txt is located and run the following code in your shell.

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

The example data consists of 50 Users, 6 Courses and 500 Certificates. After the ingestion phase, the following analyses were provided on `anaysis.py`. You can also run these analyses on your shell with specified arguments.

#### Average complete time of a course

```python
python3 analysis.py --get_average_complete_times
```

Query:
```sql
select aco.title,round(avg(julianday(completedDate) - julianday(startDate)),2) as avg_complete_day
from api_certificate ace
left join api_course aco on ace.course = aco.id
group by aco.title
```
Output:

![Figure_1](https://user-images.githubusercontent.com/53194457/148920282-99ef2b4a-387f-41f5-b67c-ece6ce1fa731.png)

#### Average amount of users time spent in a course

```python
python3 analysis.py --get_avg_time_spent
```
Query:
```sql
with total_time_spent as (
    select course, user, sum(julianday(completedDate) - julianday(startDate)) as time_spent
    from api_certificate
    group by course, user
)
select aco.title, round(avg(tts.time_spent),2) as average_time_spent
from total_time_spent tts
    left join api_course aco on tts.course = aco.id
    group by aco.title
```
Output:

|                              title | average_time_spent |
| ---------------------------------  | -------------------|
|                            Darknet |             149.60 |
|                               GDPR |             117.30 |
|                How do Hackers act? |             184.69 |
|              Internet & Smart Home |              81.85 |
|  Protect yourself against Phishing |             133.63 |
|            What is cyber security? |             136.97 |


#### Average amount of users time spent for each course individually

```python
python3 analysis.py --get_avg_time_spent
```

