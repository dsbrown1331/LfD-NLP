# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:07:46 2017

@author: daniel
"""

#first need to install yaml 
#sudo apt-get install python-yaml

import yaml

#how to open a yaml file
with open("world.yaml", 'r') as stream:
    try:
        world_settings = yaml.load(stream)
        print world_info 
    except yaml.YAMLError as exc:
        print exc 

#how to access elements
print world_settings['staging_area']


#how to save to yaml file
stream = file('output.yaml', 'w')
yaml.dump(world_settings, stream)    # Write a YAML representation of data to 'document.yaml'.
print yaml.dump(world_settings)      # Output the document to the screen.