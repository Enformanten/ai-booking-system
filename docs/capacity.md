# Model for capacity
*Sprint 4 - AI version 2*

Lets consider the problem with the capacity of the room.

- On the one hand side, it does not make sense to suggest the user a room that is too small for the planned activity: if the participants will not fit in the room, it does not matter if the energy required to heat it and light it is very low.

-  On the other hand side, we want to avoid recommending rooms that are far too big (see below for how we approach defining way too big) for the activity planned: First, because it might result on heating a very big room to have two people in it, but most importantly, because the room could be better booked later by a larger group.

### Mathematical model

We approach the problem as finding a cost for mismatched capacity that can be added to the other energy costs, that is, the electricity and the heating cost.

We define the cost function $C_c$ for a required capacity (i.e. the number of participants in the activity) $x$ as for the $i$-th room as:

$$
C_c(x) = \begin{cases}
\infty & \text{if } x < c_i, \\
\alpha \frac{x-c_i}{c_i} & x \leq c_i.
\end{cases}
$$

where $c_i$ is the capacity (i.e. the amount of people that fit) in room $i$ and $\alpha$ is a coefficient that can be adjusted for business purposes for each school.

Intuitively, this means that its not possible to book the room if $x < c_i$, since the participants will not fit, it is ''for free'' to book it if $x=c_i$, since the participants match the capacity, and if there is free space, there is an additional cost of $\alpha/c_i$ for each free spot in the room.

The factor $1/c_i$ in the expression for the cost models the relative importance of having an extra free sit: while having 5 free spots in a room with capacity for 10 people is having half of the sits empty and is not desirable, having 5 free spots in a room with capacity for 100 people is not a big problem. The first will be punished with an extra $0.5\alpha$ cost while the second example will be punished with the much smaller $0.05\alpha$ cost.
