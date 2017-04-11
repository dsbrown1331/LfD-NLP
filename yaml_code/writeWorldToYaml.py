# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:25:04 2017

@author: daniel
"""

import yaml

#script to output world into yaml file

shapes = {'circle':0,'square':1,'triangle':2,'star':3,'diamond':4}
colors = {'blue':0, 'red':1,'green':2,'purple':3,'yellow':4,'orange':5}


#settings
width = 100
height = 100
num_objects = 2         #objects starting on table
table_length = 80
table_topright = (0,0)
table_length = 70
staging_topright = (80,80)
staging_length = 20
object_width = 5
task_object = [object_width,2,3]  #purple triangle
goal = [10,60,object_width,object_width]
object1 = [40,30,object_width,0,1]
object2 =  [60,10,object_width,1,2]

#create a dictionary and save to yaml file format
objects = [object1, object2]
staging_area = [staging_topright[0], staging_topright[1], staging_length, staging_length ]
table = [table_topright[0], table_topright[1], table_length, table_length]
data = {}
data['width'] = width
data['height'] = height
data['objects'] = objects
data['table'] = table
data['task_object'] = task_object 
data['staging_area'] = staging_area
data['goal'] = goal

stream = file('output.yaml', 'w')
yaml.dump(data, stream)    # Write a YAML representation of data to 'document.yaml'.
print yaml.dump(data)      # Output the document to the screen.



