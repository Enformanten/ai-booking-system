# School as a graph
*Sprint 3 - AI version 1*

Let every school be represented by one or more graphs, where each node represents a room in the school. In this representation, two rooms share an edge if they share a wall (or a floor-ceiling in case of the school having more than one floor).

In this version, we represent the school as an undirected and unweighted graph, $G_s$. If the graph can be split into several subgraphs, we choose this representation. From here on we assume, for the sake of clarity, that the school is represented by a single, indivisible graph, but the discussion may be extended to multiple graphs in later versions.

Let $N_r$ be the number of rooms in the school and let $i=0, 1, ..., N_r-1$ denote the $i$-th room of the school. Then, the *adjacency matrix* $A_s$ of the school is given by:

$$
    \left( A_s\right)_{ij} =
    \begin{cases}
1 & \text{if } i \text{ and } j \text{ share a wall}, \\
0 & \text{otherwise}.
\end{cases}
$$

## The booking system as a graph

We also represent the booking system as a graph $G$, with $N_r \times N_t$ nodes, where $N_t$ is the number of time slots for a day. The graph $G$ consists of $N_t$ copies of the graph $G_s$, where each copy represents the rooms of the school at a given time slot. Each room is connected to the rooms it shares a wall with, plus to the version of itself in the graphs representing the time-slots that take place immediately before and immediately after.

The adjacency matrix for graph $G$, $A$, is a squared matrix of size $N_t N_r \times N_t N_r$ that can be built in block form as follows:

$$
A = \left(\begin{matrix}
A_s & \lambda\mathbb{I} & \mathbb{O} &\cdots & \mathbb{O} \\
\lambda\mathbb{I} & A_s & \lambda\mathbb{I} & \cdots & \mathbb{O} \\
\mathbb{O} & \lambda\mathbb{I} & A_s  & \cdots & \mathbb{O} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
\mathbb{O} & \mathbb{O} & \mathbb{O} &\cdots & A_s\\
\end{matrix} \right),
$$

where all blocks are of size $N_r \times N_r$,  $\mathbb{I}$ is the *identity matrix*, $\mathbb{O}$ is the *null matrix* and and $\lambda$ is a scalar coefficient representing the relative importance of time respect to space (more about this in the next section).

## Graph-based first-order model for the cost of heating rooms:

Let us discuss how to compute the cost of heating a new room given some rooms have already been booked.

### Qualitative discussion:

As a first order approximation, we can consider that the cost of heating a given room is the cost of heating that room if it was the only room used that day, minus the energy savings coming from other rooms that have already been booked.
We assume those energy savings come from three sources:
*  Heating a room that shares a wall in the same time slot with a room that is already in use,
* The room is already warm because it has been used in the previous time slot,
* If this room is booked, it will already be warm when used in the next time slot.

Intuitively we can think of this model as each room as having an intrinsic cost and then receiving messages from its nearest neighbors in graph $G$ telling it to reduce its cost if they are already booked. The optimal rooms to book will be those that receive the most (or the most important) messages, thus, having the lowest cost.

The parameter $\lambda$ in the definition of $G$ controls the relative importance of the messages:
- if $\lambda > 1$, booking the same room over time is favored over booking adjacent rooms
- if $\lambda < 1$, booking adjacent rooms is favored over booking the same room at subsequent time slots
- and if $\lambda = 1$, the space and time components are treated on equal footing.

The following section discusses a way of formalizing and implementing this model.


### Mathematical formulation of the model

Let $s$ be the *schedule* vector, of size $N_r N_t$, such that

$$
s_i = \begin{cases}
1 & \text{if room } (i \mod N_r) \text{ room is booked} \\
 & \text{at time } (i \div N_t), \\
0 & \text{otherwise};
\end{cases}
$$

where $\div$ represents the integer division and $ \cdot\mod{\cdot}$ represents its reminder.

Equipped with this notation, we can write the first-order approximation of the cost as follows:

$$
c = c_a - \eta As,
$$

where $c$ is the cost vector representing the cost of heating the room, $c_a$ is a vector representing the cost of heating the room if this room at this time slot was the only room booked that day, and $\eta$ is a scalar coefficient representing the relative importance of the messages $As$ compared to the alone costs $c_a$.

## Example:
Let the school have 4 rooms, whose connectivity is given by the following spatial adjacency matrix:

$$
A_s = \left(\begin{matrix}
0 & 1 & 1 & 0 \\
1 & 0 & 0 & 1 \\
1 & 0 & 0 & 1 \\
0 & 1 & 1 & 0
\end{matrix} \right).
$$

The identity matrix for 4 rooms is given by:

$$
\mathbb{I} = \left(\begin{matrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{matrix} \right)
$$

 and the null matrix by:

$$
\mathbb{O} = \left(\begin{matrix}
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{matrix} \right).
$$

Lets assume we have three time slots for the day in question, $t=-1,0,1$. The adjacency matrix $A$ for the booking graph $G$ looks like:

$$
A = \left(\begin{matrix}
A_s & \lambda\mathbb{I} & \mathbb{O} \\
\lambda\mathbb{I} & A_s & \lambda\mathbb{I} \\
\mathbb{O} & \lambda\mathbb{I} & A_s  \\
\end{matrix} \right).
$$

Lets say that the 0-th room was booked at time 0. Then, the schedule vector s looks like:

$$
s = \left(\begin{matrix}
0 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
\end{matrix} \right),
$$

where, $s$ has been displayed in a rooms $\times$ time_slots format for convenience, but please keep in mind that it is a 1-D vector.

The messages $As$ look like:

$$
As = \left(\begin{matrix}
\lambda & 0 & 0 & 0 \\
0 & 1 & 1 & 0 \\
\lambda & 0 & 0 & 0 \\
\end{matrix} \right),
$$

and, if we assume that all rooms where equally costly to heat alone, that is, $c_a = k (1,1,\dots,1)$, then the cost of new possible bookings is:

$$
c = \left(\begin{matrix}
k-\eta\lambda & k & k & k \\
k & k-\eta & k-\eta & k \\
k-\eta\lambda & k & k & k \\
\end{matrix} \right),
$$

where $k$, $\eta$ and $\lambda$ are positive numbers. Note that the room that is already booked doesn't have an outstandingly high cost to be re-booked, this is to be corrected in subsequent versions of the model.

If $\lambda > 1$, the model suggest that the optimal room to book is the 0-th room at time slots $-1$ or $1$, while if its smaller than 1, then its rooms 1 and 2 at time 0 that are optimal for booking.
