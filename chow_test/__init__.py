from sklearn.linear_model import LinearRegression as Lr
from scipy.stats import f
import pandas as pd


def _calculate_rss(X_series: pd.DataFrame, y_series: pd.Series):
    """
    This function returns the sum of squared residuals. The function firstly checks that the input
    arguments are of the correct type, followed by fitting the linear regression model on the X_series
    and y_series. The predicted values are then placed into the 'y_hat' column, after which the residuals
    are calculated. Finally, the sum of squared residuals (rss) is calculated.

    :param: X_series: the series or set of series denoting the X variable. (pd.DataFrame)
    :param: y_series: the series denoting the y variable. (pd.Series)
    :return: summary_result: a Pandas DataFrame summarising the result. (pd.DataFrame)
    :return: rss: the sum of squared errors. (float)
    """
    if not isinstance(X_series, pd.DataFrame):
        raise TypeError("The 'X_series' argument should be a Pandas DataFrame.")
    if not isinstance(y_series, pd.Series):
        raise TypeError("The 'y_series' argument must be a Pandas Series.")
    model = Lr().fit(X_series, y_series)
    summary_result = pd.DataFrame()
    summary_result['y_hat'] = list(model.predict(X_series))
    summary_result['y_actual'] = y_series.values
    summary_result['residuals'] = summary_result['y_actual'] - summary_result['y_hat']
    summary_result['residuals_sq'] = (summary_result['y_actual'] - summary_result['y_hat']) ** 2
    rss = float(summary_result['residuals_sq'].sum())
    return summary_result, rss


def _data_preparation(X_series: (pd.Series, pd.DataFrame), y_series: pd.Series, last_index: int, first_index: int):
    """
    This function prepares the data by splitting the X_series and y_series into two subsets. The function firstly checks
    that the input arguments are of the expected types, followed by splitting the X_series and y_series into X_series_one,
    X_series_two, y_series_one and y_series_two respectively. The function then returns the sub-series'.

    :param: y_series: the series denoting the y variable. (pd.Series)
    :param: X_series: the series or set of series denoting the X variable. (pd.Series, pd.DataFrame)
    :param: last_index: the final index value to be included before the data split. (int)
    :param: first_index: the first index value to be included after the data split. (int)
    :return: X_series_one: the Pandas DataFrame containing the pre-split X data. (pd.DataFrame)
    :return: X_series_two: the Pandas DataFrame containing the post-split X data. (pd.DataFrame)
    :return: y_series_one: the Pandas Series containing the pre-split y data. (pd.Series)
    :return: y_series_two: the Pandas Series containing the post_split y data. (pd.Series)
    """
    if not isinstance(y_series, pd.Series):
        raise TypeError("The 'y_series' argument must be a Pandas Series.")
    if not isinstance(X_series, (pd.Series, pd.DataFrame)):
        raise TypeError("The 'X_series' argument must be a Pandas Series or a Pandas DataFrame.")
    if not all(isinstance(v, int) for v in [last_index, first_index]):
        raise TypeError("The 'last_index' and 'first_index' arguments must be integer types.")
    X_series_one = X_series[: last_index]
    X_series_two = X_series[first_index:]
    y_series_one = y_series[: last_index]
    y_series_two = y_series[first_index:]
    return X_series_one, X_series_two, y_series_one, y_series_two


def _calculate_chow_statistic(pooled_rss_value: (int, float), rss_one: (int, float), rss_two: (int, float),
                              k_value: int, n_one_value: int, n_two_value: int):
    """
    This function calculates the chow test statistic. Firstly the function checks that the input arguments are of the
    correct input type, followed by calculating the numerator argument for th chow test. After this, the denominator
    argument is calculated, and the chow test statistic is attempted. If this fails due to a zero division error, the
    user is warned and the value is returned as 0.

    :param: pooled_rss_value: the sum of squared errors for the whole data series. (float)
    :param: rss_one: the sum of squared errors for the first series. (float)
    :param: rss_two: the sum of squared errors for ths second series. (float)
    :param: k_value: the number of degrees of freedom. (int)
    :param: n_one_value: the length of the first series. (int)
    :param: n_two_value: the length of the second series. (int)
    :return: chow_test: the chow test statistic. (float)
    """
    if not all(isinstance(v, (float, int)) for v in [pooled_rss_value, rss_one, rss_two]):
        raise TypeError("The 'pooled_rss_value', 'rss_one' and 'rss_two' values must be either integers or floats.")
    if not all(isinstance(v, int) for v in [k_value, n_one_value, n_two_value]):
        raise TypeError("The 'k_value', 'n_one_value' and 'n_two_value' arguments must be integer types.")
    numerator = (pooled_rss_value - (rss_one + rss_two)) / k_value
    denominator = (rss_one + rss_two) / (n_one_value + n_two_value - (2 * k_value))
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0


def _determine_p_value_significance(chow_statistic: (int, float), n_one_value: int, n_two_value: int, k_value: int,
                                   significance_level: float, verbose: bool = True):
    """
    This function determines the statistical significance of the chow_statistic passed as an input argument. The
    function firstly checks that the input arguments are of the correct type, followed by defining the p-value with
    respect to the f-distribution. The p-value is subsequently assessed against the significance_level argument,
    printing the output if verbose is set to True. The chow_statistic and corresponding p-value are returned.

    :param: chow_statistic: the chow statistic for which to assess the p-value. (float)
    :param: n_one_value: the number of observations held within the first subset of data. (int)
    :param: n_two_value: the number of observations held within the second subset of data. (int)
    :param: k_value: the number of degrees of freedom. (int)
    :param: significance_level: the significance level against which the p-value is assessed. (float)
    :param: verbose: determines if progress is printed. (bool)
    :return: chow_statistic: the chow statistic for which to assess the p-value. (float)
    :return: p_value: the p-value associated with the chow statistic. (float)
    """
    if not all(isinstance(v, int) for v in [n_one_value, n_two_value, k_value]):
        raise TypeError("The 'n_one_value', 'n_two_value' and 'k_value' must be integer types.")
    if not isinstance(chow_statistic, (int, float)):
        raise TypeError("The 'chow_statistic' must be an integer or float type.")
    p_value = float(1 - f.cdf(chow_statistic, dfn=k_value, dfd=((n_one_value + n_two_value) - 2 * k_value)))
    if p_value <= significance_level and verbose:
        print("Reject the null hypothesis of equality of regression coefficients in the two periods.")
    elif p_value > significance_level and verbose:
        print("Fail to reject the null hypothesis of equality of regression coefficients in the two periods.")
    if verbose:
        print("Chow Statistic: {}, P_value: {}".format(chow_statistic, p_value))
    return chow_statistic, p_value


def chow_test(X_series: (pd.Series, pd.DataFrame), y_series: pd.Series, last_index: int, first_index: int,
              significance: float):
    """
    This function acts as the highest level of abstraction for the chow test. The function firstly checks that the
    input arguments are of the correct type, followed by calculating the sum of squared residuals for the entire data
    series, and the two sub-sets of data, as determined by the last_index and first_index arguments. The chow test is
    then computed and assessed against the significance argument. Finally, the chow_test value and p_value are returned
    from the function.

    :param: X_series: the series or set of series denoting the X variable. (pd.DataFrame)
    :param: y_series: the series denoting the y variable. (pd.Series)
    :param: last_index: the final index value to be included before the data split. (int)
    :param: first_index: the first index value to be included after the data split. (int)
    :param: significance_level: the significance level against which the p-value is assessed. (float)
    :return: chow_value: the chow test output value. (float)
    :return: p_value: the associated p-value for the chow test. (float)
    """
    if not isinstance(y_series, pd.Series):
        raise TypeError("The 'y_series' argument must be a Pandas Series.")
    if not isinstance(X_series, (pd.Series, pd.DataFrame)):
        raise TypeError("The 'X_series' argument must be a Pandas Series or a Pandas DataFrame.")
    if not all(isinstance(v, int)for v in [last_index, first_index]):
        raise TypeError("The 'last_index' and 'first_index' arguments must be integer types.")
    if not isinstance(significance, float):
        raise TypeError("The 'significance' argument must be a float type.")
    if significance not in [0.01, 0.05, 0.1]:
        raise KeyError("The 'significance' argument must be 0.01, 0.05 or 0.1")

    if isinstance(X_series, pd.Series):
        X_series = pd.DataFrame(X_series)
    _, rss_pooled = _calculate_rss(X_series, y_series)
    X_one, X_two, y_one, y_two = _data_preparation(X_series, y_series, last_index, first_index)
    _, first_rss = _calculate_rss(X_one, y_one)
    _, second_rss = _calculate_rss(X_two, y_two)
    k = X_series.shape[1] + 1
    n_one = X_one.shape[0]
    n_two = X_two.shape[0]
    chow_value = _calculate_chow_statistic(rss_pooled, first_rss, second_rss, k, n_one, n_two)
    chow_value, p_value = _determine_p_value_significance(chow_value, n_one, n_two, k, significance)
    return chow_value, p_value


if __name__ == "__main__":
    data = [[11, 10, 9], [11,  15, 9], [12, 14, 16], [11, 10, 9], [11,  15, 9],
            [12, 14, 16], [11, 10, 9], [11,  15, 9], [12, 14, 16], [11, 10, 9],
            [11,  15, 9], [12, 14, 16], [11, 10, 9], [11,  15, 9], [12, 14, 16]]
    new_data = pd.DataFrame(data, columns=["A", "B", "C"])
    chow, p_val = chow_test(new_data["B"], new_data["A"], 8, 9, 0.01)
