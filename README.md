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
python3 analysis.py --get_avg_time_spent_ind
```

Query:
```sql
with total_time_spent as (
    select course, user, sum(julianday(completedDate) - julianday(startDate)) as time_spent
    from api_certificate
    group by course, user
)
select aco.title,apu.firstName,apu.lastName,round(avg(tts.time_spent),2) as average_time_spent_day
from total_time_spent tts
    left join api_course aco on tts.course = aco.id
    left join api_user apu on tts.user = apu.id
    group by aco.title,apu.firstName,apu.lastName
```

Output:

The query result has 247 rows. The first 5 row are shown below

|   title |firstName | lastName | average_time_spent_day|
|---------|----------|----------|-----------------------|
| Darknet |   Adolph |  Schaden |                  45.51|
| Darknet | Adrianna |   Kemmer |                   5.83|
| Darknet |   Austyn |   Brakus |                 139.87|
| Darknet |    Barry |    Lemke |                  11.15|
| Darknet | Benedict |  Wiegand |                 438.41|

#### Report of fastest vs. slowest users completing a course

```python
python3 analysis.py --get_course_completes
```

Query:
```sql
with min_max_certificates as (
    select course,
           max(julianday(completedDate) - julianday(startDate)) as max_complete_day,
           min(julianday(completedDate) - julianday(startDate)) as min_complete_day
    from api_certificate
    group by course
)
select aco.title,
       round(mmc.max_complete_day,2) as max_complete_day,apu_max.firstName || " " || apu_max.lastName as max_completed_user_fullName,
       round(mmc.min_complete_day,2) as min_complete_day,apu_min.firstName || " " || apu_min.lastName as min_completed_user_fullName
from min_max_certificates mmc
left join api_certificate ace_min on mmc.course = ace_min.course and mmc.min_complete_day = (julianday(ace_min.completedDate) - julianday(ace_min.startDate))
left join api_certificate ace_max on mmc.course = ace_max.course and mmc.max_complete_day = (julianday(ace_max.completedDate) - julianday(ace_max.startDate))
left join api_course aco on mmc.course = aco.id
left join api_user apu_min on ace_min.user = apu_min.id
left join api_user apu_max on ace_max.user = apu_max.id
```

Output:

|title								|max_complete_day   |max_completed_user_fullName |min_complete_day  |min_completed_user_fullName |
|-----------------------------------|-------------------|----------------------------|------------------|----------------------------|
|Protect yourself against Phishing	|203.05				|Reba Rath					 |1					|Marco Beer					 |
|GDPR								|184.74				|Shad Marvin				 |0.85				|Marjolaine Friesen			 |
|What is cyber security?		    |245.25				|Jameson Wilderman			 |0.44				|Vincent Gorczany			 |
|Darknet							|286.42				|Misael Rohan				 |0.45				|Norris Raynor				 |
|How do Hackers act?				|310.83				|Harrison Heathcote			 |0.4				|Fredy Weissnat				 |
|Internet & Smart Home				|144.28				|Harley Donnelly			 |0.31				|Charley Jacobi				 |


#### Amount of certificates per customer

```python
python3 analysis.py --get_certificates_per_customer
```

Query:
```sql
select apu.firstName || " " || apu.lastName as fullName,count(distinct ace.course) as num_of_unique_certificate
from api_certificate ace
left join api_user apu on ace.user = apu.id
group by apu.firstName,apu.lastName
```

Output:

The query returns 50 rows. The first 5 rows are shown below

|    fullName     | num_of_unique_certificate  |
|-----------------| ---------------------------|
| Abigail O'Hara  |                      5     |
| Adolph Schaden  |                      4     |
|Adrianna Kemmer  |                      5     |
|   Ansel Heller  |                      5     |
|  Austyn Brakus  |                      5     |
|    Barry Lemke  |                      5     |



#### Which time user starts mostly

```python
python3 analysis.py --get_user_starts_mostly
```

Query:
```sql
select strftime('%H',startDate) as hour,count(distinct id) as num_of_user
from api_certificate
group by strftime('%H',startDate)
```

Output:
![Figure_2](https://user-images.githubusercontent.com/53194457/148920565-16c44442-adcf-4546-95d7-2d33aa80a3d3.png)



#### Most frequent used courses

```python
python3 analysis.py --get_most_frequent_used_courses
```

Query:
```sql
select aco.title,count(distinct ace.id) as num_of_used
from api_certificate ace
left join api_course aco on ace.course = aco.id
group by aco.title
```

Output:
![Figure_3](https://user-images.githubusercontent.com/53194457/148920579-f2687e44-0007-4393-9c12-362207212096.png)

