# Installation instructions

We recommend that you install the satellite system objects (SSO) generator in a conda environment.

If you don't have conda already, you can find it here: [Miniconda](https://www.anaconda.com/download/success) 
following the [instructions](https://www.anaconda.com/docs/getting-started/miniconda/install) for your operating system. 
Once you have miniconda, create a new conda environment using the (LINK UPDATE) [myenv.yml](https://drive.google.com/file/d/1e44vjI2q-3aW41ChRvum1KCcGCevo2tf/view?usp=sharing) file.

In a terminal (or Anaconda Powershell prompt for Windows), run:

```
conda env create -f myenv.yml
```

Then, activate the conda environment:

```
conda activate my-env
```

Clone the repository and pip install:

```
git clone https://gitlab.com/link/to/your/repo-name.git
cd repo-name
pip install .
```


