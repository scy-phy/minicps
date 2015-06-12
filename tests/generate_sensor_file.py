#!/usr/bin/python

import random

nb_values = 100000
sensor_file = open("../temp/monitoring_test/sensor.txt", 'w')

start = 5.0
maxi = 5.0 # linear function 
mini = -5.0

for i in range(nb_values):
    nb = random.uniform(start-mini, start+maxi)
    mzx min += 200
    sensor_file.write("{:3.2f}\n".format(nb))

sensor_file.close()
