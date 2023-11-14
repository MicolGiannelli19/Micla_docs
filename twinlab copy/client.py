# Standard imports
import io
import json
from pprint import pprint
import time
from typing import Union, Optional, Tuple

# Third-party imports
import pandas as pd
from typeguard import typechecked

# Project imports
from . import api
from . import settings
from . import utils


### Utility functions ###

# TODO: Move to utils.py?


def _get_value_from_body(key: str, body: dict):
    # Improve the error messaging and relate response from api.py directly here
    if key in body.keys():
        return body[f"{key}"]
    else:
        print(body)
        raise KeyError(f"{key} not in API response body")


def _status_campaign(
    campaign_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> dict:
    response = api.get_status_model(campaign_id, verbose=debug)
    if verbose:
        message = _get_message(response)
        print(message)
    return response


def _get_csv_string(filepath_or_df: Union[str, pd.DataFrame]) -> str:
    if type(filepath_or_df) is str:
        filepath = filepath_or_df
        csv_string = open(filepath, "r").read()
    elif type(filepath_or_df) is pd.DataFrame:
        df = filepath_or_df
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        csv_string = buffer.getvalue()
    else:
        raise ValueError("filepath_or_df must be a string or pandas dataframe")
    return csv_string


@typechecked
def _use_campaign(
    campaign_id: str,
    method: str,
    filepath_or_df: Optional[Union[str, pd.DataFrame]] = None,
    filepath_or_df_std: Optional[Union[str, pd.DataFrame]] = None,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
    **kwargs,
) -> Union[io.StringIO, list, float]:
    if filepath_or_df is not None:
        data_csv = _get_csv_string(filepath_or_df)
    else:
        data_csv = None
    if filepath_or_df_std is not None:
        data_std_csv = _get_csv_string(filepath_or_df_std)
    else:
        data_std_csv = None
    response = api.use_model(
        campaign_id,
        method,
        data_csv=data_csv,
        data_std_csv=data_std_csv,
        processor=processor,
        verbose=debug,
        **kwargs,
    )

    if method in ["predict", "sample", "get_candidate_points", "solve_inverse"]:
        output_csv = _get_value_from_body("dataframe", response)
        return io.StringIO(output_csv)
    else:
        output_list = _get_value_from_body("result", response)
        return output_list


def _get_message(response: dict) -> str:
    # TODO: This could be a method of the response object
    # TODO: This should be better
    try:
        message = response["message"]
    except:
        message = response
    return message


### ###

### General functions ###


@typechecked
def get_user_information(
    verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> dict:
    """
    # Get user information

    Get information about the user

    ## Arguments

    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `dict` containing user information

    ## Example
    ```python
    import twinlab as tl

    user_info = tl.get_user_information()
    print(user_info)
    ```
    """
    response = api.get_user(verbose=debug)
    user_info = response
    if verbose:
        print("User information:")
        pprint(user_info, compact=True, sort_dicts=False)
    return user_info


@typechecked
def get_versions(
    verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> dict:
    """
    # Get versions

    Get information about the twinLab version being used

    ## Arguments

    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `dict` containing version information

    ## Example
    ```python
    import twinlab as tl

    version_info = tl.get_versions()
    print(version_info)
    ```
    """
    response = api.get_versions(verbose=debug)
    version_info = response
    if verbose:
        print("Version information:")
        pprint(version_info, compact=True, sort_dicts=False)
    return version_info


### ###

### Dataset functions ###


@typechecked
def upload_dataset(
    filepath_or_df: Union[str, pd.DataFrame],
    dataset_id: str,
    use_upload_url: Optional[bool] = True,
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
) -> None:
    """
    # Upload dataset

    Upload a dataset to the `twinLab` cloud so that it can be queried and used for training.

    ## Arguments

    - `filepath_or_df`: `str` | `Dataframe`, location of csv dataset on local machine or `pandas` dataframe
    - `dataset_id`: `str`, name for the dataset when saved to the twinLab cloud
    **Warning:** If the `dataset_id` already exists for the current cloud account, it will be overwritten by the
    newly uploaded dataset
    - `use_upload_url`: `bool`, Optional, determining whether to upload via a pre-signed url or directly to the server
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional,determining level of information logged on the server

    **NOTE:** Local data must be a CSV file, working data should be a pandas Dataframe.

    ## Examples

    Upload a local file:
    ```python
    import twinlab as tl

    data_filepath = "path/to/dataset.csv"
    tl.upload_dataset(data_filepath, "my_dataset")
    ```

    Upload a `pandas` dataframe:
    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    ```
    """

    # Upload the file (either via link or directly)
    if use_upload_url:
        response = api.generate_upload_url(dataset_id, verbose=debug)
        upload_url = _get_value_from_body("url", response)
        if type(filepath_or_df) is str:
            filepath = filepath_or_df
            utils.upload_file_to_presigned_url(
                filepath, upload_url, verbose=verbose, check=settings.CHECK_DATASETS
            )
        elif type(filepath_or_df) is pd.DataFrame:
            df = filepath_or_df
            utils.upload_dataframe_to_presigned_url(
                df, upload_url, verbose=verbose, check=settings.CHECK_DATASETS
            )
        else:
            raise ValueError("filepath_or_df must be a string or pandas dataframe")
        if verbose:
            print("Processing dataset.")
        response = api.process_uploaded_dataset(dataset_id, verbose=debug)

    else:
        csv_string = _get_csv_string(filepath_or_df)
        response = api.upload_dataset(dataset_id, csv_string, verbose=debug)

    if verbose:
        message = _get_message(response)
        print(message)


@typechecked
def list_datasets(
    verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> list:
    """
    # List datasets

    List datasets that have been uploaded to the `twinLab` cloud

    ## Arguments

    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `list` of `str` dataset ids

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    datasets = tl.list_datasets()
    print(datasets)
    ```
    """
    response = api.list_datasets(verbose=debug)
    datasets = _get_value_from_body("datasets", response)
    if verbose:
        print("Datasets:")
        pprint(datasets, compact=True, sort_dicts=False)
    return datasets


@typechecked
def view_dataset(
    dataset_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> pd.DataFrame:
    """
    # View dataset

    View a dataset that exists on the twinLab cloud.

    ## Arguments

    - `dataset_id`: `str`; name for the dataset when saved to the twinLab cloud
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `pandas.DataFrame` of the dataset.


    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    df = tl.view_dataset("my_dataset")
    print(df)
    ```
    """
    response = api.view_dataset(dataset_id, verbose=debug)
    csv_string = _get_value_from_body("dataset", response)
    csv_string = io.StringIO(csv_string)
    df = pd.read_csv(csv_string, sep=",")
    if verbose:
        print("Dataset:")
        print(df)
    return df


@typechecked
def query_dataset(
    dataset_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> pd.DataFrame:
    """
    # Query dataset

    Query a dataset that exists on the `twinLab` cloud by printing summary statistics.

    ## Arguments

    - `dataset_id`: `str`; name of dataset on S3 (same as the uploaded file name)
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `pandas.DataFrame` containing summary statistics for the dataset.

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    df = tl.query_dataset("my_dataset")
    print(df)
    ```
    """
    response = api.summarise_dataset(dataset_id, verbose=debug)
    csv_string = _get_value_from_body("dataset_summary", response)
    csv_string = io.StringIO(csv_string)
    df = pd.read_csv(csv_string, index_col=0, sep=",")
    if verbose:
        print("Dataset summary:")
        print(df)
    return df


@typechecked
def delete_dataset(
    dataset_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> None:
    """
    # Delete dataset

    Delete a dataset from the `twinLab` cloud.

    ## Arguments

    - `dataset_id`: `str`; name of dataset to delete from the cloud
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    tl.delete_dataset("my_dataset")
    ```
    """
    response = api.delete_dataset(dataset_id, verbose=debug)
    if verbose:
        message = _get_message(response)
        print(message)


###  ###

### Campaign functions ###


@typechecked
def train_campaign(
    filepath_or_params: Union[str, dict],
    campaign_id: str,
    ping_time: Optional[float] = 1.0,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
) -> None:
    """
    # Train campaign

    Train a campaign in the `twinLab` cloud.

    ## Arguments

    - `filepath_or_params`: `str`, `dict`, Union; filepath to local json or parameters dictionary for training
    - `campaign_id`: `str`, name for the final trained campaign
    **Warning:** If the `campaign_id` already exists for the current cloud account, it will be overwritten by the
    newly trained campaign
    - `ping_time`: `float`, Optional, time between pings to the server to check if the job is complete [s]
    - `processor`: `str`, Optional, processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    The parameters retrieved from the first argument are divided into 2 different sets of parameters, one for
    setting up the campaign and the other for training the campaign.

    Parameters to setup the campaign(used during initialization of a Campaign class object):
    - `dataset_id`: `str`, dataset_id of the dataset as stored in the cloud
    - `inputs`: `list`, a list of strings referring to the columns in the
                Pandas DataFrame that will be used as input parameters
    - `outputs`: `list`, a list of strings referring to the columns in the
                Pandas DataFrame that will be used as output parameters
    - `estimator`: `str`, Optional, The type of estimator used in the pipeline
                ("gaussian_process_regression" or "gradient_boosting_regression")
    - `estimator_kwargs`: `dict`, Optional, keywords passed to the underlying estimator
                The estimator_kwargs dictionary for "gaussian_process_regression" allows the
                following keywords:
                `detrend`: `bool`, Optional, specifies whther to linear detrend the output
                        data before estimator fitting, default is False
                `device`: `str`, Optional, specifies whether to fit the estimator using
                        "cpu" or "gpu", default is "cpu"
    - `decompose_input`: `bool`, Optional, specifies whether the input parameters
                should be decomposed
    - `input_explained_variance`: `float`, Optional, specifies how much of the
                variance should be explained after the truncation of the SVD
                (Singular Value Decomposition) for functional input
    - `decompose_output`: `bool`, Optional, specifies whether the output parameters
                should be decomposed
    - `output_explained_variance`: `float`, Optional, specifies how much of the
                variance should be explained after the truncation of the SVD
                (Singular Value Decomposition) for functional output

    Parameters to train the campaign(used when fit() function is called using a Campaign class object for training):
    - `train_test_ratio`: `float`, Optional, specifies the ratio of training samples in
            the dataset
    - `model_selection`: `bool`, Optional, whether to run model selection
    - `model_selection_kwargs`: `dict`, Optional, keywords passed to the model
            selection process
            The model_selection_kwargs dictionary for "gaussian_process_regression" allows the
            following keywords:
            `seed`: `int`, Optional, specifies the seed for the random number genrator for every
                trial of the model selection process
            `evaluation_metric`: `str`, Optional, specifies the evaluation metric used to score
                different configuration during the model selection process, can be "BIC" or "MSLL",
                default is "MSLL"
            `val_ratio`: `float`, Optional, specifies the percentage of random validation data
                allocated to to compute the "BIC" metric, default is 0.2
            `base_kernels`: Set[str], Optional, specifies the list of kernels to use for
                Compositional Kernel Search, can be "all", "restricted" or Set[str] object
                Set of available kernels are ["LIN", "M12", "M32", "M52", "PER", "RBF", "RQF"],
                default is "restricted" and uses ["LIN", "M32", "M52", "PER", "RBF"]
            `depth`: `int`, Optional, specifies the number of base kernels to be combined in
                the Compositional Kernel Search, depth=3 means the resulting kernel may be
                composed from three base kernels, e.g. "(LIN+PER)*RBF" or "(M12*RBF)+RQF",
                default is 1
            `beam`: `int`, Optional, specifies the beam width of the Compositional Kernel Search
                algorithm, beam=1 is greedy search, beam=None performs breadth-first search and
                beam>1 perfroms beam search with the specified beam value, default is None
            `resources_per_trial`: `dict`, Optional, The amount of CPU and GPU resources allocated
                to each trial of model selection, default is {"cpu": 1, "gpu": 0}
    - `seed`: `int`, Optional, specifies the seed for the random number generator

    ## Example

    Train using a local `json` parameters file:

    ```python
    import twinlab as tl

    tl.train_campaign("path/to/params.json", "my_campaign")
    ```

    Train via a `python` dictionary:

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    ```
    """
    if type(filepath_or_params) is dict:
        params = filepath_or_params
    elif type(filepath_or_params) is str:
        filepath = filepath_or_params
        params = json.load(open(filepath))
    else:
        print("Type:", type(filepath_or_params))
        raise ValueError("filepath_or_params must be either a string or a dictionary")
    params = utils.coerce_params_dict(params)
    params_str = json.dumps(params)
    response = api.train_model(
        campaign_id, params_str, processor=processor, verbose=debug
    )
    if verbose:
        message = _get_message(response)
        print(message)

    # Wait for job to complete
    complete = False
    while not complete:
        status = _status_campaign(campaign_id, verbose=False, debug=debug)
        complete = _get_value_from_body("job_complete", status)
        time.sleep(ping_time)


@typechecked
def list_campaigns(
    verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> list:
    """
    # List campaigns

    List campaigns that have been completed to the `twinLab` cloud.

    ## Arguments

    - `verbose`: `bool`, Optional,determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - A `list` of `str` campaign ids

    ## Example

    ```python
    import twinlab as tl

    campaigns = tl.list_campaigns()
    print(campaigns)
    ```
    """
    response = api.list_models(verbose=debug)
    campaigns = _get_value_from_body("models", response)
    if verbose:
        print("Trained models:")
        pprint(campaigns, compact=True, sort_dicts=False)
    return campaigns


@typechecked
def view_campaign(
    campaign_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> dict:
    """
    # View campaign

    View a campaign that exists on the twinLab cloud.

    ## Arguments

    - `campaign_id`: `str`; name for the model when saved to the twinLab cloud
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `dict` containing the campaign training parameters.

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    params = tl.view_campaign("my_campaign")
    print(params)
    ```
    """
    response = api.view_model(campaign_id, verbose=debug)
    model_parameters = response
    if verbose:
        print("Campaign summary:")
        pprint(model_parameters, compact=True, sort_dicts=False)
    return model_parameters


@typechecked
def query_campaign(
    campaign_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> dict:
    """
    # Query campaign

    Get summary statistics for a pre-trained campaign in the `twinLab` cloud.

    ## Arguments

    - `campaign_id`: `str`; name of trained campaign to query
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `dict` containing summary statistics for the pre-trained campaign.

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    info = tl.query_campaign("my_campaign")
    print(info)
    ```
    """
    response = api.summarise_model(campaign_id, verbose=debug)
    summary = response
    if verbose:
        print("Model summary:")
        pprint(summary, compact=True, sort_dicts=False)
    return summary


@typechecked
def predict_campaign(
    filepath_or_df: Union[str, pd.DataFrame],
    campaign_id: str,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    # Predict campaign

    Make predictions from a pre-trained model that exists on the `twinLab` cloud.

    ## Arguments

    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation
        or `pandas` dataframe
    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions
    - `processor`: `str`, Optional, processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.

    ## Returns

    - `tuple` containing:
        - `df_mean`: `pandas.DataFrame` containing mean predictions
        - `df_std`: `pandas.DataFrame` containing standard deviation predictions

    ## Example

    Using a local file:
    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    filepath = "path/to/data.csv" # Local
    campaign_id = 'my_campaign" # Pre-trained
    df_mean, df_std = tl.predict_campaign(filepath, campaign_id)
    print(df_mean)
    print(df_std)
    ```

    Using a `pandas` dataframe:
    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    df = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
    tl.predict_campaign(df, "my_campaign")
    ```
    """

    csv = _use_campaign(
        campaign_id,
        method="predict",
        filepath_or_df=filepath_or_df,
        processor=processor,
        verbose=verbose,
        debug=debug,
    )
    df = pd.read_csv(csv, sep=",")
    n = len(df.columns)
    df_mean, df_std = df.iloc[:, : n // 2], df.iloc[:, n // 2 :]
    df_std.columns = df_std.columns.str.removesuffix(" [std_dev]")
    if verbose:
        print("Mean predictions:")
        print(df_mean)
        print("Standard deviation predictions:")
        print(df_std)

    return df_mean, df_std


@typechecked
def sample_campaign(
    filepath_or_df: Union[str, pd.DataFrame],
    campaign_id: str,
    num_samples: int,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
    **kwargs,
) -> pd.DataFrame:
    """
    # Sample campaign

    Draw samples from a pre-trained campaign that exists on the `twinLab` cloud.

    ## Arguments

    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation
        or `pandas` dataframe
    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions
    - `num_samples`: `int`; number of samples to draw for each row of the evaluation data
    - `processor`: `str`, Optional, processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.

    ## Returns

    - `DataFrame` with the sampled values

    ## Example

    Using a local file:
    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    filepath = "path/to/data.csv" # Local
    n = 10
    df_mean, df_std = tl.sample_campaign(filepath, "my_campaign", n)
    print(df_mean)
    print(df_std)
    ```

    Using a `pandas` dataframe:
    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    df = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
    n = 10
    tl.sample_campaign(df, "my_campaign", n)
    ```
    """

    csv = _use_campaign(
        campaign_id,
        method="sample",
        filepath_or_df=filepath_or_df,
        num_samples=num_samples,
        processor=processor,
        verbose=verbose,
        debug=debug,
        **kwargs,
    )
    df = pd.read_csv(csv, header=[0, 1], sep=",")
    if verbose:
        print("Samples:")
        print(df)
    return df


@typechecked
def active_learn_campaign(
    campaign_id: str,
    num_points: int,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
    **kwargs,
) -> pd.DataFrame:
    """
    # Active learn campaign

    Draw new candidate data points via active learning from a pre-trained campaign
    that exists on the `twinLab` cloud.

    ## Arguments
    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions
    - `num_points`: `int`; number of samples to draw for each row of the evaluation data
    - `processor`: `str`, Optional, processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Returns

    - `Dataframe` containing the recommended sample locations

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    n = 10
    df = tl.active_learn_campaign("my_campaign", n)
    print(df)
    ```
    """

    csv = _use_campaign(
        campaign_id,
        method="get_candidate_points",
        acq_func="qNIPV",
        num_points=num_points,
        processor=processor,
        verbose=verbose,
        debug=debug,
        **kwargs,
    )
    df = pd.read_csv(csv, sep=",")
    if verbose:
        print("Candidate points:")
        print(df)
    return df


@typechecked
def optimise_campaign(
    campaign_id: str,
    num_points: int,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
    **kwargs,
) -> pd.DataFrame:
    """
    # Optimise campaign

    Draw new candidate data points by optimizing for "qEI" (Monte Carlo Expected Improvement)
    acquisition function from a pre-trained campaign that exists on the `twinLab` cloud.

    ## Arguments
    - `campaign_id`: `str`, name of pre-trained campaign to use for predictions
    - `num_points`: `int`, number of samples to draw for each row of the evaluation data
    - `processor`: `str`, Optional, processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server
    - `acq_kwargs`: `dict`, Optional, specifies the keyword arguments to modify the behavior of
        the acquisition function. This dictionary currently allows only one keyword argument
        - `weights`: `list[float]`, specifies the weightage for different objectives to be
            optimised in a mulit-objective optimisation scenario. By default all weights are equal.
            e.g for a problem with 2 outputs if weights are as follows [1, 0.5], this indicates
            that we focus on maximising the first output dimension twice as much as
            the second output dimension.

    ## Returns

    - `Dataframe` containing the recommended sample locations

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [0.0, 0.25, 0.75, 1.0], 'y': [-1.60856306, -0.27526546, -0.34670215, -1.65062947]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    n = 1
    df = tl.optimise_campaign("my_campaign", n)
    print(df)
    ```
    """

    csv = _use_campaign(
        campaign_id,
        method="get_candidate_points",
        acq_func="qEI",
        num_points=num_points,
        processor=processor,
        verbose=verbose,
        debug=debug,
        **kwargs,
    )
    df = pd.read_csv(csv, sep=",")
    if verbose:
        print("Candidate points:")
        print(df)
    return df


@typechecked
def solve_inverse_campaign(
    campaign_id: str,
    filepath_or_df: Union[str, pd.DataFrame],
    filepath_or_df_std: Union[str, pd.DataFrame],
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = False,
    debug: Optional[bool] = False,
    **kwargs,
) -> pd.DataFrame:
    """
    # Inverse modelling on campaign

    Given a set of observations, inverse modelling finds the model that would best suit the data.

    ## Arguments
    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions
    - `data_csv`: `DataFrame`; a DataFrame of observations
    - `data_std_csv` : `DataFrame`; a DataFrame of errors on the observations
    - `processor`: `str`; processor to use for sampling ("cpu"; "gpu")
    - `verbose`: `bool` determining level of information returned to the user
    - `debug`: `bool` determining level of information logged on the server

    ## Returns

    - `Dataframe` containing the recommended model statistics

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    data_csv = pd.DataFrame({'y': [1]})
    data_std_csv = pd.DataFrame({'y': [0.498]})
    df = tl.solve_inverse_campaign("my_campaign", data_csv, data_std_csv)
    print(df)
    ```
    """
    csv = _use_campaign(
        campaign_id,
        method="solve_inverse",
        filepath_or_df=filepath_or_df,
        filepath_or_df_std=filepath_or_df_std,
        processor=processor,
        verbose=verbose,
        debug=debug,
        **kwargs,
    )

    df = pd.read_csv(csv, sep=",")
    if verbose:
        print("Inverse model statistics:")
        print(df)
    return df


@typechecked
def score_campaign(
    campaign_id: str,
    combined_score: Optional[bool] = False,
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = True,
    debug: Optional[bool] = False,
) -> list:
    """
    # Quantify the performance of your trained model with a model score.

    ## Arguments
    - `combined_score`: `bool` determining whether to average scores across dimensions. If False, will return a numpy array even if only one dimension.

    ### Returns
    - `List` containing the trained model score.

    ### Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
    tl.predict_campaign(df, "my_campaign")
    tl.score_campaign(df, combined_score=True)
    ```
    """

    list = _use_campaign(
        campaign_id,
        method="score",
        combined_score=combined_score,
        processor=processor,
        verbose=verbose,
        debug=debug,
    )
    if verbose:
        print("Campaign Score:")
        print(list)
    return list


@typechecked
def get_calibration_curve_campaign(
    campaign_id: str,
    type: Optional[str] = "quantile",
    processor: Optional[str] = "cpu",
    verbose: Optional[bool] = True,
    debug: Optional[bool] = False,
) -> list:
    """
    # Quantify the performance of your trained model with a calibration curve.

    ## Arguments
    - `type`: `str` determining whether to use "quantiile" or "interval" for the model calibration error.

    ### Returns
    - `List` containing the data for the calibration curve.

    ### Example

    ```pyt
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
    tl.train_campaign(df, "my_campaign")
    tl.get_calibration_curve(df, type="quantile")

    # Plot the calibration curve
    fraction_observed = tl.get_calibration_curve(type="quantile")
    fraction_expected = np.linspace(0,1,fraction_observed.shape[0])

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title("Calibration curve")
    ax.set_xlabel("Expected coverage")
    ax.set_ylabel("Observed coverage")

    plt.plot(np.linspace(0, 1, 100), fraction_observed)
    plt.plot(np.linspace(0, 1, 100), np.linspace(0, 1, 100), "--")
    plt.show()
    ```
    """

    list = _use_campaign(
        campaign_id,
        method="get_calibration_curve",
        type=type,
        processor=processor,
        verbose=verbose,
        debug=debug,
    )
    if verbose:
        print("Calibration curve information:")
        print(list)
    return list


@typechecked
def delete_campaign(
    campaign_id: str, verbose: Optional[bool] = False, debug: Optional[bool] = False
) -> None:
    """
    # Delete campaign

    Delete campaign from the `twinLab` cloud.

    ## Arguments

    - `campaign_id`: `str`; name of trained campaign to delete from the cloud
    - `verbose`: `bool`, Optional, determining level of information returned to the user
    - `debug`: `bool`, Optional, determining level of information logged on the server

    ## Example

    ```python
    import pandas as pd
    import twinlab as tl

    df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
    tl.upload_dataset(df, "my_dataset")
    params = {
        "dataset_id": "my_dataset",
        "inputs": ["X"],
        "outputs": ["y"],
    }
    tl.train_campaign(params, "my_campaign")
    tl.delete_campaign("my_campaign")
    ```
    """
    response = api.delete_model(campaign_id, verbose=debug)
    if verbose:
        message = _get_message(response)
        print(message)


### ###
