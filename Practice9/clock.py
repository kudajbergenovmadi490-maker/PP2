"""
clock.py - Clock logic for Mickey's Clock application.
Handles time retrieval and angle calculations for clock hands.
"""

import datetime
import math


def get_current_time():
    """
    Returns the current system time as a (minutes, seconds) tuple.
    """
    now = datetime.datetime.now()
    return now.minute, now.second


def get_hand_angle(value, max_value):
    """
    Converts a time value to a rotation angle (in degrees).

    Clock convention:
      - 0 = pointing straight up (12 o'clock)
      - Angle increases clockwise

    Args:
        value     : current time unit (e.g., seconds or minutes)
        max_value : maximum value for that unit (60 for both)

    Returns:
        Rotation angle in degrees (clockwise from 12 o'clock position).
    """
    # Full circle (360°) divided proportionally
    return (value / max_value) * 360


def degrees_to_pygame_angle(degrees):
    """
    Converts a clockwise-from-top angle (clock convention) to the angle
    expected by pygame.transform.rotate(), which rotates counter-clockwise
    from the right (standard math convention).

    pygame.transform.rotate() rotates counter-clockwise, so we negate.
    We also offset by 90° because clock 0° is "up" but math 0° is "right".

    Args:
        degrees : angle in clock convention (0 = up, CW positive)

    Returns:
        Angle suitable for pygame.transform.rotate()
    """
    return -(degrees - 90)
