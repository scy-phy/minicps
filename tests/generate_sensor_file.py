#!/usr/bin/python

import random

nb_values = 100000
sensor_file = open("../temp/monitoring_test/sensor.txt", 'w')
maxi = 1600.0 # linear function 
mini = 0.0
for i in range(nb_values):
    nb = random.uniform(mini, maxi)
    sensor_file.write("{:3.2f}\n".format(nb))

sensor_file.close()
