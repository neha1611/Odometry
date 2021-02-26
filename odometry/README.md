Odometry Dashboard
==============================

Building a Dash application that will help the Experts to Label odometry data, Invoke Training of classification Models, View performance of models and Review the Classification.


## Installation and implementation

- Need python>=3.9.1 and python3-venv, create a new environment first

If python3-env library is not installed, install using below line, after that create environment
```
sudo apt install python3-venv
```

```
python3 -m venv mdp_env
source mdp_env/bin/activate
```

- Git clone (need credentials)
```
git clone -b DashDevelopment https://alstom-smart-mobility@dev.azure.com/alstom-smart-mobility/Odometry/_git/odometry_classification
```

- Install requirements
```
cd odometry_classification/Dash/odometry
pip install -U setuptools wheel pip
pip install -r requirements.txt
```

## To run dash aplication

- First set config varibles in `config.py` present in directory `odometry_classification/Dash/odometry/settings`. Update values for 
APP_HOST, PGHOST, PGDATABASE, PGUSER,PGPASSWORD

-- Install DB schem using 
/odometry_clasification/Dash/odometrt/data/SQL_Script.sql

- to run Dash application (you should be in directory `odometry`)
```
python index.py
```



Project Structure
------------
