import numpy as np

from thermo.heater import ProportionalHeater
from thermo.schedule import Schedule
from thermo.school import School
from thermo.simulator import Simulator

# Make a school: Room distribution
D = 12
A = np.zeros((D, D))

connections = [
    (0, 1),
    (1, 2),
    (2, 3),
    (4, 5),
    (5, 6),
    (6, 7),
    (8, 9),
    (9, 10),
    (10, 11),
    (0, 4),
    (4, 8),
    (1, 5),
    (5, 9),
    (2, 6),
    (6, 10),
    (3, 7),
    (7, 11),
]

for conn in connections:
    pass
    A[conn] = 1
A += A.T


school = School(A, 0.05, 0.2)

# Make 4 identical heaters for the school
heaters = [ProportionalHeater(k=10, max_heat=5) for _ in range(school.D)]
school.set_heaters(heaters)

# Set up the school schedule, in hours
template = np.zeros(12)


def put(arr, idx, val):
    arr = arr.copy()
    np.put(arr, idx, val)
    return arr


def test(hour_1_rooms: list):
    schedule = Schedule(
        schedule=np.array(
            [
                template.copy(),
                put(template, [4], [1]),
                put(template, hour_1_rooms, np.ones(len(hour_1_rooms))),
                put(template, [4], [1]),
                template.copy(),
            ]
        ),
        target_temperature=19,
        keep_warm=0,
    )

    # Run the simulation
    simulation = Simulator(school, T_out=-1, schedule=schedule)
    simulation.simulate(max_time=len(schedule.schedule) * 0.98 * 60)

    # Extract the variables
    print(f"Total consumption: {simulation.U[-1]:.2f}")  # noqa


print("Before any additional bookings")  # noqa
test([3, 11])
print("Book room 4 during hour 1")  # noqa
test([3, 4, 11])
print("Book room 7 during hour 1")  # noqa
test([3, 7, 11])
