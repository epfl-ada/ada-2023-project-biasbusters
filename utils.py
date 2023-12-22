import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import numpy as np
import dataset
import statsmodels as sts
import matplotlib.pyplot as plt
import seaborn as sns
import communities
import plots
import json

def one_hot_encode_multilabel(df, column_name):
    """
    Applies one-hot encoding to a column with multilabel classes in a DataFrame.

    :param df: pandas DataFrame containing the column to encode.
    :param column_name: string name of the column that contains multilabel classes.
    :return: DataFrame with original column replaced by one-hot encoded columns.
    """
    df = df.reset_index(drop=True)
    mlb = MultiLabelBinarizer()
    
    encoded_data = mlb.fit_transform(df[column_name])
    encoded_df = pd.DataFrame(encoded_data, columns=[f'{column_name}_{class_}' for class_ in mlb.classes_])
    
    df = df.drop(column_name, axis=1).join(encoded_df)
    
    return df


def fit_regression_model(df, feature_columns, target_feature, print_summary=False):
    """
    Fits a regression model using one-hot encoding for categorical features with multilabel classes
    and standardizes numerical features.
    
    :param df: pandas DataFrame containing the data.
    :param feature_columns: list of feature column names to include in the model.
    :param target_feature: the name of the target feature for regression.
    """
    # Create a copy of the DataFrame to avoid modifying the original one
    df_copy = df.copy()
    df_copy = df_copy[df_copy[feature_columns + [target_feature]].notna().all(axis=1)]
    
    # Initialize the StandardScaler
    scaler = StandardScaler()
    
    # Process each feature column
    formula_parts = []
    for column in feature_columns:
        # Check if the column is categorical
        if df_copy[column].dtype == 'O' or df_copy[column].dtype.name == 'category':
            # Apply one-hot encoding to the column
            df_copy = one_hot_encode_multilabel(df_copy, column)
            encoded_columns = [col for col in df_copy.columns if col.startswith(f'{column}_')]
            formula_parts.extend([f'C({col})' for col in encoded_columns])
        else:
            # For numerical columns, apply standardization
            df_copy[column] = scaler.fit_transform(df_copy[[column]])
            formula_parts.append(column)
    
    formula = f'{target_feature} ~ ' + ' + '.join(formula_parts)
    
    mod = smf.ols(formula=formula, data=df_copy)
    res = mod.fit()
    
    # Extract model parameters for plotting
    variables = res.params.index
    coefficients = res.params.values
    p_values = res.pvalues
    standard_errors = res.bse.values
    
    # Sort them all by the absolute value of coefficients for plotting
    l1, l2, l3, l4 = zip(*sorted(zip(coefficients[1:], variables[1:], standard_errors[1:], p_values[1:])))
    
    plt.figure(figsize=(12, 2 + int(len(l1)/4)))
    plt.errorbar(l1, np.array(range(len(l1))), xerr=2*np.array(l3), linewidth=1,
                 linestyle='none', marker='o', markersize=3,
                 markerfacecolor='black', markeredgecolor='black', capsize=5)
    
    plt.vlines(0, 0, len(l1), linestyle='--')
    plt.title(f'Coefficients of regression model for target "{target_feature}" with ±2se intervals; p-values less than 0.05 are printed')
    plt.xlabel('Coefficient value in the model')
    
    for i, (coef, p) in enumerate(zip(l1, l4)):
        if p < 0.05:  # Only annotate significant p-values
            plt.text(coef, i, f'p={p:.2e}', fontsize=8, verticalalignment='bottom')
    
    plt.yticks(range(len(l2)), l2)
    plt.show()

    if print_summary:
        print(res.summary())


def plot_regression(df, feature_column, target_feature):
    df_copy = df.copy()
    df_copy = df_copy[df_copy[[feature_column, target_feature]].notna().all(axis=1)]
    fig, ax = plt.subplots(figsize=(10, 6))
    if df_copy[feature_column].dtype == 'O' or df_copy[feature_column].dtype.name == 'category':
        df_copy = one_hot_encode_multilabel(df_copy, feature_column)
        encoded_columns = [col for col in df_copy.columns if col.startswith(f'{feature_column}_')]
        for i, column in enumerate(encoded_columns):  # exclude the target column
            # Filter the target feature where the categorical feature equals 1
            data_to_plot = df_copy[df_copy[column] == 1][target_feature]
            # Plot the boxplot for the current category
            ax.boxplot(data_to_plot, positions=[i], widths=0.5)
        
        ax.boxplot(df_copy[target_feature], positions=[i+1], widths=0.5)
        
        # Setting the x-axis labels to the encoded column names
        ax.set_xticklabels(
            [x.replace(f'{feature_column}_', '') for x in encoded_columns] + ['overall_distribution'],
            rotation=45, ha='right')
        
        # Setting the y-axis label
        ax.set_ylabel(target_feature)
        
        # Adding a title to the plot
        ax.set_title(f'Boxplots of {target_feature} for {feature_column}')
    else:
        sns.regplot(
            df_copy, x=feature_column, y=target_feature, ci=95, marker='.', 
            scatter_kws={'alpha': 0.1, 'color': 'grey'})


