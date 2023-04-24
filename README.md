# Thermo
Booking recommender system for energy optimization for the GovTech square meters project.

Read the full documentation [here](https://NTTDATAInnovation.github.io/thermo/)

## Try it out (GUI):

A streamlit gui is available in `gui/app`. To run it install poetry with the optional *gui* dependencies:
```bash
poetry install --with gui
```

 and run:
 ```bash
 poetry run streamlit run gui/app.py
 ```

## Installation:
User installation. You will need an environment with *python 3.10*. After that, you can
install the package using `poetry`:

```bash
poetry install
```

### Developer installation:
You will need the development dependencies:
```bash
poetry install --with dev
```

You may also need the flags `--with docs` if you want to test the documentation locally or `--with gui` if you want to try the GUI locally.

## Usage
Building specifications are loaded from a config directory, through the `.from_config` method. The booking state is retrieved under the hood through an open API.

```python
from thermo.recommender import Recommender
from datetime import date

recommender = Recommender.from_config(building_name = "demo_school")
recommendation = recommender.run(day=date.today())

recommendation.show()
```
`show()` returns a color-coded DataFrame.Styler object, similar to the following table
|        |Room A | ... | Room G | Room H   | Room I |
|:------:|:------:|:------:|:--------:|:------:|:------:|
| t_0    | 1.0    | ...    | 1.0      | 1.0    | 0.5    |
| t_1    | 1.0    | ...    | 1.0      | 0.5    | BOOKED |
| t_2    | 1.0    | ...    | 1.0      | 1.0    | 0.0    |
| t_3    | 1.0    | ...    | 1.0      | 0.5    | BOOKED |
| t_4    | 1.0    | ...    | 1.0      | 1.0    | 0.5    |
| t_5    | 0.5    | ...    | 0.5      | 1.0    | 1.0    |
| t_6    | BOOKED | ...    | BOOKED | 0.5    | 1.0    |
| t_7    | 0.0    | ...    | BOOKED   | 1.0    | 1.0    |

Similarly, `top_recommendations()` produces a list of room-time combinations, i.e. booking recommendations, ranked after their aggregated (estimated) cost (*score*).

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

# Presentations
.pdf versions of presentations can be found in `/presentations`.
For .ppt versions, please see the [project Teams channel](https://itellicloud.sharepoint.com/:p:/r/teams/MSTeams_GovTechProject-INTERNNDBS/Shared%20Documents/INTERN%20NDBS/AI-S3-review.pptx?d=w3f5b518c54504a60bc4061387aa50a81&csf=1&web=1&e=3jwbN3) # noqa

<br>
