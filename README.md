# LfD-NLP
Using NLP to improve LfD

To run the yaml files you need python-yaml
```{r, engine='sh', count_lines}
sudo apt-get install python-yaml
```
To generate yaml files use the writeWorldToYaml.py file in the yaml_code directory

usage: 
```{r, engine='sh', count_lines}
python writeWorldToYaml.py -o object_color object_shape -l landmark_color landmark_shape -r relation -n numObjects -f output_filename
```
Here are the possible arguments

possible shape names: circle, square, triangle, star, diamond

possible colors: blue, red, green, purple, yellow, orange

possible relations: left, right, up, down, on, near, far


For example, to generate a world where the goal is to place a blue square to the left of a red circle with two distractors you would use the following command:
```{r, engine='sh', count_lines}
python writeWorldToYaml.py -o blue square -l red circle -r left -n 3 -f leftPlacementTest
```


Ideas / Thoughts:

Maybe have a free-for-all round at end of user demonstrations where we have human teach robot any task they want through demonstration and words. At worst, we throw this data away, at best we get some interesting spatial relationships that we didn't hand code into the experiments. This also gives us something more realistic since the human starts with a goal and then gives demonstrations, rather than being trained along the way. We could just give them a set of fixed objects that are randomly placed each time, or have them move the objects to set up each demonstration. Then ask them to give X demos of the task they want the robot to learn and a concise description of the task.
