import math
import random
import turtle
import os

# set up screen

wn = turtle.Screen()
wn.bgcolor("dark blue")
wn.title("Turtle Defender")
wn.bgpic("turtle_fighter_background.gif")

# register the shapes


# draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("light blue")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):  # creates a box for the border
    border_pen.fd(600)  # moves line x amount of pixels in one direction
    border_pen.lt(90)  # turns the pen to go in a different direction as it is drawing the square
border_pen.hideturtle()

# set the score to 0

score = 0

# draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# create player turtle
player = turtle.Turtle()
player.color("green")
player.shape("circle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player_speed = 15

# create enemy
# initializing enemy object within the GUI
enemy = turtle.Turtle()
enemy.color("red")
enemy.shape("circle")
enemy.penup()
enemy.speed(0)
enemy.setposition(-200, 250)

enemy_speed = 2

# choose the number of enemies
number_of_enemies = 5

# create an empty list of enemies
enemies = []

# add enemies to the list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemy_speed = 2

# create the player's weapons

weapon = turtle.Turtle()
weapon.color("light blue")
weapon.shape("triangle")
weapon.penup()  # prevents weapons from drawing a line as it moves through the GUI
weapon.speed(0)
weapon.setheading(90)
weapon.shapesize(0.5, 0.5)
weapon.hideturtle()

weapon_speed = 20

# initializing state of the weapon
# ready to fire
# firing
weapon_state = "ready"


# move the player to the left and right
def move_left():
    """
    Checking boundaries for the player so they
    do not move off of the board when moving to the left.
    Keeps the player inside the world of the game.
    """
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = - 280
    player.setx(x)


def move_right():
    """
    Checking boundaries for the player so they
    do not move off of the board when going to the right.
    Keeps the player inside the world of the game.
    """
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def fire_weapon():
    # set weapon state as a global if it needs to be changed
    global weapon_state  # any change within this function will be reflected in the global scope
    if weapon_state == "ready":
        weapon_state = "fire"
        # move the weapon to be just above the player
        x = player.xcor()
        y = player.ycor() + 10
        weapon.setposition(x, y)
        weapon.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 18:
        return True
    else:
        return False


# create keyboard bindings
# initializing connection between keyboard commands to player movement in the GUI
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_weapon, "space")

# primary game loop
while True:  # while the game is running, or while the player is actually playing the game

    for enemy in enemies:
        # move the enemy
        x = enemy.xcor()  # initializing the x coordinates of the enemy AI
        x += enemy_speed  # setting the enemy speed
        enemy.setx(x)  # setting the x coordinates to the x values on the GUI

        # need the enemy to reverse once it touches either edge of the board
        if enemy.xcor() > 280:
            for e in enemies:
                y = e.ycor()  # initializing the y coordinates
                y -= 40  # every time the enemy hits the boarder, the enemy will drop down 40 pixels, and hence will get
                # closer to the player
                e.sety(y)
            # change the enemy's direction
            enemy_speed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()  # initializing the y coordinates
                y -= 40  # every time the enemy hits the boarder, the enemy will drop down 40 pixels, and hence will get
                # closer to the player
                e.sety(y)
            # change the enemy's direction
            enemy_speed *= -1

        # checking for collision between the weapon and the enemy
        if isCollision(weapon, enemy):
            # reset weapon
            weapon.hideturtle()
            weapon_state = "ready"
            weapon.setposition(0, -400)  # moves weapon off the screen

            # reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

            # update score
            score += 10
            score_string = "Score: %s" % score
            # on type of string when using python's string formatting capabilities. More specifically, %s converts a
            # specified value to a string using the str() function.
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        # checking for collision between the player and the enemy
        if isCollision(player, enemy):
            # reset weapon
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    #  move the weapon
    if weapon_state == "fire":
        y = weapon.ycor()
        y += weapon_speed
        weapon.sety(y)

    # checking to see if the weapon has reached the top
    if weapon.ycor() > 275:
        weapon.hideturtle()
        weapon_state = "ready"

delay = raw_input("Press enter to finish")
