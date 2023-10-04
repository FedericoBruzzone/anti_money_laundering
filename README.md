|Decision Tree | Random Forest|
|-|-|
|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg) ](https://colab.research.google.com/github/federicobruzzone/anti-money-laundering/blob/main/decision_tree.ipynb)| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg) ](https://colab.research.google.com/github/federicobruzzone/anti-money-laundering/blob/main/random_forest.ipynb)|

# Anti Money Laundering

The project is based on the analysis of the «IBM Transactions for Anti Money Laundering» dataset published on Kaggle. The task is to implement a system which predicts whether or not a transaction is illicit, using the attribute "Is Laundering" as a label to be predicted.

## Starting point working locally

**Kaggle instructions**

1. Create `.env` file using the following template:
```env
KAGGLE_USER=
KAGGLE_KEY=
KAGGLE_DATASET_LINK=ealtman2019/ibm-transactions-for-anti-money-laundering-aml
VIEW=default-viewer|code|""
VERBOSE=0|1
```

2. If you prefer to use Kaggle-style configuration, you need to create `.kaggle` folder in the root directory and add `kaggle.json` into using the following template:
```json
{
    "username":"",
    "key":""
}
```

**Create and start a new virtual environment**

`source create_venv.sh venv`

**Start current virtual environment**

`source venv/bin/activate`

**Deactivate the current virtual environment**

`deactivate`

### Run the `<file>.py` file

`python3 -m src.<file>`

### Using Virtual Environments in Jupyter Notebook and Python

**Add Virtual Environment to Jupyter Notebook**

Install ipykernel which provides the IPython kernel for Jupyter:

```pip install --user ipykernel```

Add your virtual environment to Jupyter by typing:

```python -m ipykernel install --user --name=<name>```

This should print the following:

```Installed kernelspec myenv in /home/user/.local/share/jupyter/kernels/<name>```

**Remove Virtual Environment from Jupyter Notebook**

List the kernel with:

```
jupyter kernelspec list
```

This should return something like:

```
Available kernels:
  <name>     /home/user/.local/share/jupyter/kernels/<name>
  python3    /usr/local/share/jupyter/kernels/python3
```

To uninstall the kernel, type:

```jupyter kernelspec uninstall <name>```

## Contributing

Contributions to this project are welcome! If you have any suggestions, improvements, or bug fixes, feel free to submit a pull request.

## License

This repository is licensed under the [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html). Please review the license file provided in the repository for more information regarding the terms and conditions of the GPL license.

## Contact

If you have any questions, suggestions, or feedback, do not hesitate to [contact me](https://federicobruzzone.github.io/).

