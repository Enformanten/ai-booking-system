import matplotlib.pyplot as plt
import numpy as np

from thermo.heater import ProportionalHeater
from thermo.schedule import Schedule
from thermo.school import School
from thermo.simulator import Simulator

# Make a school: Room distribution
A = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]])
school = School(A, 0.05, 0.2)

# Make 4 identical heaters for the school
heaters = [ProportionalHeater(k=10, max_heat=5) for _ in range(school.D)]
school.set_heaters(heaters)

# Set up the school schedule, in hours
schedule = Schedule(
    schedule=np.array(
        [
            np.zeros(4),
            [1, 0, 1, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
            np.zeros(4),
        ]
    ),
    target_temperature=24,
    keep_warm=0,
)

# Run the simulation
simulation = Simulator(school, T_out=15.0, schedule=schedule)
simulation.simulate(max_time=len(schedule.schedule) * 0.98 * 60)

# Extract the variables
t = simulation.t  # time
y = simulation.T  # temperature
u = simulation.U  # Energy

# Visualization
fig, axes = plt.subplots(1, 5, figsize=(9, 4), tight_layout=True)


def is_on(schedule, t):
    return np.array([schedule[int(tt // 60)] for tt in t])


for i, ax in enumerate(axes[:4]):
    ax.plot(t, y[:, i])
    sch = schedule.schedule[:, i]
    ax.plot(t, 24 * is_on(sch, t), "k--")
    ax.set_title(f"Room {i+1}")
    ax.set_ylabel("Temperature")
    ax.set_ylim((14, 25))

ax = axes[-1]
ax.plot(t, u, "r")
ax.set_title("Cumulative energy")
ax.set_ylabel("Energy")
plt.savefig("small_school.png")
