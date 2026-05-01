# https://alan-turing-institute.github.io/rse-course/html/module03_research_data_in_python/03_06_boids.html

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

def new_flock(count, lower_limits, upper_limits):
    width = upper_limits - lower_limits
    return lower_limits[:, np.newaxis] + np.random.rand(2, count) * width[:, np.newaxis]

def alpha_boids():
    t = np.linspace(0, 2*np.pi, num=1000)

    x = np.cos(t) / (np.sin(t)**2 + 1)
    y = np.cos(t) * np.sin(t) / (np.sin(t)**2 + 1)

    # plt.plot(x, y)
    # plt.show()

def update_boids(positions, velocities):
    # fly towards the middle
    move_to_middle_strength = 0.004
    offset = 12
    middle = np.mean(positions + offset, 1)
    direction_to_middle = positions - middle[:, np.newaxis]
    velocities -= direction_to_middle * move_to_middle_strength

    # avoid collisions
    separations = positions[:, np.newaxis, :] - positions[:, :, np.newaxis]
    squared_displacements = separations * separations
    square_distances = np.sum(squared_displacements, 0)
    alert_distance = 100
    far_away = square_distances > alert_distance
    separations_if_close = np.copy(separations)
    separations_if_close[0, :, :][far_away] = 0
    separations_if_close[1, :, :][far_away] = 0
    velocities += np.sum(separations_if_close, 1)

    # match speed of nearby birds
    velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]
    formation_flying_distance = 10000
    formation_flying_strength = 0.225
    very_far = square_distances > formation_flying_distance
    velocity_differences_if_close = np.copy(velocity_differences)
    velocity_differences_if_close[0, :, :][very_far] = 0
    velocity_differences_if_close[1, :, :][very_far] = 0
    velocities -= np.mean(velocity_differences_if_close, 1) * formation_flying_strength

    # update positions
    positions += velocities

    # update the angle boids point toward
    # https://github.com/matplotlib/matplotlib/pull/20914

def animate(frame):
    update_boids(positions, velocities)
    scatter.set_offsets(positions.transpose())

limits = np.array([2000, 2000])
positions = new_flock(420, np.array([500, 700]), np.array([1500, 1300]))
velocities = new_flock(420, np.array([-8, -5]), np.array([0, 0]))
alpha_positions = new_flock(1, np.array([500, 1000]), np.array([501, 1001]))
alpha_velocities = new_flock(1, np.array([0, 0]), np.array([0, 0]))

# need to animate 2 subplots
# https://search.brave.com/search?q=pyplot+two+animations

figure = plt.figure()
axes = plt.axes(xlim=(0, limits[0]), ylim=(0, limits[1]))
scatter = axes.scatter(
    positions[0, :], positions[1, :], marker="$>$", edgecolor="k", lw=0.5
)

# anim = animation.FuncAnimation(figure, alpha_boids, frames=300, interval=35)
anim = animation.FuncAnimation(figure, animate, frames=400, interval=40)
anim.save("boids_1.gif")

git config --global user.name "slantedtable"
git config --global user.email "agraemelowe@gmail.com"
