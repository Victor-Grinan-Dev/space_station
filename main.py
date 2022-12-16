import turtle
import math
import random

PI = 3.14159
HEIGHT = 600
WIDTH = 600

win = turtle.Screen()
win.setup(height=HEIGHT, width=WIDTH)
win.title("space ship defender")
win.bgcolor("black")

player_vertices = ((0, 15), (-15, 0), (-18, 5), (-18, -5), (0, 0), (18, -5), (18, 5), (15, 0))
win.register_shape("player", player_vertices)


class Sprite(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()


level = 1
asteroid_speed = 1

player = Sprite()
player.color("white")
player.shape("player")
player.score = 0

missile = Sprite()
missile.hideturtle()
missile.color("red")
missile.shape("arrow")
missile.speed = 15
missile.state = "ready"

pen = Sprite()
pen.hideturtle()
pen.color("white")


def actualize_score():
    pen.clear()
    pen.goto(-200, 200)
    pen.write(f"Score: {player.score} level: {level}", True, align="center", font=("Arial", 14, "normal"))


actualize_score()
asteroids = []


def create_asteroids(lvl):
    print(f"creating {lvl} asteroids")
    for _ in range(lvl):
        asteroid_ = Sprite()
        asteroid_.hideturtle()
        asteroid_.color("brown")
        asteroid_.shape("circle")
        heading_ = random.randint(0, 360)
        distance_ = random.randint(450, 600)
        asteroid_.setheading(heading_)
        asteroid_.fd(distance_)
        asteroid_.setheading(asteroid_.towards(player.pos()))
        # asteroid_.speed += 1
        asteroid_.showturtle()
        asteroids.append(asteroid_)


def get_heading_to(x2, y2):
    """
    calculates the heading in radiants, convert radiants to degrees
    :param x2: coord from your position to:
    :param y2: coord from your position to:
    :return: angle degrees, float
    """
    radiants = math.atan2(-x2, -y2)
    heading = (radiants + PI) * 360 / (2 * PI)  # returning angles
    return heading


def mouse_move(event):
    x, y = event.x, event.y
    heading_ = get_heading_to(x, y)
    player.setheading(heading_)


def rotate_left():
    player.lt(15)


def rotate_right():
    player.rt(15)


def fire_missile():
    if missile.state == "ready":
        missile.goto(0, 0)
        missile.setheading(player.heading())
        missile.showturtle()
        missile.state = "fire"


win.listen()
win.onkey(rotate_left, "Left")  # notice upper L
win.onkey(rotate_right, "Right")  # notice upper R
win.onkey(fire_missile, "space")  # notice lower s

create_asteroids(level)
# canvas = win.getcanvas()
# canvas.bind("<motion>", mouse_move)
# # win.onclick(mouse_move)

while True:
    win.update()
    player.goto(0, 0)

    for asteroid in asteroids:
        asteroid.fd(asteroid_speed)
        # check collation:
        # asteroid and missile
        if asteroid.distance(missile) < 20:
            # reset asteroid
            asteroids.remove(asteroid)
            asteroid.hideturtle()

            # reset missile
            missile.hideturtle()
            missile.state = "ready"

            # score handling
            player.score += 1
            actualize_score()

        # check collation:
        # asteroid and player
        if asteroid.distance(player) < 10:
            # reset asteroid
            asteroids.remove(asteroid)
            asteroid.hideturtle()
            missile.hideturtle()
            create_asteroids(1)  # create one asteroid so you dont level up?

    if missile.state == "fire":
        missile.fd(missile.speed)
    if missile.xcor() > 400 or missile.xcor() < -400 or missile.ycor() > 400 or missile.ycor() < -400:
        missile.state = "ready"

    if len(asteroids) == 0:
        level += 1
        create_asteroids(level)
        asteroid_speed += 1

# win.exitonclick()
