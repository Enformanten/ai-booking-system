# Thermo
**Booking recommender system for energy optimization for the GovTech Smart M<sup>2</sup> project OPI project.**

### Background
The purpose of the OPI project is to achieve savings on energy and climate consumption by consolidating activities, implementing intelligent local allocation, and increasing the utilization rate of the municipal building stock through the use of building data, IoT solutions (Internet of Things), and artificial intelligence (AI).

The municipalities wish to carry out a public-private innovation collaboration with NTT DATA, in which the municipalities, together with NTT DATA, investigate, test, and specify which components and processes are necessary, regardless of the choice of supplier, for a later solution in a nationwide tender, which focuses on providing insight and overview of energy consumption at the three selected primary schools, and to develop the solution as an AI solution for optimizing energy consumption outside of normal school hours, from 4pm to 10pm on weekdays and during the weekends. Daytime hours are not included in local optimization as it is not possible to extract data from AULA, and because it would exceed the project's economic framework to rely on a solution that can retrieve data from AULA through alternative means.

### Project objectives
- To provide users with an overview of possible bookings for a given building, ranked by estimated energy optimality.
- To use existing data sources to estimate the energy cost associated with possible bookings, including:
    - Building plan (room location relative to other rooms)
    - Room capacity and inherent functionalities (whiteboard, kitchen equipment, etc.)
    - Indoor climate
    - Energy consumption
- To identify the necessary data sources to build this type of AI solution.

### Users
- Building managers (professionals responsible for booking rooms on behalf of leisure users and/or monitoring and controlling CTS operation).
- Leisure users (third-party users who want to book a room in the given building).

### Use case
(What actions should be possible via the AI solution?)
(In the following, it is assumed that the AI solution is connected to a web-based application with a GUI)
- Retrieve/see a ranked list of estimated climate-optimal bookings for a given building at the given time.

### Demo GUI
A GUI (built in streamlit) is available @ https://app-govtech-demo.azurewebsites.net/
**NOTE**: May be taken down during/after the project.

<br>

***

<br>

## Example usage
(Installation guide is excluded from this public documentation.)
Building specifications are loaded from a config directory, through the `.from_config` method. The booking state is retrieved under the hood through an open API.

```python
from thermo.recommender import Recommender
from datetime import date

recommender = Recommender.from_config(building_name = "demo_school")
recommendation = recommender.run(day=date.today())

recommendation.show()
```
`show()` returns a color-coded DataFrame.Styler object, similar to the following table

<br>


|        |Room A | ... | Room G | Room H   | Room I |
|:------:|:------:|:------:|:--------:|:------:|:------:|
| t_0    | 1.0    | ...    | 1.0      | 1.0    | 0.5    |
| t_1    | 1.0    | ...    | 1.0      | 0.5    |  |
| t_2    | 1.0    | ...    | 1.0      | 1.0    | 0.0    |
| t_3    | 1.0    | ...    | 1.0      | 0.5    |  |
| t_4    | 1.0    | ...    | 1.0      | 1.0    | 0.5    |
| t_5    | 0.5    | ...    | 0.5      | 1.0    | 1.0    |
| t_6    |  | ...    |  | 0.5    | 1.0    |
| t_7    | 0.0    | ...    |    | 1.0    | 1.0    |

<br>

With the empty cells representing time slots that are either already booked or infeasible due to the booking requirements (e.g., required capacity or particular amenities such as a whiteboard)

Similarly, `recommendation.top_recommendations()` produces a list of room-time combinations, i.e. booking recommendations, ranked after their aggregated (estimated) cost (*score*).

| Time Slot | Room | Score  |
|:---------:|:----:|:------:|
| t_2  | Room I | 0.0      |
| t_7  | Room E | 0.0      |
| t_0  | Room I | 0.5      |
| t_1  | Room H | 0.5      |
| t_3  | Room H | 0.5      |
| ...  | ...    | ...      |
| t_7  | Room F | 1.0      |

<br>

### User arguments
User arguments (i.e. booking requirements) are passed to the `.run` function of the `Recommender`.

```python
recommendation = recommender.run(
    recommender=recommender,
    day=date.today(),
    required_amenities=REQUIRED_AMENITIES,
    ...
    required_capacity=REQUIRED_CAPACITY,
)
```
