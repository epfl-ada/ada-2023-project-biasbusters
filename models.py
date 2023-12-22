from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.metrics import mean_squared_error, make_scorer, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

def evaluate_LinearRegression(overall_engagement, column):
    # We need to remove any rows with zeros since log(0) is undefined
    filtered_data = overall_engagement[(overall_engagement['num_votes'] > 0) & (overall_engagement[column] > 0)]

    # Log-transform the relevant columns
    X = np.log(filtered_data[['num_votes']])
    y = np.log(filtered_data[column])

    # Define the model
    model = LinearRegression()

    # Define the K-fold cross validator
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Define the scoring function
    mse_scorer = make_scorer(mean_squared_error)

    # Perform K-fold cross-validation and compute the MSE
    mse_scores = cross_val_score(model, X, y, cv=kf, scoring=mse_scorer)

    # Compute the average MSE
    average_mse = np.mean(mse_scores)

    # Calculate the exponentiated version of the RMSE (RMSLE - Root Mean Squared Logarithmic Error)
    rmsle = np.sqrt(average_mse)
    multiplicative_error = np.exp(rmsle)

    # Fit model on training data and conduct prediction + evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test data
    y_pred = model.predict(X_test)

    # Calculate the R-squared value
    r2 = r2_score(y_test, y_pred)
    exp_r2 = r2_score(np.exp(y_test), np.exp(y_pred))
    
    print(f'Prediction: {column}')
    print('- - - - - - - - - - - - - - - - -')
    print(f'Average MSE: {average_mse}')
    print(f'Exponentiated RMSE: {multiplicative_error}')
    print(f'R-squared (log space): {r2}')
    print(f'R-squared (original scale): {exp_r2}')
    print()



def evaluate_KNN(overall_engagement, column, n_neighbors=5):
    # We need to remove any rows with zeros since log(0) is undefined
    filtered_data = overall_engagement[(overall_engagement['num_votes'] > 0) & (overall_engagement[column] > 0)]

    # Log-transform the relevant columns
    X = np.log(filtered_data[['num_votes']])
    y = np.log(filtered_data[column])

    # Define the model pipeline: StandardScaler + KNN
    # StandardScaler is used to normalize the feature(s) because KNN is distance-based
    model = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=n_neighbors))

    # Define the K-fold cross validator
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Define the scoring function
    mse_scorer = make_scorer(mean_squared_error)

    # Perform K-fold cross-validation and compute the MSE
    mse_scores = cross_val_score(model, X, y, cv=kf, scoring=mse_scorer)

    # Compute the average MSE
    average_mse = np.mean(mse_scores)

    # Calculate the exponentiated version of the RMSE (RMSLE - Root Mean Squared Logarithmic Error)
    rmsle = np.sqrt(average_mse)
    multiplicative_error = np.exp(rmsle)

    # Fit model on training data and conduct prediction + evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test data
    y_pred = model.predict(X_test)

    # Calculate the R-squared value
    r2 = r2_score(y_test, y_pred)
    exp_r2 = r2_score(np.exp(y_test), np.exp(y_pred))
    
    return {'k_value': n_neighbors, 'average_mse': average_mse, 'multiplicative_error': multiplicative_error, 'r2': r2, 'exp_r2': exp_r2}


def evaluate_KNN_range(overall_engagement, column, range_k=np.linspace(1,1000, 100)):
    results = []
    
    for k in range_k:
        results.append(evaluate_KNN(overall_engagement, column, int(k)))
        
    return pd.DataFrame(results)
    
