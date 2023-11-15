# Installation

## Installation for macOS

### Requirements.

* Python 3.9 to 3.11.9 version installed and running for your current environment.
  
*We recommend managing your Python packages with Python virtual environments. See more [here.](https://docs.python.org/3/tutorial/venv.html)*

### Installation

**1.** Open a terminal. 

**2.** Define the folder/directory where you want to install twinlab. Then, set that folder/directory as your current one.

```bash
mkdir my_project 
cd my_project
```

**3.** In your newly created directory, install twinlab on the terminal using **pip3 install twinlab**.

```bash
pip3 install twinlab
```

**4.** Still in the folder/directory that you have selected, create an **.env file** with your given API key. To do this use the following command on the terminal.

```bash
echo -e "TWINLAB_URL=https://twinlab.digilab.co.uk\nTWINLAB_API_KEY=[your_api_key]"> .env
```

**Replace *[your_api_key]* with the API key given as a part of the license acquisition.** (For information on licensing, please contact us [here.](https://www.digilab.co.uk/products/twinlab)

Be aware of any blank spaces in the words between the quotation marks!

To make sure you have created the document in your directory you can use the `ls -a` command on your terminal.

```bash
ls -a
```

As an output, you should see the .env file among your files.

```bash
. .env
```

## Installation for Windows

### Requirements

* Python 3.9 to 3.11.9 version installed and running for your current environment. (To download python visit https://www.python.org/downloads/)
* Microsoft Visual C++ 14 or higher versions installed. 

*We recommend managing your Python packages with Python virtual environments. See more [here.](https://docs.python.org/3/tutorial/venv.html)*

### Installation

**1.** Open a terminal. 

**2.** Define the folder/directory where you want to install twinlab. Then, set that folder/directory as your current one.

```bash
mkdir my_project 
cd my_project
```

**3.** In your newly created directory, install twinlab on the terminal using **pip3 install twinlab**.

```bash
pip3 install twinlab
```

**4.** Still in the folder/directory that you have selected, create an **.env file** with your given API key. To do this use the following command on the terminal.

```bash
echo TWINLAB_URL=https://twinlab.digilab.co.uk > .env && echo TWINLAB_API_KEY=[your_api_key]>> .env && echo TWINLAB_SERVER=https://twinlab.digilab.co.uk >> .env && echo TWINLAB_KEY=[your_api_key]>> .env
```

**Replace *[your_api_key]* with the API key given as a part of the license acquisition.** Notice that you have to replace it twice! (For information on licensing, please contact us [here.](https://www.digilab.co.uk/products/twinlab))

Be aware of any blank spaces in the words between the quotation marks!

To make sure you have created the document in your directory you can use the `dir /a` command on your terminal.

```bash
dir /a
```

As an output, you should see the .env file among your files.

```bash
. .env
```

## Installation for [Colab](https://colab.research.google.com)

### Requirements

* A Google Account

### Installation

**1.** Create a new notebook by going to File -> New Notebook

**2.** Install twinlab into Colab by entering **!pip3 install twinlab** in a code cell and clicking play.

```bash
!pip3 install twinlab
```

**3.** Create an **.env file** with your given API key. To do this enter and play the following command into a new cell:

```bash
echo -e "TWINLAB_URL=https://twinlab.digilab.co.uk\nTWINLAB_API_KEY=[your_api_key]"> .env
```

**Replace *[your_api_key]* with the API key given as a part of the license acquisition.** (For information on licensing, please contact us [here.](https://www.digilab.co.uk/products/twinlab). 

To make sure you have created the document you can use the `ls -a` command on your terminal.

```bash
ls -a
```

As an output, you should see the .env file among your files.

```bash
. .env
```

You can check that the .env file is correctly configured by entering **!more .env** . Be aware of any blank spaces in the words between the quotation marks!

## Import and Use

To start using twinLab, enter the following line of Python.

```python
import twinlab as tl
```

If you run this as a script from the Terminal or in a Colab cell, it should return something like this:

```bash
{'username': 'yourname', 'credits': 0}

         === TwinLab Client Initialisation ===
         Version  : 1.4.0
         User     : yourname
         Server   : https://twinlab.digilab.co.uk
         Key      : your_api_key
```

You're all set! Here's an example script to get you started:

```python
# Import pandas as well
import pandas as pd

# Create a dataset and upload to twinLab cloud
df = pd.DataFrame({"X": [1, 2, 3, 4], "y": [1, 4, 9, 16]})
tl.upload_dataset(df, "test-data")

# Train a machine-learning model for the data
params = {
    "dataset_id": "test-data",
    "inputs": ["X"],
    "outputs": ["y"],
}
tl.train_campaign(params, campaign_id="test-model")

# Evaluate the model on some unseen data
df = pd.DataFrame({"X": [1.5, 2.5, 3.5]})
df_mean, df_std = tl.predict_campaign(df, campaign_id="test-model")

# Explore the results
print(df_mean)
print(df_std)
```

## Having Problems?

If you have any questions or concerns you can email us at twinlab@digilab.co.uk or find out more at [digilab.co.uk/products/twinlab](https://www.digilab.co.uk/products/twinlab).