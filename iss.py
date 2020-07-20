#!/usr/bin/env python

__author__ = 'Reggy Tjitradi guided by Stew and support from Howard, Ramon, and Ruth'


import requests  # https://realpython.com/python-requests/
import time  # https://docs.python.org/3/library/time.html
import turtle
# https://docs.python.org/3.3/library/turtle.html?highlight=turtle
import json  # https://docs.python.org/3/library/json.html


iss = turtle.Turtle()
in_loc = turtle.Turtle()


def current_astronauts():
    astros_data = requests.get('http://api.open-notify.org/astros.json')
    astros_obj = json.loads(astros_data.text)
    print('Currently there are {0} astronauts \
in space. These are the details:'.format(astros_obj['number']))
    for person in astros_obj['people']:
        print('\t{0} who is onboard spacecraft: {1}'.format(person['name'], person['craft']))


def iss_location():
    iss_data = requests.get('http://api.open-notify.org/iss-now.json')
    if iss_data.status_code == 200:
        iss_obj = json.loads(iss_data.text)
        lat = float(iss_obj['iss_position']['latitude'])
        long = float(iss_obj['iss_position']['longitude'])
        move_iss(lat, long)
    else:
        print('result error', iss_data.status_code)


def move_iss(lat, long):
    global iss
    iss.penup()
    iss.goto(long, lat)


def screen_setup(screen):
    global iss, in_loc
    screen.setup(720, 360)
    screen.title('Here is where the ISS is located')
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)
    in_loc.shape('circle')
    in_loc.turtlesize(.3, .3, .3)
    in_loc.color('yellow')
    turtle.register_shape('iss.gif')
    iss.shape('iss.gif')


def over_indianapolis(long, lat):
    payload = {'lat': lat, 'lon': long}
    res = requests.get('http://api.open-notify.org/iss-pass.json',
                       params=payload)
    if res.status_code == 200:
        res_obj = json.loads(res.text)
        return res_obj['response'][0]['risetime']
    else:
        print('something is wrong', res.status_code)


def plot_indianapolis():
    global in_loc
    in_loc.penup()
    in_loc.goto(-86.159536, 39.778117)
    next_time = over_indianapolis(-86.159536, 39.778117)
    next_time = time.ctime(next_time)
    in_loc.write(next_time)


def main():
    current_astronauts()
    global iss, in_loc
    screen = turtle.Screen()
    screen_setup(screen)
    iss_location()
    plot_indianapolis()


if __name__ == '__main__':
    main()
    turtle.mainloop()
