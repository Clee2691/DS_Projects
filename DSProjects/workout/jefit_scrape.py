from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

def date_list_maker(year):
    
    date_list = []

    for month in range(1, 13):
        for day in range(1, 32):
            try:
                date_list.append(datetime(year, month, day).strftime("%Y-%m-%d"))
                #print(datetime(2020, month, day).strftime("%Y-%m-%d"))
            except ValueError:
                pass
    return date_list

def entry_grabber(exercise_elements):
    log_entry_list = []

    for exercise in exercise_elements:
        # Exercise Details
        log_id = exercise.select("input[name='logid']")[0]['value']
        exercise_id = exercise.select("input[name='exerciseid']")[0]['value']
        exercise_name = exercise.select("input[name='ename']")[0]['value']
        log_date = exercise.select("input[name='date']")[0]['value']

        x = 1
        # weight and rep for each exercise
        for weight, rep in zip(exercise.select("input[name='weight']"), exercise.select("input[name='rep']")):

            set_number = x # Specify which set number it is; not hardcoded in a value
            weight_value = weight['value']
            rep_value = rep['value']

            log_entry_list.append([log_date, log_id, exercise_id, exercise_name, set_number, weight_value, rep_value])

            x += 1

    return log_entry_list

def csv_maker(entry):
    try:
        with open('workout_list.csv', 'a', newline='') as workout_file:
            writer=csv.writer(workout_file, delimiter=',')
            for data in entry:
            writer.writerow(data)

    except:
        with open('workout_list.csv', 'w', newline ='') as workout_file:
            writer = csv.writer(workout_file, delimiter=',')
            writer.writerow(['date', 'log_id', 'exercise_id', 'exercise_name', 'set_number', 'weight', 'rep'])

