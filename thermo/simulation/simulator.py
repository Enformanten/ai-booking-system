import numpy as np
import scipy.integrate as integrate

from thermo.simulation.schedule import Schedule
from thermo.simulation.school import School


class Simulator:
    """
    Simulation class to simulate the amount of heating used to heat
    a building. It uses Runge-Kutta method to solve the system of
    differential equations.
    Args:
    -----
    school: School object containing the geometry and heaters of the school
    T_out: Outdoors temperature
    schedule: Schedule of the school for that day.
    """

    def __init__(self, school: School, T_out: float, schedule: Schedule):
        self.school = school
        self.schedule = schedule
        self.T_out = T_out
        self.solver = None

    @property
    def t(self) -> np.ndarray:
        return np.array(self._t)

    @property
    def T(self) -> np.ndarray:
        return np.array(self._y)

    @property
    def U(self) -> np.ndarray:
        return integrate.cumulative_trapezoid(np.array(self._U), self.t, initial=0)

    def init_variables(self) -> tuple:
        return self.T_out * np.ones(self.school.D), 0.0

    def init_solver(self, max_time: float, *args, **kwargs):
        y0, t0 = self.init_variables()
        self.solver = integrate.RK45(
            self.ODE, t0, y0, t_bound=max_time, *args, **kwargs
        )
        self._t = [t0]
        self._y = [y0]
        self._U = [0.0]

    def ODE(self, t: float, y0: np.ndarray) -> np.ndarray:
        T = y0.copy()
        q_i = self.school.outer_heat_transfer(T, self.T_out)
        q_ij = self.school.inner_heat_transfer(T)
        c_i = self.school.heat_sources(T, self.schedule.get_target(t), t)
        return c_i - q_i - q_ij.sum(axis=1)

    def step(self):
        self.solver.step()

        t = self.solver.t
        self._t.append(t)
        self._y.append(self.solver.y)
        U = self.school.heat_sources(
            self.solver.y, self.schedule.get_target(t), t
        ).sum()
        self._U.append(U)

    def simulate(self, max_time: float, *args, **kwargs):
        self.init_solver(max_time=max_time, *args, **kwargs)
        while True:
            try:
                self.step()
            except RuntimeError:
                break
