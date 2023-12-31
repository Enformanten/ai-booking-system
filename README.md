# Thermo
Booking recommender system for energy optimization for the GovTech M<sup>2</sup> OPI AI signature project.

Read the full documentation [here](https://enformanten.github.io/ai-booking-system/)

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
poetry install --with=dev
```

You may also need the flags `--with docs` if you want to test the documentation locally or `--with gui` if you want to try the GUI locally. You will need the flag `--with eda` if you wish to do run the notebooks for exploratory data analysis (EDA) or prototypes.


## Machine learning:

We use `dvc` to run our ML pipelines. To create a model to extract hyperparameters for a given building run the following:
```bash
cd buildings/<building_name>
dvc exp run dvc.yaml
```

For example, for **Strandskolen** in **Aarhus kommune** this would be:
```bash
cd buildings/strandskolen
dvc exp run dvc.yaml
```

If you would like to add a machine learning model for a new school, you should do the following:

```bash
mkdir buildings/<building_name>  # This creates the directory, skip it if you already have one
cd buildings/<building_name>
dvc init --subdir
git add .
git commit -m "Add dvc tracking for school <building_name>"
```

This will create a DVC project for the school and commit al the DVC metafiles and directories. You can read more on this [here](https://dvc.org/doc/user-guide/basic-concepts/dvc-project).

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



# Docker GUI
The dir `gui` contains a Dockerfile and a requirements.txt file. From the root dir, run
```bash
docker build -t streamlit -f gui/dockerfile .
```
and navigate to `http://localhost:8000/` to access the app.

## Deploy GUI
**NOTE**: The `sudo` cmds may be necessary to connect to Azure ACR!

```bash
# Set the tenant ID and login to Azure CLI using device code authentication
sudo az login --use-device-code --tenant <tenant ID>

# Set the subscription ID
# Login to the Azure Container Registry
# Check the available tags for the repository
sudo az account set --subscription <sub ID>

sudo az acr login --name acrgovtech
az acr repository show-tags --name acrgovtech --repository acrgovtech

# Set the tag for the Docker image
export TAG=<your_tag>

# Build and tag the Docker image
sudo docker build -t acrgovtech.azurecr.io/acrgovtech:$TAG -f gui/dockerfile .

# Run the Docker image on port 8000
sudo docker run -p 8000:8000 acrgovtech.azurecr.io/acrgovtech:latest

# Push the Docker image to the Azure Container Registry
sudo docker push acrgovtech.azurecr.io/acrgovtech:latest
sudo docker push acrgovtech.azurecr.io/acrgovtech:$TAG

# Restart the Azure Web App with the new version
az webapp restart --name app-govtech --resource-group rg-govtech

# View the logs of the Azure Web App
az webapp log tail --name app-govtech --resource-group rg-govtech
```
