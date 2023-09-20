# Development information for ML pipelines

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

After this, one needs a `dvc.yaml` and a `params.yaml` file in the `buildings/<building_name>` folder. We recommend copying the files in `demo_school`

```bash
cp buildings/demo_school/dvc.yaml buildings/<building_name>
cp buildings/demo_school/params.yaml buildings/<building_name>
```
into the folder for the new building and modifying the `params.yaml` to fulfill your needs (In particular, to find the appropriate data source files under `assets/`).

Then, running
```bash
cd buildings/<building_name> && dvc exp run dvc.yaml
```
will run the ML pipeline and you will be able to explore the results by examining the files created under:
`buildings/<building_name>/model/`

## Testing:
The GitHub repository for [thermo](https://nttdatainnovation.github.io/thermo/) includes a number of tests to ensure the quality of the ML pipelines.

### Unit tests:
Unit tests have been written to ensure the integrity of the different components of the pipeline. They can be found [here](https://github.com/NTTDATAInnovation/thermo/tree/main/tests/unit_tests/test_stages). These tests are run, together with the other unit tests of the project, as part of the `testing/pytest` job every time code is pushed to the repository.

### Intergrity test for all pipelines:
The job `testing/test_dvc` is run every time code is pushed to the repository. This component does a **dry run** of all the `dvc` pipelines under `buildings`, that is: `bulidings/*/dvc.yaml`.

This checks that the pipeline files are understandable to `dvc` themselves, but does not ensure that they run with no errors (that will depend on the data, among other things).

### ML integration tests:
ML integration tests check that the quality of results of the DVC pipeline for *demo-school*. As such, they need the files the pipeline generates. They are marked with `ml_integration` and they don't run unless they are specifically called for.

The code for the ml_integration tests can be found under `tests/integration_tests/test_mlworkflow`.


#### Running ML integration tests locally
First, you will need to run the `demo_school` pipeline, as:
```bash
cd buildings/demo_school/
dvc exp run dvc.yaml
cd ../..
```
This will generate the files in the folders `buildings/demo_school/data` and `buildings/demo_school/model` that the integration tests need.

Then you can run the test as:
```bash
pytest -m ml_integration
```

#### Running the ml_integration tests in GitHub Actions:
The ML integration tests are run automatically every time code is pushed to the repository, if the unit tests and the dvc tests complete.
The job first runs the `demo_school` dvc pipeline and then runs the tests marked as `ml_integration`.
