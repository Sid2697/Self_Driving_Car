# importing the libraries
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# importing the Kivy packages
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

# Importing our car's brain
from ai import Dqn

# This line helps from stopping creation of a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Introducing last_x and last_y, used to keep the last point in memory when we draw tha same line
last_x = 0
last_y = 0
n_points = 0
length = 0

# Getting our AI, which we call 'brain' and that contains our neural network that represent
brain = Dqn(5, 3, 0.9)
action2rotation = [0, 20, -20]
last_reward = 0
scores = []

# initializing the map
first_update = True


def init():
    global sand
    global goal_x  # x-coordinate of the goal
    global goal_y  # y-coordinate of the goal
    global first_update
    sand = np.zeros((longueur, largeur))
    goal_x = 20
    goal_y = largeur - 20
    first_update = False


# Initialize the last distance
last_distance = 0

# Creating the car class


class Car(Widget):

    angle = NumericProperty(0)  # angle of the car
    rotation = NumericProperty(0)  # last rotation of the car
    velocity_x = NumericProperty(0)  # x-coordinate of velocity vector
    velocity_y = NumericProperty(0)  # y-coordinate of velocity vector
    velocity = ReferenceListProperty(velocity_x, velocity_y)  # velocity vector
    sensor1_x = NumericProperty(0)  # x-coordinate of the first sensor
    sensor1_y = NumericProperty(0)  # y-coordinate of the first sensor
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)  # first sensor vector
    sensor2_x = NumericProperty(0)  # x-coordinate of second sensor
    sensor2_y = NumericProperty(0)  # y-coordinate of second sensor
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)  # second sensor vector
    sensor3_x = NumericProperty(0)  # x-coordinate of third sensor
    sensor3_y = NumericProperty(0)  # y-coordinate of third sensor
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)  # third sensor vector
    signal1 = NumericProperty(0)  # signal recived by sensor 1
    signal2 = NumericProperty(0)  # signal recived by sensor 2
    signal3 = NumericProperty(0)  # signal recived by sensor 3

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos  # updating the position of the car according to its last position and velocity
        self.rotation = rotation  # rotation of the car
        self.angle = self.angle + self.rotation  # updating the angle
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos  # updating position of sensor 1
        self.sensor2 = Vector(30, 0).rotate((self.angle + 30) % 360) + self.pos  # updating the position of sensor 2
        self.sensor3 = Vector(30, 0).rotate((self.angle - 30) % 360) + self.pos  # updating the position of sensor 3
        self.signal1 = int(np.sum(sand[int(self.sensor1_x) - 10:int(self.sensor1_x + 10), int(self.sensor1_y) - 10:int(self.sensor1_y) + 10])) / 400.  # getting signal received by sensor 1
        self.signal2 = int(np.sum(sand[int(self.sensor2_x) - 10:int(self.sensor2_x + 10), int(self.sensor2_y) - 10:int(self.sensor2_y) + 10])) / 400.  # getting signal received by sensor 2
        self.signal3 = int(np.sum(sand[int(self.sensor3_x) - 10:int(self.sensor3_x + 10), int(self.sensor3_y) - 10:int(self.sensor3_y) + 10])) / 400.  # getting signal received by sensor 3
        if self.sensor1_x > longueur - 10 or self.sensor1_x < 10 or self.sensor1_y > largeur - 10 or self.sensor1_y < 10:  # if sensor 2 is out of the map
            self.signal1 = 1.  # sensor 1 detects full sand
        if self.sensor2_x > longueur - 10 or self.sensor2_x < 10 or self.sensor2_y > largeur - 10 or self.sensor2_y < 10:  # if sensor 2 is out of the map
            self.signal2 = 1.  # sensor 2 detects full sand
        if self.sensor3_x > longueur - 10 or self.sensor3_x < 10 or self.sensor3_y > largeur - 10 or self.sensor3_y < 10:  # if sensor 2 is out of the map
            self.signal3 = 1.  # sensor 3 detects full sand


class Ball1(Widget):
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass


class Game(Widget):

    car = ObjectProperty(None)  # getting car object from kivy file
    ball1 = ObjectProperty(None)  # getting the sensor 1 object
    ball2 = ObjectProperty(None)  # getting the sensor 2 object
    ball3 = ObjectProperty(None)  # getting the sensor 3 object

    def serve_car(self):  # starting the car when we launch tha application
        self.car.center = self.center  # the car will start at the center of the map
        self.car.velocity = Vector(6, 0)  # the car will start to go horizontally to the right with a speed of 6

    def update(self, dt):

        # specifying the global variables
        global brain
        global last_reward
        global scores
        global last_distance
        global goal_x
        global goal_y
        global longueur
        global largeur

        longueur = self.width  # widht of the map
        largeur = self.height  # height of the map
        if first_update:  # trick to initialize map only once
            init()

        xx = goal_x - self.car.x  # difference of x-coordinates between the goal and the car
        yy = goal_y - self.car.y  # difference of y-coordinates between the goal and the car
        orientation = Vector(*self.car.velocity).angle((xx, yy)) / 180.  # direction of the car wrt. goal
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]  # our input state vector, composed of the three signals received by the three sensors, plus the orientation and  -orientation
        action = brain.update(last_reward, last_signal)  # playing the action from our AI
        scores.append(brain.score())  # appending the score
        rotation = action2rotation[action]  # converting the action played (0, 1 or 2) into the rotation angle (0, 20 or -20)
        self.car.move(rotation)  # moving the car according to this last rotation angle
        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)  # getting the distance between the car and the goal right after the car moved
        self.ball1.pos = self.car.sensor1  # updating the position of the first sensor (ball1)
        self.ball2.pos = self.car.sensor2  # updating the position of the first sensor (ball1)
        self.ball3.pos = self.car.sensor3  # updating the position of the first sensor (ball1)

        if sand[int(self.car.x), int(self.car.y)] > 0:  # if car is on the sand
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)  # it is slowed down
            last_reward = -1  # and reward = -1
        else:
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)  # it goes to normal speed
            last_reward = -0.2
            if distance < last_distance:
                # however if it is getting close to the goal
                last_reward = 0.1

        if self.car.x < 10:  # if the car is in the left of the frame
            self.car.x = 10  # it is not slowed down
            last_reward = -1  # but if gets bad reward -1
        if self.car.x > self.width - 10:  # if the car is in the right of the frame
            self.car.x = self.width - 10  # it is not slowed down
            last_reward = -1  # but if gets bad reward -1

        if self.car.y < 10:  # if the car is in the left of the frame
            self.car.y = 10  # it is not slowed down
            last_reward = -1  # but if gets bad reward -1

        if self.car.y > self.height - 10:  # if the car is in the right of the frame
            self.car.y = self.height - 10  # it is not slowed down
            last_reward = -1  # but if gets bad reward -1

        if distance < 100:  # when the car reaches its goal
            goal_x = self.width - goal_x  # the goal the bottom right corner of the map
            goal_y = self.height - goal_y  # the goal becomes the bottom right corner of the map

        # Updating the last distance from the car to the goal
        last_distance = distance


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):  # putting some sand when we do a left click
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            sand[int(touch.x), int(touch.y)] = 1

    def on_touch_move(self, touch):  # putting some sand whan we move the mouse while pressing left
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            n_points += 1.
            density = n_points / (length)
            touch.ud['line'].width = int(20 * density + 1)
            sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            last_x = x
            last_y = y


# Adding API Buttons

class CarApp(App):

    def build(self):
        parent = Game()
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0 / 60.0)
        self.painter = MyPaintWidget()
        clearbtn = Button(text='clear')
        savebtn = Button(text='save', pos=(parent.width, 0))
        loadbtn = Button(text='load', pos=(2 * parent.width, 0))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        return parent

    def clear_canvas(self, obj):
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur, largeur))

    def save(self, obj):
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        brain.load()


# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
