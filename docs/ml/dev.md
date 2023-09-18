# Development information for ML pipelines

## Testing:
The GitHub repository for [thermo](https://nttdatainnovation.github.io/thermo/) includes a number of tests to ensure the quality of the ML pipelines.

### Unit tests:
Unit tests have been written to ensure the integrity of the different components of the pipeline. They can be found [here](https://github.com/NTTDATAInnovation/thermo/tree/main/tests/unit_tests/test_stages). These tests are run, together with the other unit tests of the project, as part of the `testing/pytest` job every time code is pushed to the repository.

### Intergrity test for all pipelines:
The job `testing/test_dvc` is run every time code is pushed to the repository. This component does a **dry run** of all the `dvc` pipelines under `buildings`, that is: `bulidings/*/dvc.yaml`.

This checks that the pipeline files are understandable to `dvc` themselves, but does not ensure that they run with no errors (that will depend on the data, among other things).

### ML integration tests:
