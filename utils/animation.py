import math


def lerp(depart, arrive, facteur):
    return depart + (arrive - depart) * facteur


def lerp_position_2d(position_depart: tuple, position_arrive: tuple, facteur) -> tuple:
    return (lerp(position_depart[0], position_arrive[0], facteur), lerp(position_depart[1], position_arrive[1], facteur))


def ease_in_out(t):
    return math.sin(t * math.pi / 2)


def ease_out_back(t):
    if t == 0:
        return 0
    elif t >= 1:
        return 1
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)


def easeInOutExpo(t):
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2
    

def linear(t):
    return t


def animate(animate_func, depart, arrive, t):
    return lerp(depart, arrive, animate_func(t))


def animate_position_2d(animate_func, position_depart: tuple, position_arrive: tuple, t) -> tuple:
    return (animate(animate_func, position_depart[0], position_arrive[0], t), animate(animate_func, position_depart[1], position_arrive[1], t))
