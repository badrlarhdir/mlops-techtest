import numpy as np
from cpsc2019_score import load_ans, score


# Define the function to perform model evaluation
def perform_model_evaluation() -> dict:
    """
    Perform model evaluation and calculate evaluation metrics.

    This function loads reference data and model predictions, calculates
    R Detection accuracy (rec_acc) and heart rate accuracy (hr_acc), and
    returns the evaluation results as a dictionary.

    Returns:
        dict: A dictionary containing evaluation results including:
            - tot_file_number: Total number of files processed.
            - rec_acc: Recognition accuracy.
            - hr_acc: Heart rate accuracy.
    """
    # Define the sampling frequency and threshold for the CPSC2019_challenge function
    FS = 500
    THR = 0.075

    DATA_PATH = "./data/"
    RPOS_PATH = "./ref/"

    R_ref, HR_ref, R_ans, HR_ans = load_ans(DATA_PATH, RPOS_PATH, FS)
    rec_acc, hr_acc = score(R_ref, HR_ref, R_ans, HR_ans, FS, THR)

    # Return the evaluation results as a dictionary
    evaluation_results = {
        "tot_file_number": np.shape(HR_ans)[0],
        "rec_acc": rec_acc,
        "hr_acc": hr_acc,
    }

    return evaluation_results
