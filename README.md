# IP Geolocation Visualizer

Copyright (c) 2020 Yiming Lin

This repository implements a visualier for client geolocation based on data provided in [*CS510 SRE course*](https://sites.google.com/pdx.edu/sre-fall-2020/home?authuser=0). The following instructions guide how to run our work.

### Running Environment
Our code is developed under Windows operating system, in order to run our code, install [Adaconda](https://www.anaconda.com/) is required. After install [Adaconda](https://www.anaconda.com/), a Adaconda powershell prompt is also installed on your machine, open it and type in the following commands.

```sh
$ conda install --channel conda-forge geopandas
```

Install and activate geo_env virtual environment

```sh
$ conda create -n geo_env
$ conda activate geo_env
$ conda config --env --add channels conda-forge
$ conda config --env --set channel_priority strict
```

Install required dependencies

```sh
$ conda install python=3 geopandas
$ conda install python=3 matplotlib
```

### Replace ipinfo Token
```sh
$ vim gen_coords.py
```
Then replace line 7 to your own ipinfo token, which can be acquired [here](https://ipinfo.io/) by signing up. 