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
