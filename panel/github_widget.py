#!/usr/bin/python

import json
import datetime
import os
from urllib.request import urlopen
from number_widget import NumberWidget


class GithubWidget(NumberWidget):
    def __init__(self):
        super(GithubWidget, self).__init__('G')
        self.url = self.get_url()
        self.update_time = 60 * 5

    def update_number(self):
        try:
            self.number = self.get_commits()
        except Exception as e:
            print("Couldn't get github commits")
            print(e)
            self.number = 0

    def get_commits(self):
        raw = self.get_raw_json()
        parsed = json.loads(raw)

        today = 0

        for event in parsed:
            time = event['created_at'].split("T")[0]

            try:
                amount = int(event['payload']['size'])
            except KeyError:
                amount = 0

            if self.check_time(time):
                today += amount

        return today

    def get_raw_json(self):
        response = urlopen(self.url)
        return response.read().decode()

    @staticmethod
    def check_time(time_str):
        spl = time_str.split('-')
        year = int(spl[0])
        month = int(spl[1])
        day = int(spl[2])

        now = datetime.datetime.now()

        isToday = \
            now.year == year and \
            now.month == month and \
            now.day == day

        return isToday

    @staticmethod
    def get_url():
        with open("./dotfiles/panel/git_token", 'r') as f:
            token = f.read()

        return 'https://api.github.com/users/mishajw/events?access_token=' + token
