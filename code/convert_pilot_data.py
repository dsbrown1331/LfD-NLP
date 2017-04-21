'''
Created on Apr 20, 2017

@author: dsbrown
'''

import yaml

#hard coded ids from shapes and colors to integers
shapes = {'circle':0,'square':1,'triangle':2,'star':3,'diamond':4}
colors = {'blue':0, 'red':1,'green':2,'purple':3,'yellow':4,'orange':5}

def main():
    files = ['red_triangle_right_green_circle_', 'green_square_left_blue_star_', 'blue_circle_above_red_square_']
    for f in files:
        for i in range(1,11):
            filename = "../pilot_data_raw/" + f + str(i) + ".yaml"
            print filename
            #filename = "/home/dsbrown/Code/LfD-NLP/yaml_code/downTest.yaml"
            
            #how to open a yaml file
            with open(filename, 'r') as stream:
                try:
                    world = yaml.load(stream)
                    print world
                except yaml.YAMLError as exc:
                    print exc 
            
            #need to parse each object and replace shape with id and color with id
            id_objects = []
            for ob in world['objects']:
                print ob[4]
                print colors[ob[4]]
                id_objects.append([ob[0], ob[1], ob[2], shapes[ob[3]], colors[ob[4]]])
            
            #need to parse task_object and do the same thing
            id_task_object = world['task_object']
            id_task_object[1] = shapes[id_task_object[1]]
            id_task_object[2] = colors[id_task_object[2]]
            
            
            
            data = {}
            data['objects'] = id_objects
            data['task_object'] = id_task_object 
            data['target'] = world['target']
            
        
            stream = file("../pilot_data/" +  f + str(i) +  '.yaml', 'w')
            yaml.dump(data, stream)    # Write a YAML representation of data to 'document.yaml'.
            print yaml.dump(data)      # Output the document to the screen.


if __name__ == '__main__':
    main()
