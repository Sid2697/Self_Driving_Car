# Self_Driving_Car
A demonstration of Reinforcement Learning applied to a car.
## Description
This project was made while learning about *Deep Q Learning* which is a widely used technique for *Reinforcement Learning*.<br>
The idea behind this is simple, the car has 3 sensors which measure the density of the sand and also the edges of the environment.<br>
This input is then sent to a simple feed-forward Neural Network which takes the decision in which direction the car must move.<br>
## Objective
The objective for the car is to make to and fro trips from top left corner of the screen to the bottom right corner of the screen.<br>
The closer it gets to the target corner the more positive rewards it gets, in the other case it gets negative rewards. Which in turns help in improving the weights of the Neural Network.
## Preview
[![IMAGE ALT TEXT](https://github.com/Sid2697/Self_Driving_Car/blob/master/Thumbnail.png)](https://www.youtube.com/watch?v=ZRDK-vmoAog)
## Requirements
- NumPy
- kivy
- Pytorch<br>

You can install all the required libraries by running the following command
##### pip install requirements.txt
## Functionalities
1. Demonstrate the working of Deep Q-Learning.
2. Neural Network working as the brain of the car.
3. Kivy for creating all the graphics.
## Procedure
1. Go through the code once, and then run the file `map_Sid.py`.
2. When the car start to run click on the screen to draw the sand. <br>
## Credits
This project was inspired by [Hadelin de Ponteves](https://www.linkedin.com/in/hadelin-de-ponteves-1425ba5b/) and his team via the course [Artificial Intelligence A-Z](https://www.udemy.com/artificial-intelligence-az/).
