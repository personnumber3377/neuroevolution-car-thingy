
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
        try:
            return 1 / (1 + math.exp(-x * 1.0))
        except:
            return 0

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
    def mutate(self):
    
        #if len(self.dendrons) == 0:
        #    return
        for dendron in self.dendrons:
            randomnumber = random.randint(0,2)
            if randomnumber == 1:
                anotherrandomnumber = random.randint(0, 2)
                if anotherrandomnumber == 0:
                    kerroin = 1
                else:
                    kerroin = -1
                dendron.weight = dendron.weight +(kerroin*(100/random.randint(1,200)))
        


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

    def mutatenetwork(self):
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.mutate();


class Car:
	def __init__(self, angle, x, y, xwidth, ywidth):
		self.nn = Network([20,10,4])
		self.magnitudeofvelocity = 0
		self.x = x
		self.y = y
		self.fitness = 0
		self.angle = angle
		self.terminalstate = False
		self.xwidth = xwidth
		self.ywidth = ywidth
		self.deltax = self.magnitudeofvelocity*math.cos(self.angle/57.2958)
		self.deltay = self.magnitudeofvelocity*math.sin(self.angle/57.2958)
		self.deltax = round(deltax, 2)
		self.deltay = round(deltay, 2)
	def drawcar(self, angle, x, y, xwidth, ywidth):
		import turtle
		"""
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


		"""

		turtle.speed(0)
		turtle.penup()
		turtle.goto(x, y)
		turtle.pendown()
		turtle.dot()
		turtle.penup()
	def checkcollision(self):
		if self.x > -240:
			
			if self.y < 200:
				return True
		if self.x < -400 and self.y > -340:
			return True
		if self.x > 400:
			return True
		if self.y > 400:
			return True
		if self.y < -400:
			return True
		if self.x < -800:
			return True
		return False


"""
was before this

	def checkcollision(self):
		if self.x > -240:
			if self.x < 260:
				if self.y > -100:
					if self.y < 200:
						return True
		if self.x < -400:
			return True
		if self.x > 400:
			return True
		if self.y > 400:
			return True
		if self.y < -400:
			return True
		return False

"""





def checkcollisiongeneric(ax,ay):
	if ax > -240:
		
		if ay < 200:
			return True
	if ax < -400 and ay > -340:
		return True
	if ax > 400:
		return True
	if ay > 400:
		return True
	if ay < -400:
		return True
	if ax < -800:
		return True
	return False

"""
Was before this:

def checkcollisiongeneric(ax,ay):
	if ax > -240:
		if ax < 260:
			if ay > -100:
				if ay < 200:
					return True
	if ax < -400:
		return True
	if ax > 400:
		return True
	if ay > 400:
		return True
	if ay < -400:
		return True
	return False

"""
	

def drawmap():
	paska = turtle.Turtle()

	paska.speed(0)
	
	paska.color("grey","grey")
	
	paska.penup()
	
	paska.setposition(-240,-400)
	paska.pendown()
	paska.left(90)
	paska.forward(540)
	paska.right(90)
	paska.forward(500)
	
	paska.penup()
	paska.goto(-400, 500)
	paska.setheading(-90)
	paska.pendown()
	paska.forward(840)
	paska.right(90)
	paska.forward(300)
	paska.penup()
	paska.left(90)
	paska.penup()
	paska.forward(60)
	paska.pendown()
	paska.left(90)
	paska.forward(600)
	print(paska.pos())
def drawbestcar():
	try:
		bescar.drawcar(bestcar.angle, bestcar.x, bestcar.y, 30, 10)
	except:
		pass

def calculatefitness(carobject):
	fitnessthing = 1/(math.sqrt(((destination[0]-carobject.x)**2)+((destination[1]-carobject.y)**2))) + (1/(juttu+1))*emphasisontime
	return fitnessthing









magnitudeofvelocity = 1
deltax = 1
deltay = 0
angle = 0


brakingconstant = 1
cars = []
terminalstate = False
bestcar = None
numofcars = 1
emphasisontime = 0
destination = [-800, -380]
#for i in range(numofcars):
#	cars.append(Car(0, random.randint(0, 100), random.randint(0,1000), 30, 10))

"""
for paskajuttu in range(0,100):
	print("Generation: "+str(paskajuttu))
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
		cars.append(copy.deepcopy(thingycar))
	
		
	if bestcar == None:
		cars = []
		for i in range(numofcars):
			cars.append(Car(0, 300, 300, 30, 10))
	
	for car in cars:
		car.nn.mutatenetwork()
		car.angle = -180
	for k in range(len(cars)):

		for i in range(len(cars)-1):
			if cars[i].nn == cars[i+1].nn:
				print("fuck this")
	
	for juttu in range(2000):
		
		
		
		
		
		for car in cars:
			'''
			turtle.penup()
			turtle.goto(car.x, car.y)
			turtle.pendown()
			turtle.goto(0, 0)
			'''
			if car.magnitudeofvelocity < 0.1 and juttu > 50:
				cars.remove(car)
				continue
			
			
			car.deltax = car.magnitudeofvelocity*math.cos(car.angle/57.2958)
			car.deltay = car.magnitudeofvelocity*math.sin(car.angle/57.2958)
			
			car.deltax = round(car.deltax, 6)
			
			car.deltay = round(car.deltay, 6)
			if (math.sqrt(((destination[0]-car.x)**2)+((destination[1]-car.y)**2))) < 200:
				car.fitness = calculatefitness(car)
				car.fitness = car.fitness*(1-(juttu/3000))
				car.deltax = 0
				car.deltay = 0
				car.terminalstate = True
				if car.fitness > bestfitness:
					bestcar = copy.deepcopy(car)
				
					bestfitness = bestcar.fitness
				
				cars.remove(car)
				continue
			if car.checkcollision():
				
				
				car.fitness = calculatefitness(car)
				car.fitness = car.fitness*(1-(2999/3000))
				car.deltax = 0
				car.deltay = 0
				car.terminalstate = True
				if car.fitness > bestfitness:
					bestcar = copy.deepcopy(car)
					
					bestfitness = bestcar.fitness
				
				cars.remove(car)
				
				continue
			
			
			
			car.x = car.x + car.deltax
			car.y = car.y + car.deltay
			
			'''
			if keyboard.is_pressed("w"):
				print("you pressed forward")
				car.magnitudeofvelocity = car.magnitudeofvelocity + 0.02
				print(car.magnitudeofvelocity)
			if keyboard.is_pressed("a"):
				car.angle = car.angle + magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("d"):
				car.angle = car.angle - magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("s"):
				car.magnitudeofvelocity = car.magnitudeofvelocity - 0.01
			'''
			
			car.magnitudeofvelocity = car.magnitudeofvelocity - 0.001
			if car.magnitudeofvelocity < 0:
				car.magnitudeofvelocity = 0
			inputti = [0]*20
			anglejuttu = -100+car.angle
			for i in range(20):
				
				for kakka in range(10):
					if checkcollisiongeneric((car.x + 10*kakka*math.cos(anglejuttu/57.2958)), (car.y + 10*kakka*math.sin(anglejuttu/57.2958))):
						inputti[i] = 1
				'''
				turtle.setheading(anglejuttu)
				turtle.penup()
				turtle.goto((car.x + 100*math.cos(anglejuttu/57.2958)), (car.y + 100*math.sin(anglejuttu/57.2958)))

				turtle.pendown()
				turtle.forward(100)
				turtle.penup()
				'''
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
		


		

		

		

	for car in cars:
		car.fitness = calculatefitness(car)
		car.fitness = car.fitness*(1-(2999/3000))
		car.deltax = 0
		car.deltay = 0
		car.terminalstate = True
		if car.fitness > bestfitness:
			bestcar = copy.deepcopy(car)
				
			bestfitness = bestcar.fitness
				
		cars.remove(car)
	
	#for i in range():
		#for i in range(6)
			#print(bestcar.nn.layers[1][0].dendrons[i].weight)

"""
import turtle
bestcarcoordinates = []
turtle.screensize(960, 960)
drawmap()
turtle.tracer(0,0)
for paskajuttu in range(0,11000):
	print(paskajuttu)
	cars = []
	results = []
	terminalstate = False
	bestfitness = 0
	
	thingycar = Car(0, 300, 300, 30, 10)
	
		
		
	for i in range(numofcars):
		cars.append(copy.deepcopy(thingycar))
	
		
	if bestcar == None:
		cars = []
		for i in range(numofcars):
			cars.append(Car(0, 300, 300, 30, 10))
	
	
	
	for juttu in range(3000):
		
		turtle.clear()
		for bestcarcoordinate in bestcarcoordinates:
				print("paskaaaaaaaaaaa")
				
				turtle.goto(bestcarcoordinate[0], bestcarcoordinate[1])
				turtle.pendown()
				turtle.dot()
				turtle.penup()

		
		
		
		
		for car in cars:
			"""
			turtle.penup()
			turtle.goto(car.x, car.y)
			turtle.pendown()
			turtle.goto(0, 0)
			"""
			
			
			
			car.deltax = car.magnitudeofvelocity*math.cos(car.angle/57.2958)
			car.deltay = car.magnitudeofvelocity*math.sin(car.angle/57.2958)
			
			car.deltax = round(car.deltax, 6)
			
			car.deltay = round(car.deltay, 6)
			if (math.sqrt(((destination[0]-car.x)**2)+((destination[1]-car.y)**2))) < 200:
				car.fitness = calculatefitness(car)
				car.fitness = car.fitness*(1-(juttu/3000))
				car.deltax = 0
				car.deltay = 0
				car.terminalstate = True
				print(juttu)
				if car.fitness > bestfitness:
					bestcar = copy.deepcopy(car)
					#bestcarcoordinates.append([bestcar.x, bestcar.y])
				
					bestfitness = bestcar.fitness
				
				cars.remove(car)
				continue
			if car.checkcollision():
				
				
				car.fitness = calculatefitness(car)
				car.fitness = car.fitness*(1-(2999/3000))
				car.deltax = 0
				car.deltay = 0
				car.terminalstate = True
				if car.fitness > bestfitness:
					bestcar = copy.deepcopy(car)
					#bestcarcoordinates.append([bestcar.x, bestcar.y])
					bestfitness = bestcar.fitness
				
				
				
				continue
			
			
			
			car.x = car.x + car.deltax
			car.y = car.y + car.deltay
			car.drawcar(car.angle, car.x, car.y, 30, 10)
			

			
			if keyboard.is_pressed("w"):
				
				car.magnitudeofvelocity = car.magnitudeofvelocity + 0.02
				
			if keyboard.is_pressed("a"):
				car.angle = car.angle + magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("d"):
				car.angle = car.angle - magnitudeofvelocity*brakingconstant
			if keyboard.is_pressed("s"):
				car.magnitudeofvelocity = car.magnitudeofvelocity - 0.01
			
			
			car.magnitudeofvelocity = car.magnitudeofvelocity - 0.001
			if car.magnitudeofvelocity < 0:
				car.magnitudeofvelocity = 0
			inputti = [0]*20
			anglejuttu = -100+car.angle
			for i in range(20):
				
				for kakka in range(10):
					if checkcollisiongeneric((car.x + 10*kakka*math.cos(anglejuttu/57.2958)), (car.y + 10*kakka*math.sin(anglejuttu/57.2958))):
						inputti[i] = 1
				"""
				turtle.setheading(anglejuttu)
				turtle.penup()
				turtle.goto((car.x + 100*math.cos(anglejuttu/57.2958)), (car.y + 100*math.sin(anglejuttu/57.2958)))

				turtle.pendown()
				turtle.forward(100)
				turtle.penup()
				"""
				anglejuttu = anglejuttu + 10
			drawbestcar()
			#car.nn.setInput(inputti)
			#car.nn.feedForword()
			#results = car.nn.getResults()
			"""
			if results[0] > 0.5:
				car.magnitudeofvelocity = car.magnitudeofvelocity + 0.01
			if results[1] > 0.5:
				car.magnitudeofvelocity = car.magnitudeofvelocity - 0.01
			if results[2] > 0.5:
				car.angle = car.angle + magnitudeofvelocity*brakingconstant
				
			if results[3] > 0.5:
				car.angle = car.angle - magnitudeofvelocity*brakingconstant
			"""
		paskaa = True
		for i in range(len(cars)):
			if cars[i].terminalstate == True:
				paskaa = True
			else:
				paskaa = False
				break
		drawbestcar()


		

		

		turtle.update()

	for car in cars:
		car.fitness = calculatefitness(car)
		car.fitness = car.fitness*(1-(2999/3000))
		car.deltax = 0
		car.deltay = 0
		car.terminalstate = True
		if car.fitness > bestfitness:
			bestcar = copy.deepcopy(car)
			#bestcarcoordinates.append([bestcar.x, bestcar.y])
			bestfitness = bestcar.fitness
				
		cars.remove(car)
	#bestcarcoordinates.append([bestcar.x, bestcar.y]) 
	
	#for i in range():
		#for i in range(6)
			#print(bestcar.nn.layers[1][0].dendrons[i].weight)
	
