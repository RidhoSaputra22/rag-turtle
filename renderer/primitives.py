import math

def goto(t, x, y):

    t.penup()
    
    t.goto(
        x,
        y
    )

    t.pendown()


def rectangle(
    t,
    x,
    y,
    width,
    height,
    fill="white",
    outline=None
):

    left = (
        x - width / 2
    )

    bottom = (
        y - height / 2
    )

    goto(
        t,
        left,
        bottom
    )

    t.setheading(0)

    t.color(outline or fill, fill)

    t.begin_fill()


    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    
    t.end_fill()

def polygon(
    t, 
    points,
    fill="white",
    outline=None
):
    if not points:
        return 
    
    t.color(outline or fill, fill)

    goto(
        t,
        points[0][0],
        points[0][1]
    )

    t.begin_fill()

    for x, y in points[1:]:

        t.goto(
            x,
            y
        )

    t.goto(
        points[0][0],
        points[0][1]
    )

    t.end_fill()


def circle(
    t,
    x,
    y,
    radius,
    fill="white",
    outline=None
):

    goto(
        t,
        x,
        y - radius
    )

    t.setheading(0)

    t.color(outline or fill, fill)

    t.begin_fill()

    t.circle(radius)

    t.end_fill()


def line(
    t,
    x,
    y,
    length,
    angle=0,
    color="black",
    width=2
):

    goto(
        t,
        x,
        y
    )

    t.setheading(angle)

    t.color(color)

    t.pensize(width)

    t.forward(length)

    t.pensize(1)
