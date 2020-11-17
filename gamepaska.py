import turtle
import time
import math
import keyboard
import random
import numpy as np
import copy

class Connection:
    def __init__(self, connectedNeuron):
        self.connectedNeuron = connectedNeuron
        self.weight = np.random.normal()
        self.dWeight = 0.0


class Neuron:
    eta = 0.001
    alpha = 0.01

    def __init__(self, layer):
        self.dendrons = []
        self.error = 0.0
        self.gradient = 0.0
        self.output = 0.0
        if layer is None:
            pass
        else:
            for neuron in layer:
                con = Connection(neuron)
                self.dendrons.append(con)

    def addError(self, err):
        self.error = self.error + err

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x * 1.0))

    def dSigmoid(self, x):
        return x * (1.0 - x)

    def setError(self, err):
        self.error = err

    def setOutput(self, output):
        self.output = output

    def getOutput(self):
        return self.output

    def feedForword(self):
        sumOutput = 0
        if len(self.dendrons) == 0:
            return
        for dendron in self.dendrons:
            sumOutput = sumOutput + dendron.connectedNeuron.getOutput() * dendron.weight
        self.output = self.sigmoid(sumOutput)

    def backPropagate(self):
        self.gradient = self.error * self.dSigmoid(self.output);
        
        for dendron in self.dendrons:
            dendron.dWeight = Neuron.eta * (
            self.gradient * dendron.connectedNeuron.output) + self.alpha * dendron.dWeight;
            dendron.weight = dendron.weight + dendron.dWeight;
            dendron.connectedNeuron.addError(dendron.weight * self.gradient);
        self.error = 0;


class Network:
    def __init__(self, topology):
        self.layers = []
        for numNeuron in topology:
            layer = []
            for i in range(numNeuron):
                if (len(self.layers) == 0):
                    layer.append(Neuron(None))
                else:
                    layer.append(Neuron(self.layers[-1]))
            layer.append(Neuron(None))
            layer[-1].setOutput(1)
            self.layers.append(layer)

    def setInput(self, inputs):
        for i in range(len(inputs)):
            self.layers[0][i].setOutput(inputs[i])

    def feedForword(self):
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.feedForword();

    def backPropagate(self, target):
        for i in range(len(target)):
            self.layers[-1][i].setError(self.layers[-1][i].getOutput()- target[i])
        for layer in self.layers[::-1]:
            for neuron in layer:
                neuron.backPropagate()

    def getError(self, target):
        err = 0
        for i in range(len(target)):
            e = (target[i] - self.layers[-1][i].getOutput())
            err = err + e ** 2
        err = err / len(target)
        err = math.sqrt(err)
        return err

    def getResults(self):
        output = []
        for neuron in self.layers[-1]:
            output.append(neuron.getOutput())
        output.pop()
        return output

    def getThResults(self):
        output = []
        for neuron in self.layers[-1]:
            o = neuron.getOutput()
            print(o)
            if (o > 0.5):
                o = 1
            else:
                o = 0
            output.append(o)
        output.pop()
        return output


class Car:
	def __init__(self, angle, x, y, xwidth, ywidth):
		self.nn = Network([5,4,4])
		self.magnitudeofvelocity = 0
		self.x = x
		self.y = y
		self.fitness = 0
		self.angle = angle
		self.terminalstate = False
		self.xwidth = xwidth
		self.ywidth = ywidth
		self.deltax = magnitudeofvelocity*math.cos(self.angle/57.2958)
		self.deltay = magnitudeofvelocity*math.sin(self.angle/57.2958)
		self.deltax = round(deltax, 2)
		self.deltay = round(deltay, 2)
	def drawcar(self, angle, x, y, xwidth, ywidth):
		paskat = turtle.pos()
	
		turtle.speed(0)
		turtle.penup()
		turtle.goto(x,y)
		turtle.pendown()
		turtle.speed(0)
		turtle.setheading(angle)
	
	
		turtle.forward(xwidth)
		turtle.left(90)
		turtle.forward(ywidth)
		turtle.left(90)
		turtle.forward(xwidth)
		turtle.left(90)
		turtle.forward(ywidth)
		turtle.left(90)
		turtle.penup()
		turtle.goto(paskat)
	def checkcollision(self):
		if self.x > -240:
			if self.x < 260:
				if self.y > -100:
					if self.y < 200:
						return True
		if self.x < -480:
			return True
		if self.x > 480:
			return True
		if self.y > 480:
			return True
		if self.y < -480:
			return True
		return False

def checkcollisiongeneric(ax,ay):
	if ax > -240:
		if ax < 260:
			if ay > -100:
				if ay < 200:
					return True
	if ax < -480:
		return True
	if ax > 480:
		return True
	if ay > 480:
		return True
	if ay < -480:
		return True
	return False
	

def drawmap():
	paska = turtle.Turtle()

	paska.speed(0)
	
	paska.color("grey","grey")
	
	paska.penup()
	
	paska.setposition(-240,-100)
	paska.begin_fill()
	paska.pendown()
	paska.forward(500)
	paska.left(90)
	paska.forward(300)
	paska.left(90)
	paska.forward(500)
	paska.left(90)
	paska.forward(300)


turtle.screensize(960, 960)



drawmap()


magnitudeofvelocity = 1
deltax = 1
deltay = 0
angle = 0
turtle.tracer(0,0)
drawmap()
brakingconstant = 0.2
cars = []
terminalstate = False
bestcar = None
numofcars = 100
for i in range(numofcars):
	cars.append(Car(0, random.randint(0, 100), random.randint(0,1000), 30, 10))
while True:
	cars = []
	results = []
	terminalstate = False
	bestfitness = 0
	if bestcar != None:
		bestcar.x = 300
		bestcar.y = 300
		bestcar.deltax = 0
		bestcar.deltay = 0
		bestcar.magnitudeofvelocity = 0
	thingycar = Car(0, 300, 300, 30, 10)
	if bestcar:
		thingycar.nn = bestcar.nn
		
	for i in range(numofcars):
		cars.append(thingycar)
	for car in cars:
		
	if bestcar == None:
		cars = []
		for i in range(numofcars):
			cars.append(Car(0, 300, 300, 30, 10))

	for juttu in range(1000):
		print(juttu)
		turtle.clear()
		
		
		
		
		for car in cars:

			car.deltax = car.magnitudeofvelocity*math.cos(car.angle/57.2958)
			car.deltay = car.magnitudeofvelocity*math.sin(car.angle/57.2958)
			
			car.deltax = round(car.deltax, 6)
			
			car.deltay = round(car.deltay, 6)

			if car.checkcollision():
				car.deltax = 0
				car.deltay = 0
				car.terminalstate = True
				if car.fitness > bestfitness:
					bestcar = copy.deepcopy(car)
					bestfitness = bestcar.fitness
					print(bestcar)
				cars.remove(car)
				continue
			car.fitness += car.deltax + car.deltay
			
			
			car.x = car.x + car.deltax
			car.y = car.y + car.deltay
			car.drawcar(car.angle, car.x, car.y, 30, 10)
			
			if keyboard.is_pressed("w"):
				
				car.magnitudeofvelocity = car.magnitudeofvelocity + 0.01
			if keyboard.is_pressed("a"):
				car.angle = car.angle + magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("d"):
				car.angle = car.angle - magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("s"):
				car.magnitudeofvelocity = car.magnitudeofvelocity - 0.01
			
			car.magnitudeofvelocity = car.magnitudeofvelocity - 0.001
			if car.magnitudeofvelocity < 0:
				car.magnitudeofvelocity = 0
			inputti = [0,0,0,0,0]
			anglejuttu = -20+car.angle
			for i in range(5):
				if checkcollisiongeneric((car.x + 40*math.cos(anglejuttu/57.2958)), (car.y + 40*math.sin(anglejuttu/57.2958))):
					
					inputti[i] = 1
				else:
					inputti[i] = 0
				turtle.setheading(anglejuttu)
				turtle.penup()
				turtle.goto((car.x + 40*math.cos(anglejuttu/57.2958)), (car.y + 40*math.sin(anglejuttu/57.2958)))

				turtle.pendown()
				turtle.forward(100)
				turtle.penup()
				anglejuttu = anglejuttu + 10
			car.nn.setInput(inputti)
			car.nn.feedForword()
			results = car.nn.getResults()
			if results[0] > 0.5:
				car.magnitudeofvelocity = car.magnitudeofvelocity + 0.01
			if results[1] > 0.5:
				car.magnitudeofvelocity = car.magnitudeofvelocity - 0.01
			if results[2] > 0.5:
				car.angle = car.angle + magnitudeofvelocity*brakingconstant
			if results[3] > 0.5:
				car.angle = car.angle - magnitudeofvelocity*brakingconstant
		paskaa = True
		for i in range(len(cars)):
			if cars[i].terminalstate == True:
				paskaa = True
			else:
				paskaa = False
				break


		

		

		turtle.update()
	if bestcar == None:
		continue

	