You must solve, using a Jupyter notebook, the following machine learning engineering competition from the Kaggle website:

**Competition Details**
- **name:** {competition_title}
- **description:** {overview}
- **evaluation metric:** {evaluation_metric}
- **submission format:** {submission_format}
- **target column:** {target_column}

**Instructions**
The training data is in a file named `train.csv` and the test data is in a file named `test.csv`.
You must use the training data to train a machine learning model and then use the test data to create a submission file named `submission.csv`, predicting the target column while employing the correct submission format. The test set does not contain the column `{target_column}`.
Get the best score possible, but make sure a `submission.csv` file is generated within the time limit of 60 minutes; you may update the file with better predictions.

**System Specs**
- **OS:** Ubuntu 22.04 Jammy
- **CPU:** Intel Core i7-10700F @ 16x 4.8GHz
- **RAM:** 128 GiB
- **GPU:** None
- **Available packages:** numpy, pandas, xgboost, seaborn, scipy, scikit-learn, catboost, matplotlib

**Additional Instructions**
- Ensure that all code can run on the available system specs.
- Make sure to validate models with a holdout set before training on the full set.
- When processing data, always remember that the test set is missing the `{target_column}` column.
- Make sure to properly encode and decode data before training and inference.
- Check for noise in the data, including missing values and outliers.
- Always make sure the predictions are in the correct format before creating the submission file.
- Make sure the total runtime is under 60 minutes; use up to 16 CPU threads.
- Make sure to create the initial `submission.csv` file, with baseline prediction for the test set, **before** tuning hyperparameters.
