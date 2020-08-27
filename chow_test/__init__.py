# -*- coding: utf-8 -*-

from sklearn.linear_model import LinearRegression as lr
from scipy.stats import f
import pandas as pd
import numpy as np

def chowtest(X, y, last_index_in_model_1, first_index_in_model_2, significance_level):
  '''
  This function conducts a Chow Test, returning the Chow Statistic and associated p-value.

  Inputs:   X: independent variable(s) (Pandas DataFrame Column(s)).
            y: dependent variable (Pandas DataFrame Column (subset)).
            last_index_in_model_1: index of final point in prior to assumed structural break (index value).
            first_index_in_model_2: index of the first point following the assumed structural break (index value).
            significance_level: the significance level for hypothesis testing (float).


  Outputs:  Chow_Stat: Chow test statistic (float).
            p_value:  p-value associated with Chow test statistic.
            result: a tuple containing the Chow_Stat and associated p-value.

  References:

  1) Chow, Gregory C. "Tests of equality between sets of coefficients in two linear regressions." 
    Econometrica: Journal of the Econometric Society (1960): 591-605.
  
  '''
  
  
  
  def linear_residuals(X, y):   
    '''
    This sub-function is obtains performance information relating to a linear regression (sklearn).

    Inputs:   X: independent variable(s) (Pandas Series' or Pandas DataFrame Column(s)).
              y: dependent variable (Pandas Series or Pandas DataFrame Column).

    Outputs:  summary_result: DataFrame containing error information.
  
    '''    
    # fits the linear model:
    model = lr().fit(X, y)
    
    # creates a dataframe with the predicted y in a column called y_hat:
    summary_result = pd.DataFrame(columns = ['y_hat'])
    yhat_list = [float(i[0]) for i in np.ndarray.tolist(model.predict(X))]
    summary_result['y_hat'] = yhat_list  
    # saves the actual y values in the y_actual column:
    summary_result['y_actual'] = y.values
    # calculates the residuals:
    summary_result['residuals'] = (summary_result.y_actual - summary_result.y_hat)
    # squares the residuals:
    summary_result['residuals_sq'] = (summary_result.residuals ** 2)
    return summary_result
  

  def calculate_RSS(X, y):
    '''
    This sub-function returns the sum of squared residuals (errors).

    Inputs:   X: independent variable(s) (Pandas Series' or Pandas DataFrame Column(s)).
              y: dependent variable (Pandas Series or Pandas DataFrame Column).

    Outputs:  rss: sum of squared residuals (float).
  
    ''' 

    # calls the linear_residual function
    resid_data = linear_residuals(X, y)
    # calculates the sum of squared residuals
    rss = resid_data.residuals_sq.sum()
    return rss


  # calculate RSS for the entire dataset:
  rss_pooled = calculate_RSS(X, y)
    
  # splits the X and y dataframes by input arguments, calculates seperate RSS values:
  X1 = X.loc[:last_index_in_model_1]
  y1 = y.loc[:last_index_in_model_1]
  rss1 = calculate_RSS(X1, y1)
      
  X2 = X.loc[first_index_in_model_2:]
  y2 = y.loc[first_index_in_model_2:]
  rss2 = calculate_RSS(X2, y2)
    
  # determines number of independent variables, plus 1 for the constant in the regression:
  k = X.shape[1] + 1
  # determines the number of observations in the first period:
  N1 = X1.shape[0]
  # determines the number of observations in the second period:
  N2 = X2.shape[0]

  # calculates the numerator of the Chow Statistic:
  numerator = (rss_pooled - (rss1 + rss2)) / k
  # calculates the denominator of the Chow Statistic:
  denominator = (rss1 + rss2) / (N1 + N2 - 2 * k)
    
  # calculates the Chow Statistic:
  Chow_Stat = numerator / denominator
    
  # Chow statistics are distributed in a F-distribution with k and N1 + N2 - 2k degrees of freedom.

  # calculates the p-value by subtracting 1 by the cumulative probability at the Chow
  # statistic from an F-distribution with k and N1 + N2 - 2k degrees of freedom:
  p_value = 1 - f.cdf(Chow_Stat, dfn = 5, dfd = (N1 + N2 - 2 * k))

  print('*' * 100)
  if p_value <= significance_level:
    print("Reject the null hypothesis of equality of regression coefficients in the 2 periods.")
  elif p_value > significance_level:
    print("Fail to reject the null hypothesis of equality of regression coefficients in the 2 periods.")
  print('*' * 100)
  print('Chow Statistic:',Chow_Stat, 'p value:',p_value.round(5))
  print('*' * 100)
       
  # saves the Chow_State and p_value in a tuple:
  result = (Chow_Stat, p_value)
    
  # returns the result tuple:
  return result