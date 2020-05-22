#!/usr/bin/python
import tkinter as tk
from math import sin, cos, pi
import time
import sys
import json
import os
from colour import Color
import datetime


class clock(tk.Tk):

    def __init__(self, config):
        tk.Tk.__init__(self)
        self.title('B Clock')
        # self.wm_overrideredirect(True)
        self.handles = {}

        if os.name == 'posix':
            self.wm_attributes('-type', 'normal')

        if config['noTitle']:
            self.wm_overrideredirect(True)
        self.resizable(False, False)
        self.wm_attributes(
            '-alpha', config['alpha'] if 'alpha' in config else 0.5)
        self.wm_attributes('-topmost', True)
        self.radius = config['radius'] if 'radius' in config else 60
        self.x_offset = config['offset'] if 'offset' in config else 2
        self.y_offset = config['offset'] if 'offset' in config else 2
        self.xcentre = self.x_offset + self.radius
        self.ycentre = self.y_offset + self.radius
        self.center_dot_radius = 5
        self.w = tk.Canvas(self, width=2 * self.radius + 2 * self.x_offset, height=2 * self.radius + 2 * self.y_offset,
                           bg=config['backgroundColor'] if 'backgroundColor' in config else 'Cyan')
        self.w.pack()
        self.w.create_oval(self.x_offset, self.y_offset, 2 * self.radius +
                           self.x_offset, 2 * self.radius + self.y_offset)  # Main circle
        self.w.pack()
        self.w.create_oval(self.x_offset + self.radius - self.center_dot_radius, self.y_offset + self.radius - self.center_dot_radius,
                           self.x_offset + self.radius + self.center_dot_radius, self.y_offset + self.radius + self.center_dot_radius, fill='Black')  # Centre Dot
        self.w.pack()
        # Second Hand
        # self.w.create_line(0, 0, 0, 0, fill='Blue', width=1, tags='seconds')
        # Minute Hand
        # self.w.create_line(0, 0, 0, 0, fill='Blue', width=2, tags='minute')
        # Hour Hand

        for i in range(0, 12):
            # Drawing hour co-orninates
            self.degree = i*30
            self.w.create_line((self.radius * cos((self.degree*pi)/180)) + self.xcentre, (self.radius * sin((self.degree*pi)/180)) +
                               self.ycentre, ((self.radius - self.x_offset) * cos((self.degree*pi)/180)) + self.xcentre, ((self.radius - self.x_offset) * sin((self.degree*pi)/180)) + self.ycentre, fill='Red', width=6)

        # for i in range(0, 60):
        #     # Drawing minute co-orninates
        #     self.degree = i*6
        #     self.w.create_line((self.radius * cos((self.degree*pi)/180)) + 270, (self.radius * sin((self.degree*pi)/180)
        #                                                                          ) + 270, (240 * cos((self.degree*pi)/180)) + 270, (240 * sin((self.degree*pi)/180)) + 270)

        for i, c in enumerate(config['handles']):
            tag = c['label'] + '_' + str(i)
            self.handles[tag] = c
            self.w.create_line(0, 0, 0, 0, fill=c['colour'],
                               width=c['width'] if 'width' in c else 4, tags=tag)
            color = Color(c['colour'])
            color.set_saturation(0.5)
            self.w.create_line(0, 0, 0, 0, fill=color.get_web(),
                               width=2, tags=tag + '_minute')
            self.w.create_text(
                self.radius / 5, 2 * (i + 1) * 10, text=c['label'], fill=c['colour'], font=('Times New Roman', 10), tags=tag + '_TEXT')
            self.change_clock(tag)

    def change_clock(self, tag):
        utc = datetime.datetime.utcnow()
        delta = datetime.timedelta(
            hours=int(self.handles[tag]['offset']), minutes=(float(self.handles[tag]['offset']) - int(self.handles[tag]['offset'])) * 60)
        tz_time = utc + delta
        hour = tz_time.hour
        minute = tz_time.minute
        # seconds = time.localtime()[5]
        # # seconds
        # sec_degree = seconds*6 - 90
        # sec_angle = (sec_degree*pi)/180
        # sec_x = 270 + 230 * cos(sec_angle)
        # sec_y = 270 + 230 * sin(sec_angle)
        # self.w.coords('seconds', (self.xcentre, self.xcentre, sec_x, sec_y))
        # minute
        min_degree = minute*6 - 90
        min_angle = (min_degree*pi)/180
        hour_len = self.handles[tag]['length'] if 'length' in self.handles[tag] else .75
        min_x = self.xcentre + (hour_len + .1) * self.radius * cos(min_angle)
        min_y = self.ycentre + (hour_len + .1) * self.radius * sin(min_angle)
        self.w.coords(tag + '_minute', (self.xcentre,
                                        self.xcentre, min_x, min_y))
        # hour
        hour_degree = hour*30 + ((min_degree + 90) / 360) * 30 - 90
        hour_angle = (hour_degree*pi)/180
        hour_x = self.xcentre + hour_len * self.radius * cos(hour_angle)
        hour_y = self.ycentre + hour_len * self.radius * sin(hour_angle)
        self.w.coords(tag, (self.xcentre, self.ycentre, hour_x, hour_y))
        # self.w.coords(
        #     tag + '_TEXT', (hour_x + self.x_offset, hour_y + self.y_offset))
        self.after(1000, self.change_clock, tag)


config_file = os.environ['HOME'] + '/.config/bclock/config.json'
if len(sys.argv) > 1:
    config_file = sys.argv[1]

config = None
try:
    with open(config_file) as f:
        config = json.load(f)
except:
    print('Config file invalid. Exiting...')
    sys.exit(1)

clock = clock(config)
clock.mainloop()
