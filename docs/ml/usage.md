# Using the ML pipelines

## Setup

This project uses [DVC](https://dvc.org/) (Data Version Control) for the version control of datasets and machine learning models, as well as for organizing machine learning pipelines and workflows.

In order to use it, it is necessary to install [thermo](https://nttdatainnovation.github.io/thermo/) with its *development* dependencies:
```bash
poetry install --with dev
```

## Running an existing pipeline

To create a model to extract hyperparameters for a given building run the following:
```bash
cd buildings/<building_name>
dvc exp run dvc.yaml
```

For example, for **Strandskolen** in **Aarhus kommune** this would be:
```bash
cd buildings/strandskolen
dvc exp run dvc.yaml
```

### Troubleshooting
Make sure to store that the source data is stored in the `assets` directory into `csv` files, so that the pipeline is able to find them.

You might need to indicate to the pipeline the name and the contents of the original files. This can be done by modifying the `params.yaml` file in the `building/<building_name>` folder.

## Creating a new pipeline for a new building / school:
If you would like to add a machine learning model for a new school, you should do the following:

```bash
mkdir buildings/<building_name>  # This creates the directory, skip it if you already have one
cd buildings/<building_name>
dvc init --subdir
git add .
git commit -m "Add dvc tracking for school <building_name>"
```

This will create a DVC project for the school and commit al the DVC metafiles and directories. You can read more on this [here](https://dvc.org/doc/user-guide/basic-concepts/dvc-project).
