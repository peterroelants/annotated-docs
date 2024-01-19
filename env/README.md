# Python Environment

## Conda environment

The provided conda environment at `env.yml` can be built and activated locally if you have [mamba](https://mamba.readthedocs.io/en/latest/) or [conda](https://docs.conda.io/en/latest/) installed (in replace `mamba` by `conda` in that case), by running the following from the project root:
```
mamba env create --file ./env/env.yml
conda activate annotated_docs_env
```

And can be cleaned up afterwards with:
```
conda deactivate && conda remove --yes --name annotated_docs_env --all
```


### Local package

The local package at `./src/annotated_docs` can be installed with `pip install --editable .`, this makes all the packages importable and editable while preventing any issues with mis-specified PythonPath variables.


## Pre-commit hooks
[Pre-commit](https://pre-commit.com/) [hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) can be setup using:
```
conda run -n annotated_docs pre-commit install
```
