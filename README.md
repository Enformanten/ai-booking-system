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


# Presentations
.pdf versions of presentations can be found in `/presentations`.
For .ppt versions, please see the [project Teams channel](https://itellicloud.sharepoint.com/:p:/r/teams/MSTeams_GovTechProject-INTERNNDBS/Shared%20Documents/INTERN%20NDBS/AI-S3-review.pptx?d=w3f5b518c54504a60bc4061387aa50a81&csf=1&web=1&e=3jwbN3) # noqa

<br>
