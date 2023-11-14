# Usage

## Login Panel

Enter your API key into the "Enter your API key" input box, and click the "Login" button:

<!-- ![](https://hackmd.io/_uploads/rkSlyU3-T.png) -->
![](https://hackmd.io/_uploads/rkiuepA-a.jpg)

The default service endpoint url should be suitable. However, you can target a different endpoint by clicking the "Configure Endpoint" button.

If you wish to view diagnostic information (useful for debugging), you can click on the "twinLab" logo.

## Datasets Panel

This panel allows you to manage your datasets.
![](https://hackmd.io/_uploads/S1mc-pAZT.jpg)

<!-- ![](https://hackmd.io/_uploads/SJuZlU3-p.png) -->

### Upload a Dataset

A dataset is a rectangular array of cells, with string-named headers, and numerical data. Conceptually, there must be at least one "input" column, and at least one "output" column, and should contain some rows of data. The machine learning model we'll train later won't function too well without it!

For example:

| input_a | input_b | input_c | output_x | output_y |
|:--------|:-------:|:-------:|:--------:|:--------:|
|  1.0    |  1.0    |  2.0    |  2.0     |  0.5     |
|  2.0    |  3.0    | -2.0    | -12.0    | -3.0     |
|  4.0    |  2.0    |  1.0    |  8.0     |  8.0     |

In this table, inputs $a$, $b$ and $c$ are random values. $x = a * b * c$ and $y = (a * b) / c$.

You can upload a dataset to your cloud account by first highlighting an array of cells (which should comply with the above format), giving your dataset a unique name, such as "my_dataset", and then clicking the "Upload" button:

<!-- ![](https://hackmd.io/_uploads/BJ2GMU3Wp.png) -->
![](https://hackmd.io/_uploads/Hy1fz6CW6.jpg)

Note your dataset can of course have a different size!

### Listing your Datasets

If you click the "Refresh" button, then you will see you datasets avalible within the "Select a dataset" dropdown menu:
![](https://hackmd.io/_uploads/HJUhfpC-a.jpg)

<!-- ![](https://hackmd.io/_uploads/ryXNzU2WT.png) -->

### View your Dataset

Make sure you have a dataset selected, and then place your marker where you would like to import your dataset, then click the "Download" button to place it within the sheet:
![](https://hackmd.io/_uploads/r1uD7TAba.jpg)

<!-- ![](https://hackmd.io/_uploads/SyUy7U3Zp.png) -->

### Delete your Dataset

Make sure you have a dataset selected, and then click the "Delete" button to delete the dataset stored in the cloud.

Note that this will delete the only copy of your dataset stored in the cloud. No backup exists and there will not be a confirmation step.

## Training Panel

This panel allows your to train a model:
![](https://hackmd.io/_uploads/ryFTm6RWT.jpg)
<!-- 
![](https://hackmd.io/_uploads/Sk72VI2bp.png) -->

### 1. Select a Dataset

Make sure you have a dataset selected. If your dataset does not already appear in the "Select a dataset" dropdown menu, click the "Refresh" button and the dropdown menu should be populated with your dataset ID's.

### 2. Set a Model ID

Enter a unique model ID in the "New model ID" textfield, for example "my_model".

### 3. Set Training Parameters

Model training parameters can be configured by editing the json in the "Training parameters" textfield. For example:

```json
{
    "dataset_id": "my_dataset",
    "inputs": ["input_a", "input_b", "input_c"],
    "outputs": ["output_x", "output_y"],
    "train_test_ratio": 0.8
}
```
You must set the correct "inputs" and "outputs" fields with the column headings of your dataset.
<!-- Required params preserved in case we want them again -->
<!-- #### Required Training Parameters
- **dataset_id**: The dataset ID to use to train the model.
- **inputs**: A list of strings matching the string headers of the input columns.
- **outputs**: A list of strings matching the string headers of the output columns. -->

The `dataset_id`, `inputs`, and `outputs` are required parameters. Additional optional parameters can be used to further customise model training.

<!-- For the bright minds of the future:
 parameters can be found in api/shared/train.py
 docstrings can be found in library/twinlab/campaign/campaign.py-->

#### Optional Training Parameters
- **train_test_ratio**: A value between zero and one, specifying the fraction of the dataset that will be used for training the model. The remaining fraction is used for testing the accuracy of the trained model.
- **seed**: An integer that initialises random processes for reproducibility.
- **estimator**: The type of estimator used when making predictions ("gaussian_process_regression" or "gradient_boosting_regression").
- **model_selection**: A boolean indicating whether to perform automatic model selection.
- **decompose_input**: A boolean indicating whether to apply Singular Value Decomposition (SVD) to the input parameters.
-- **input_explained_variance**: When decompose_input is True, a float specifying how much of the variance should be explained after the truncation of the SVD for functional input.
- **decompose_output**: A boolean indicating whether to apply Singular Value Decomposition (SVD) to the input parameters.
-- **output_explained_variance**: When decompose_output is True, a float specifying how much of the variance should be explained after the truncation of the SVD for functional output.
<!-- Estimator kwargs can be found in library/twinlab/campaign/campaign.py -->
<!-- -- **estimator_kwargs**: -->
<!-- model selection kwargs can be found in library/twinlab/campaign/model_selection.py -->
<!-- -- **model_selection_kwargs**: -->


### Train

Hit the "Train" button to begin trainging the model. Note that this make take several minutes depending on the size of the dataset.

After the request has been submitted, a "Training has started" message will pop-up at the bottom of the panel:
![](https://hackmd.io/_uploads/SkS7E60ba.jpg)

<!-- ![](https://hackmd.io/_uploads/ryMB8Lh-T.png) -->

## Models Panel

The last panel allows you to utilise your models!

### Select a Model

Make sure you have a dataset selected from the "Select a model" dropdown menu:
![](https://hackmd.io/_uploads/HJ1046Ab6.jpg)

<!-- ![](https://hackmd.io/_uploads/ryv-vI3ba.png) -->

If your model isn't already listed then it may either still be training, or the add-in hasn't picked it up yet. Hit the "Refresh" button to trigger the add-in to update your model list.

### Make a Prediction

You can now use your model to perform four functions.

#### 1. Predict

Given some inputs, use the model to predict the *distribution* of values that the outputs could take.

Create a new dataset with the same input column headings as those used to train the model, and add some values that you would like to make a prediction from. Then, select this new dataset in the spreadsheet:
![](https://hackmd.io/_uploads/BJ5MS6RbT.jpg)

<!-- ![](https://hackmd.io/_uploads/ryLXYI3-6.png) -->

Now click the "Predict" button, and **click the spreadsheet cell in which you wish to paste the predicted values into**. After the model has made a prediction the new values will be inserted into the spreadsheet:
<!-- ![](https://hackmd.io/_uploads/rJ1wBpA-T.jpg) -->
![](https://hackmd.io/_uploads/HJoQ2oXza.jpg)

<!-- ![](https://hackmd.io/_uploads/rk3qqInb6.png) -->

See how a mean value prediction has been made for each of the output columns, and a standard-deviation has also been produced, indicating how certain the model is in the prediction.

#### 2. Sample

Similar to the "Predict" method, we can also sample some output values. That is, rather than telling us the distribution of possible output values, the model will actually give us some values sampled from the predicted distribution.

Create a new dataset of the values you wish to sample (with the same setup as the "Predict" method). Then, select this new dataset in the spreadsheet:

<!-- ![](https://hackmd.io/_uploads/BJpEiLhZp.png) -->
![](https://hackmd.io/_uploads/Bkya3o7G6.jpg)


Now set the number of samplings you wish to take next to the "Sample" button. Then click the "Sample" button. **Select the cell in the spreadsheet where you would like the result to be pasted**:

<!-- ![](https://hackmd.io/_uploads/H1OU38n-p.png) -->
![](https://hackmd.io/_uploads/ByJQpiQGa.jpg)


See how five predictions for each output column (labelled 0, 1, 2, 3, 4) have been made. If multiple output columns exist in your dataset, their outputs will be correlated.

The second row in this newly pasted dataset is not a value, it is a label showing which of the output columns are correlated.

#### 3. Active Learning

We can also use the model to tell us where to perform our next "investigation" to maxise the amount of information we'll get for doing so. In other words, the model will tell us where it is most uncertain in the input parameter space.

**Select the cell where you would like the suggestions to be pasted**. Then, select the number of inputs you would like to generate in the "Active learning" input box. Now hit the "Active learning" button, and wait for the output to be pasted into the spreadsheet:
![](https://hackmd.io/_uploads/Sy_sHTAZa.jpg)

<!-- ![](https://hackmd.io/_uploads/HklMCIn-T.png) -->

#### 4. Solve Inverse

Instead of predicting outcomes from inputs, we might want to ask the inverse: what inputs would produce a set of outputs.

Use the input box next to the "Solve Inverse" button to set the ranges of the output values you would like to invert. Then, use the second input box to set the ranges of the output standard deviations. Finally, **select the spreadsheet cell in which you wish to paste the output**, and click the "Solve Inverse" button:

### Delete Your Model

Make sure you have the model ID you wish to remove selected, and then click the "Delete" button to delete the model in the cloud.

Note that this will delete the only copy of your model stored in the cloud. No backup exists and there will not be a confirmation step.

## Having Problems?
If you have any questions or concerns you can email us at twinlab@digilab.co.uk or find out more at [digilab.co.uk/products/twinlab](https://www.digilab.co.uk/products/twinlab)
