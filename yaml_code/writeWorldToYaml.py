#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:25:04 2017

usage: 
python writeWorldToYaml.py -o object_color object_shape -l landmark_color landmark_shape -r relation -n numObjects -f output_filename

@author: daniel
"""

import yaml
import sys
import numpy as np
import random


#settings
width = 1300
height = 1000
table_width = 800
table_topleft = (100,100)  #(x,y) coordinate of top left corner of table
staging_topleft = (1000,100)
object_width = 100
staging_length = object_width
object_buffer = 10
target_width = object_width
near_range = 2 * object_buffer + 2 * object_width
far_range = near_range + 2 * object_width + 2 * object_buffer

shapes = {'circle':0,'square':1,'triangle':2,'star':3,'diamond':4}
colors = {'blue':0, 'red':1,'green':2,'purple':3,'yellow':4,'orange':5}
id_to_shape = {item[1]:item[0] for item in shapes.items()}
id_to_color = {item[1]:item[0] for item in colors.items()}


#Note all x,y are for upper left corner of shape
def placeLandmark(relationship):
    if relationship == 'right':
        #place so there is room for at least one object to right of target
        x = random.randint(table_topleft[0] + object_buffer, table_width - 2 * object_buffer - 2 * object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'left':
        #place so there is room for at least one object to left of target
        x = random.randint(table_topleft[0] + 2 * object_buffer + object_width, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'up':
        #place so there is room above landmark for at least one object
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + 2 * object_buffer + object_width, table_width - object_buffer - object_width)
    elif relationship == 'down':
        #place so there is room below landmark for at least one object
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - 2 * object_buffer - 2 * object_width)
    elif relationship == 'on':
        #place landmark anywhere
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'near' or relationship == 'far':
        #place landmark any where
        #x = random.randint(table_topleft[0] + 2 * object_buffer + object_width, table_width - 2 * object_buffer - 2 * object_width)
        #y = random.randint(table_topleft[1] + 2 * object_buffer + object_width, table_width - 2 * object_buffer - 2 * object_width)
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    else:
        print "ERROR: unknown relationship"
        sys.exit(0)
    return x,y

#Note all x,y are for upper left corner of shape
def placeTarget(landmark_pos, relationship):
    landmark_x, landmark_y = landmark_pos
    if relationship == 'right':
        #place so it is in right half-plane based on position of target
        x = random.randint(landmark_x + object_width + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'left':
        #place to it is in left-half plane of position target
        x = random.randint(table_topleft[0] + object_buffer, landmark_x - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'up':
        #place above landmark
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + object_buffer, landmark_y - object_buffer - object_width)
    elif relationship == 'down':
        #place target below landmark
        x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        y = random.randint(table_topleft[1] + landmark_y + object_width + object_buffer, table_width - object_buffer - object_width)
    elif relationship == 'on':
        #place target on landmark
        x = landmark_x
        y = landmark_y
    elif relationship == 'near':
        #place within near_range of landmark
        target_pos = placeObjectNearLandmark([landmark_x, landmark_y])
        x = target_pos[0]
        y = target_pos[1]
    elif relationship == 'far':
        #place outside of far_range of landmark
        target_pos = placeObjectFarFromLandmark([landmark_x, landmark_y])
        x = target_pos[0]
        y = target_pos[1]
    else:
        print "ERROR: unknown relationship"
        sys.exit(0)
    return x,y


def intersectsOtherObjects(new_obj, objects):
    #for each object in objects check if my absolute x or y distance is less than object diameter with some buffer space in between
    for obj in objects:
        #check x dist
        if abs(new_obj[0] - obj[0]) < (object_width + object_buffer):
            if abs(new_obj[1] - obj[1]) < (object_width + object_buffer):
                return True

    return False
    
def placeObjectFarFromLandmark(landmark):
    reject_count = 0
    while True:
        #generate candidate position until we find one that fits in the world and
        # is within near_range of landmark
        new_obj_x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        new_obj_y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
        new_obj = [new_obj_x, new_obj_y]
        #print new_obj
        if not intersectsOtherObjects(new_obj, [landmark]) and dist(new_obj, landmark) >= far_range:
            break
        reject_count += 1
        if reject_count > 500:
            print "ERROR: world is too small or far_range too big, can't fit target"
            sys.exit()

    return new_obj
    
def placeObjectNearLandmark(landmark):
    reject_count = 0
    while True:
        #generate candidate position until we find one that fits in the world and
        # is within near_range of landmark
        new_obj_x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        new_obj_y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
        new_obj = [new_obj_x, new_obj_y]
        #print new_obj
        if not intersectsOtherObjects(new_obj, [landmark]) and dist(new_obj, landmark) <= near_range:
            break
        reject_count += 1
        if reject_count > 500:
            print "ERROR: world is too small or near_range too small, can't fit target"
            sys.exit()

    return new_obj

"""compute distance between centers of objects"""
def dist(obj1, obj2):
    center_x1 = obj1[0] + object_width / 2.0
    center_x2 = obj2[0] + object_width / 2.0
    center_y1 = obj1[1] + object_width / 2.0
    center_y2 = obj2[1] + object_width / 2.0
    delta_x = (center_x1 - center_x2)
    delta_y = (center_y1 - center_y2)
    return np.sqrt(delta_x ** 2 + delta_y ** 2)

#TODO add feature selection to be unique over items so we don't have duplicates
def generateNewObject(objects):
    reject_count = 0
    while True:
        #generate candidate position until we find one that fits in the world
        new_obj_x = random.randint(table_topleft[0] + object_buffer, table_width - object_buffer - object_width)
        new_obj_y = random.randint(table_topleft[1] + object_buffer, table_width - object_buffer - object_width)
        new_obj_shape = np.random.randint(len(shapes.keys()))
        new_obj_color = np.random.randint(len(colors.keys()))
        new_obj = [new_obj_x, new_obj_y, object_width, new_obj_shape, new_obj_color]
        #print new_obj
        if not intersectsOtherObjects(new_obj, objects):
            break
        reject_count += 1
        if reject_count > 500:
            print "ERROR: world is too cluttered, can't fit all desired objects"
            sys.exit()

    return new_obj


def main():
    if len(sys.argv) != 13:
        print "usage error: python writeWorldToYaml.py -o object_color object_shape -l landmark_color landmark_shape -r relation -n numObjects -f output_filename"
        print 'Number of arguments:', len(sys.argv), 'arguments.'
        print 'Argument List:', str(sys.argv)
    landmark_color = sys.argv[sys.argv.index('-l') + 1]
    landmark_shape = sys.argv[sys.argv.index('-l') + 2]
    object_color = sys.argv[sys.argv.index('-o') + 1]
    object_shape = sys.argv[sys.argv.index('-o') + 2]
    relationship = sys.argv[sys.argv.index('-r') + 1]
    num_objects = int(sys.argv[sys.argv.index('-n') + 1])
    filename = sys.argv[sys.argv.index('-f') + 1]

    print "---------------------------"
    print "landmark color:", landmark_color
    print "landmark shape:", landmark_shape
    print "object color:", object_color
    print "object shape:", object_shape
    print "relationship:", relationship
    print "num objects:", num_objects
    print "---------------------------"

    landmark_color_id = colors[landmark_color]
    landmark_shape_id = shapes[landmark_shape]
    object_color_id = colors[object_color]
    object_shape_id = shapes[object_shape]

    #define task_object
    task_object = [object_width, object_shape_id, object_color_id]

    #place landmark
    landmark_x, landmark_y = placeLandmark(relationship)
    landmark_pos = (landmark_x, landmark_y)
    print "landmark_pos", landmark_pos
    landmark_obj = [landmark_x, landmark_y, object_width, landmark_shape_id, landmark_color_id]   #[x, y, diameter, shape, color]
    
    #place target postion to place object
    target_x, target_y = placeTarget(landmark_pos, relationship)
    print "target_pos", (target_x,target_y)
    target_obj = [target_x, target_y, target_width]



    #place other distractor objects in world
    intersection_list = [landmark_obj, target_obj]  #includes target, used for computing intersections
    objects = [landmark_obj]                        #object array for yaml file
    for i in range(num_objects - 1):                #-1 so don't regenerate landmark
        new_obj = generateNewObject(intersection_list)
        intersection_list.append(new_obj)
        objects.append(new_obj)
        #print "generated object"
        #print intersection_list

    #output world into yaml file


    
    #create a dictionary and save to yaml file format
    staging_area = [staging_topleft[0], staging_topleft[1], staging_length]
    table = [table_topleft[0], table_topleft[1], table_width]
    data = {}
    data['width'] = width
    data['height'] = height
    data['objects'] = objects
    data['table'] = table
    data['task_object'] = task_object 
    data['staging_area'] = staging_area
    data['target'] = target_obj
    data['color_map'] = id_to_color
    data['shape_map'] = id_to_shape

    stream = file(filename + '.yaml', 'w')
    yaml.dump(data, stream)    # Write a YAML representation of data to 'document.yaml'.
    print yaml.dump(data)      # Output the document to the screen.

if __name__=="__main__":
    main()

