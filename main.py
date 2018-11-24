#!/usr/bin/python3

import datetime
import threading
import time

from phue import Bridge


# Light Ids
BATHROOM = 1
LIVING_ROOM = 2
BEDROOM = 3
BRIDGE_IP = '192.168.0.123'

# weekday
# - 0: monday
# - 6: sunday

# Schedules

wake_up_weekend_data = {
    'command': 'fade_in',
    'hour': 9,
    'minute': 30,
    'light_id': BEDROOM,
    'transition_time': 1800,  # 30 minutes
    'weekdays': [5, 6],       # weekend only
    }

wake_up_week_data = {
    'command': 'fade_in',
    'hour': 7,
    'minute': 30,
    'light_id': BEDROOM,
    'transition_time': 1800,           # 30 minutes
    'weekdays': [0, 1, 2, 3, 4],       # weekend only
    }

sleep_week_data = {
    'command': 'fade_out',
    'hour': 23,
    'minute': 00,
    'light_id': BEDROOM,
    'transition_time': 1800,           # 30 minutes
    'weekdays': [0, 1, 2, 3, 4, 5, 6],
    }


# Commands

def fade_in(bridge, light_id, transition_time, bri=254):
    command = { 'transitiontime' : transition_time,
                'on' : True,
                'bri' : bri }
    bridge.set_light(light_id, command)


def fade_out(bridge, light_id, transition_time, bri=1):
    command = { 'transitiontime' : transition_time,
                'on' : True,
                'bri' : bri }
    bridge.set_light(light_id, command)


def should_perform_command(now, schedule_data):
  return now.hour == schedule_data['hour'] and \
         now.minute == schedule_data['minute'] and \
         now.weekday() in schedule_data['weekdays']


def schedule(bridge, schedule_data):
  while True:
    time.sleep(1)
    now = datetime.datetime.now()

    if should_perform_command(now, schedule_data):

        if schedule_data['command'] == 'fade_in':
          print("FADING IN")
          fade_in(bridge, schedule_data['light_id'], schedule_data['transition_time'])

        elif schedule_data['command'] == 'fade_out':
          print("FADING OUT")
          fade_out(bridge, schedule_data['light_id'], schedule_data['transition_time'])

        print("Sleeping for 1 minute")
        time.sleep(61)  # Sleep for more than one minute


def main():

# Bridge connection
  print("Connecting to Bridge")
  bridge = Bridge(BRIDGE_IP)
  print("Connected\n")
  print("API status")
  print(bridge.get_api())
  print("\n\n")

  # Starting Threads
  for schedule_data in [wake_up_week_data, wake_up_weekend_data, sleep_week_data]:
    print("Starting new thread with schedule_data:")
    print(schedule_data)

    threading.Thread(
        target=schedule,
        args=(bridge, schedule_data)
        ).start()

  # Infinite Loop
  while 1:
    pass
