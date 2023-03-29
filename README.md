# Thermo
Small package for energy consumption simulation

## Short description of the principle:
We use a thermal diffusion model to simulate the heat transfer between rooms and to the outside of a school.
We assume that the school and its internal walls are well insulated compared to the thermal conductivity of air,
this is, we assume that the temperature in a room is almost constant with respect to the position inside it.

We know there will be radiation effects (this is, rooms facing south will be warmer than rooms facing north when the
heating is off) but we haven't taken them into account.

We know there will be convection effects (this is, heat losses due to air currents), both from humans opening and
closing the windows (but this we will never be able to model, at least not without extra information) and from
the compulsary ventilation of the building. We haven't included a convection term, since it would make the simulation
quite challenging, and we hope that the thermal loss due to built-in ventilation can be assimilated to diffusion losses
through walls.

We assume the school has some sort of automation built in for the heaters, so that they are able to turn on
when there is a lecture and turn off when the room is not being used. Note we haven't done a full study of how a proper
controler would work, since we haven't considered retrofitting effects into the controler.

We have not considered other sources of heat, such as the people in the room, the lightbulbs for illumination or the computers.
Thus, we assume that the room is relativelly "large" compared to the number of people "crammed" in. We can come back to this later,
since it may have some impact in the optimization.

These considerations result in a linear inhomogeneous system of ordinary differential equations. Eventhough we know it would
be possible to transform the problem to the Laplace space to get a system of linear algebraic equations instead and then
transform back, making the module less computationally expensive, we have chosen not to do so for the moment. Instead, we
choose to use a Runge-Kutta method, as implemented in scipy. This implementation is more intuitive and easier to extend,
so we keep it for now. The same applies to the integral to calculate the the cumulative energy: we have used a Simpson method
because it is more flexible but if it became a bottleneck, we could use a Romberg method (they are both implemented in scipy).



## First version of model
```ipython
In [1]: from thermo.cost_model.model import HeatModel

In [2]: import numpy as np

In [4]: As = np.array([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]])

In [5]: model = HeatModel(As, 3)

In [6]: state = np.zeros(12)

In [7]: state[4] = 1

In [8]: model.run(state)
Out[8]: array([0, 0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan])
```
