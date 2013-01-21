#!/usr/bin/env python

"""A solar system orrery as a simple OO test for programming in Python."""

# Solar System Orrery in Python
# Mon 2011-04-11 00:33:29 -0400
# 
# Copyright (C) 2013 by Ken Guyton.  All Rights Reserved.

__author__ = 'Ken Guyton'

import argparse
import math

EARTH = ('Earth', 1.0, 0.0)
JUPITER = ('Jupiter', 5.0, 0.0)
NEPTUNE = ('Neptune', 30.1, 0.0)


class Planet(object):
  """A planet with a name, semi-major axis and position angle in degrees."""

  def __init__(self, name, radius, pos_angle=0.0):
    """Initialize a planet.

    Args:
      name: str.  The planet's name.
      radius: float.  The semi-major axis in AU.
      pos_angle: float.  The planet's position in it's orbit in degrees
    """

    self.name = name
    self.radius = radius
    self.pos_angle = pos_angle
  
  @property
  def period(self):
    """Return the period of the planet's orbit in years.

    This is where the astronomy happens since the period is computed using
    Kepler's law.
    """

    return math.pow(self.radius, 1.5)

  def step(self, deltatime):
    """Advance the planet along it's orbit for deltatime years."""

    self.pos_angle += 360.0 / self.period * deltatime

    # Normalize the angle.
    while self.pos_angle >= 360.0:
      self.pos_angle -= 360.0

  def __str__(self):
    return '%-7s %4.1f per %5.1f at %.2f' % (self.name, self.radius,
                                            self.period, self.pos_angle)


class Orrery(object):
  """A container of several planets."""

  def __init__(self):
    """Add planets to the orrery."""

    self.planets = (Planet(*EARTH), Planet(*JUPITER), Planet(*NEPTUNE))

  def step(self, deltatime):
    """Advance all of the planets along their orbits for deltatime years."""

    for planet in self.planets:
      planet.step(deltatime)

  def __str__(self):
    return '\n'.join([str(x) for x in self.planets])


class Runner(object):
  """Run an orrery, track the time passed and format the ouput."""

  def __init__(self, orrery, step=0.5, count=5):
    """Store the orrery, step size,  count, time and counter."""

    self.orrery = orrery
    self.step = step
    self.count = count
    self.time = 0.0
    self.counter = 0

  def print_orrery(self):
    """Print the orrery."""

    print 'Step = %d.  Time = %.2f' % (self.counter, self.time)
    print self.orrery
    print

  def step_runner(self):
    """Step the running orrery."""

    self.counter += 1
    self.time += self.step
    self.orrery.step(self.step)

  def run(self):
    """Run the orrery."""

    self.print_orrery()
    for unused_i in range(self.count):
      self.step_runner()
      self.print_orrery()


def main():
  """Create an orrery and run it."""

  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--count', type=int, default=5,
                      help='Step this many times.')
  parser.add_argument('-s', '--step', type=float, default=0.5,
                      help='Step size in years.')
  args = parser.parse_args()

  print '\nStepping the Orrery %d times' % args.count,
  print 'with step size %.2f\n' % args.count
  
  orrery = Orrery()
  orrery_runner = Runner(orrery, args.step, args.count)
  orrery_runner.run()


if __name__ == '__main__':
  main()
