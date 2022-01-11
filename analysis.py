import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import analysis
import argparse

db_connection_str = 'sqlite:////Users/oguz.kirazdiken/Workspace/perseus/challenge/db.sqlite3'
db_connection = create_engine(db_connection_str)


# Average complete time of a course
def get_average_complete_times():
    avg_complete_time = pd.read_sql('''
        select aco.title,round(avg(julianday(completedDate) - julianday(startDate)),2) as avg_complete_day
        from api_certificate ace
        left join api_course aco on ace.course = aco.id
        group by aco.title
        ''', con=db_connection)

    plt.figure(figsize=(13, 6))

    ax = plt.bar(avg_complete_time.title, avg_complete_time.avg_complete_day)

    for r in ax:
        h = r.get_height()
        plt.text(r.get_x() + r.get_width() / 2., h / 2., "%d" % h, ha="center",
                 va="center", color="white", fontsize=10, fontweight="bold")

    plt.title('Average Complete Time Of a Course')

    plt.xticks(rotation=20)

    plt.ylabel("Average Complete Day")

    return plt.show()


# Average amount of users time spent in a course
def get_avg_time_spent():
    avg_time_spent = pd.read_sql('''
        with total_time_spent as (
            select course, user, sum(julianday(completedDate) - julianday(startDate)) as time_spent
            from api_certificate
            group by course, user
        )
        select aco.title, round(avg(tts.time_spent),2) as average_time_spent
        from total_time_spent tts
        left join api_course aco on tts.course = aco.id
        group by aco.title
        ''', con=db_connection)
    print(avg_time_spent)


# Average amount of users time spent for each course individually
def get_avg_time_spent_ind():
    avg_time_spent_ind = pd.read_sql('''
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
    ''', con=db_connection)
    print(avg_time_spent_ind)


# Report of fastest vs. slowest users completing a course
def get_course_completes():
    min_max_course_completes = pd.read_sql('''
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
        ''', con=db_connection)
    print(min_max_course_completes)


# Amount of certificates per customer
def get_certificates_per_customer():
    certificates_per_customer = pd.read_sql('''
        select apu.firstName || " " || apu.lastName as fullName,count(distinct ace.course) as num_of_unique_certificate
        from api_certificate ace
        left join api_user apu on ace.user = apu.id
        group by apu.firstName,apu.lastName
        ''', con=db_connection)
    print(certificates_per_customer)


# Which time user starts mostly
def get_user_starts_mostly():
    user_starts_mostly = pd.read_sql('''
        select strftime('%H',startDate) as hour,count(distinct id) as num_of_user
        from api_certificate
        group by strftime('%H',startDate)
        ''', con=db_connection)

    colors = ['#FF0000', '#0000FF', '#FFFF00',
              '#ADFF2F', '#FFA500', '#FF9999']

    plt.figure(figsize=(13, 8))

    plt.pie(user_starts_mostly.num_of_user, colors=colors, labels=user_starts_mostly.hour, autopct='%1.1f%%',
            pctdistance=0.85)

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    fig.gca().add_artist(centre_circle)

    plt.title('Which Time User Starts Mostly (Hour)')

    return plt.show()


# Most frequent used courses
def get_most_frequent_used_courses():
    frequent_used_courses = pd.read_sql('''
        select aco.title,count(distinct ace.id) as num_of_used
        from api_certificate ace
        left join api_course aco on ace.course = aco.id
        group by aco.title
        ''', con=db_connection)

    plt.figure(figsize=(13, 6))

    ax = plt.bar(frequent_used_courses.title, frequent_used_courses.num_of_used)

    for r in ax:
        h = r.get_height()
        plt.text(r.get_x() + r.get_width() / 2., h / 2., "%d" % h, ha="center",
                 va="center", color="white", fontsize=10, fontweight="bold")

    plt.title('Course Usage Frequency')

    plt.xticks(rotation=20)

    plt.ylabel("Frequency")

    return plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--get_average_complete_times", action="store_true")
    parser.add_argument("--get_avg_time_spent", action="store_true")
    parser.add_argument("--get_avg_time_spent_ind", action="store_true")
    parser.add_argument("--get_course_completes", action="store_true")
    parser.add_argument("--get_certificates_per_customer", action="store_true")
    parser.add_argument("--get_user_starts_mostly", action="store_true")
    parser.add_argument("--get_most_frequent_used_courses", action="store_true")
    args = parser.parse_args()

    if args.get_average_complete_times:
        analysis.get_average_complete_times()

    if args.get_avg_time_spent:
        analysis.get_avg_time_spent()

    if args.get_avg_time_spent_ind:
        analysis.get_avg_time_spent_ind()

    if args.get_course_completes:
        analysis.get_course_completes()

    if args.get_certificates_per_customer:
        analysis.get_certificates_per_customer()

    if args.get_user_starts_mostly:
        analysis.get_user_starts_mostly()

    if args.get_most_frequent_used_courses:
        analysis.get_most_frequent_used_courses()
