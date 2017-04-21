'''
Created on Apr 20, 2017

@author: dsbrown
'''

import yaml

shapes = {'circle':0,'square':1,'triangle':2,'star':3,'diamond':4}
colors = {'blue':0, 'red':1,'green':2,'purple':3,'yellow':4,'orange':5}
id_to_shape = {item[1]:item[0] for item in shapes.items()}
id_to_color = {item[1]:item[0] for item in colors.items()}



""" pure LfD idea:
    (1) First take every demonstration for a specific task and compute the intersection over featurized objects to see what remains constant.
    This sees if the same exact feature is present over all demonstrations.
    
    NOTE: maybe we should just look over each feature so maybe we see there is always a circle or even always two shapes of different colors, etc"
        This really blows up since anything could be possible. Ideally we want an LfD method that starts from simple and moves to complex. 
        First look at singletons then at pairs within objects, ... we could also look at colors aligned with positions, etc. How do you deal with this?
        Need some sort of prior.

"""
def findInvariantObjects(yaml_filenames):
    
    #initialize object intersection to all objects in first filename
    seed_file = yaml_filenames[0]
    invariant_objects = extractObjectFeatures(seed_file)
    #print "initial set of objects: ", invariant_objects
    converged = False  #flag for when a full pass through data results in no reduction in intersection set
    while not converged:
        converged = True
        for filename in yaml_filenames:
            #print filename
            obj_features = extractObjectFeatures(filename) #TODO return a set of object feature tuples
            #print "new objects: ", obj_features
            num_objects_before = len(invariant_objects) #count number in set before intersection
            invariant_objects.intersection_update(obj_features)
            #print "after intersection"
            #print invariant_objects
            num_objects_after = len(invariant_objects) #count number in set after intersection
            
            if num_objects_after < num_objects_before:
                converged = False
    return invariant_objects
        
    
""" extract the shape and color features for each object, if there is more than one object of a type it only returns a single object
    TODO: It seems like we should have a unique identifier for each object even if they look identical but have different position etc.
"""
def extractObjectFeatures(yaml_filename):
    #how to open a yaml file
    with open(yaml_filename, 'r') as stream:
        try:
            world = yaml.load(stream)
            #print world
        except yaml.YAMLError as exc:
            print exc 
            
    object_features = set()
    for obj in world['objects']:
        object_features.add((obj[3], obj[4]))
    
    return object_features    
        
        
#Testing code
scenarios = ['red_triangle_right_green_circle_', 'green_square_left_blue_star_', 'blue_circle_above_red_square_']
#scenarios = ['red_triangle_right_green_circle_']

for s in scenarios:
    filenames = []
    for i in range(1,11):
        filenames.append("/home/daniel/Code/LfD-NLP/pilot_data/" + s + str(i) + ".yaml")
    
    print s
    invariant_objs = findInvariantObjects(filenames)
    print "invariant objects: "
    for obj in invariant_objs:
        print "...", id_to_color[obj[1]], id_to_shape[obj[0]] 
    
