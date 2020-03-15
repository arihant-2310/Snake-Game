import turtle
import time
import random
import pygame
import itertools
import threading
import sys


#Loading animation 
done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

#long process here
time.sleep(3)
done = True

pygame.mixer.init()

pygame.mixer.music.load("The Perfect Snake Game.mp3")

pygame.mixer.music.play()

delay = 0.1  

# Score
score = 0
high_score = 0

#set up the screen
wn = turtle.Screen()
wn.title("Snake Game By @AJ2310")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0) #keep the animation off on the screen / turns off screen updates

#snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0,0)
head.direction = "stop"

#Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("green")
food.penup()
food.goto(0,100)

#Snake Trap
trap = turtle.Turtle()
trap.speed(0)
trap.shape("triangle")
trap.color("red")
trap.penup()
trap.goto(100,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Score: 0 High Score: 0 level:0", align="center", font=("Courier", 18, "normal"))


#Functions
def go_up():
	if head.direction != "down":
		head.direction = "up"

def go_down():
	if head.direction != "up":
		head.direction = "down"

def go_right():
	if head.direction != "left":
		head.direction = "right"

def go_left():
	if head.direction != "right":
		head.direction = "left"

def move():
	if head.direction == "up":
		y = head.ycor()
		head.sety(y + 20)

	if head.direction == "down":
		y = head.ycor()
		head.sety(y - 20)

	if head.direction == "left":
		x = head.xcor()
		head.setx(x - 20)

	if head.direction == "right":
		x = head.xcor()
		head.setx(x + 20)
#Keyboard Bindings

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_left, "Left")

#for trap array
snakelen = 0
arr = []
start = 1



#main game loop
while True:
	wn.update()
	if(start==1):
		pygame.mixer.music.load("Music.mp3")
		pygame.mixer.music.play()
		start=0

	#Check for collision with the border
	if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
		pygame.mixer.music.load("hit.mp3")
		pygame.mixer.music.play()
		snakelen =0 
		arr= []
		time.sleep(1)
		head.goto(0,0)
		head.direction = "stop"
		
		
		

		#Hide the segments
		for segment in segments:
			segment.goto(1000,1000)

		#Clear the segment list
		segments.clear()

		#Reset The Score
		score =0

		#Reset the delay
		delay = 0.1

		pen.clear()
		pen.write("Score: 0 High Score: 0 level: 0", align="center", font= ("Courier", 18, "normal"))



	#Check with the collison for the food
	if head.distance(food) < 20:
		snakelen=snakelen+1
		print(snakelen)
		#Move the food to random spot
		x = random.randint(-290, 290)
		y = random.randint(-290, 290)
		food.goto(x,y)

		#Move the trap to random spot
		x1 = random.randint(-270, 270)
		y1 = random.randint(-270, 270)
		trap.goto(x1,y1)

		#Add a segment
		new_segment = turtle.Turtle()
		new_segment.speed(0) #animation speed
		new_segment.shape("square")
		new_segment.color("orange")
		new_segment.penup()
		segments.append(new_segment)
		arr.append(new_segment)

		#Shorten the delay
		delay -= 0.001

		#Increase the score
		score += 10

		if score > high_score:
			high_score = score
		pen.clear()
		pen.write("Score: {} High Score: {} level: {}".format(score,high_score,snakelen//2), align="center", font= ("Courier", 18, "normal"))
	#If snake gets trapped
	if (head.distance(trap) < 20):
		if (snakelen>0):
			x = random.randint(-270, 270)
			y = random.randint(-270, 270)
			trap.goto(x,y)
			pops=arr.pop(snakelen-1)
			segments.remove(pops)
			pops.goto(1000,1000)
			snakelen=snakelen-1
			score -= 10
			
		else:
			arr=[]
			snakelen=0
			score =0
			# high_score=0
			pygame.mixer.music.load("red.mp3")
			pygame.mixer.music.play()
			#gameover
			snakelen =0 
			arr= []
			time.sleep(1)
			head.goto(0,0)
			head.direction = "stop"
			pygame.mixer.music.load("Music.mp3")
			pygame.mixer.music.play()

			#Hide the segments
			for segment in segments:
				segment.goto(1000,1000)

			#Clear the segment list
			segments.clear()

			#Reset The Score
			score =0

			#Reset the delay
			delay = 0.1

	pen.clear()
	pen.write("Score: {} High Score: {} level: {}".format(score,high_score,snakelen//2), align="center", font= ("Courier", 18, "normal"))


	#Move the end segments first in reverse order
	for index in range(len(segments)-1, 0, -1):
		x = segments[index-1].xcor()
		y = segments[index-1].ycor()
		segments[index].goto(x,y)

	#Move segments 0 to where the head is
	if len(segments) > 0:
		x = head.xcor()
		y = head.ycor()
		segments[0].goto(x,y)


	move()

	#Check for head collison with the body segments
	for segment in segments:
		if segment.distance(head) < 20:
			time.sleep(1)
			head.goto(0,0)
			head.direction = "stop"
			pygame.mixer.music.load("pause.mp3")
			pygame.mixer.music.play()

			#Hide the segments
			for segment in segments:
				segment.goto(1000,1000)
			#clear the array
			arr =[]
			snakelen = 0

			#Clear the segment list
			segments.clear()

			#Reset The Score
			score =0

			#Reset the delay
			delay = 0.1

			#Update the score display
			pen.clear()
			pen.write("Score: {} High Score: {} level:0".format(score,high_score), align="center", font= ("Courier", 18, "normal"))


	time.sleep(delay)

wn.mainloop() #keep the window on for us