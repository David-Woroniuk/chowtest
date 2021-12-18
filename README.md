# Chow Test

[![Downloads](https://pepy.tech/badge/chowtest)](https://pepy.tech/project/chowtest) [![Downloads](https://pepy.tech/badge/chowtest/month)](https://pepy.tech/project/chowtest)

This project provides an implementation of the Chow break test.

The Chow test was initially developed by Gregory Chow in 1960 to test whether one regression or two or more regressions best characterise the data. As such, the Chow test is capable of detecting "structural breaks" within time-series. Additional information can be obtained from:

[Chow, Gregory C. "Tests of equality between sets of coefficients in two linear regressions." Econometrica: Journal of the Econometric Society (1960): 591-605.][abc]

[Toyoda, Toshihisa. "Use of the Chow test under heteroscedasticity." Econometrica: Journal of the Econometric Society (1974): 601-608.][def]

This implementation supports simple linear models, and finding breaks where k = 2.

### Installation

This module requires Python 3.0+ to run. The module can can be imported by:
```python
pip install chowtest
from chow_test import chow_test
```

### Input Arguments

The required input arguments are listed below:

| **Argument**       | **Description**                                                                        | **Data Type**             |
|--------------------|----------------------------------------------------------------------------------------|---------------------------|
| ```X_series```     | The series or series' denoting the X variables.                                        | pd.Series or pd.DataFrame |
| ```y_series```     | The series denoting the y variable                                                     | pd.Series                 |
| ```last_index```   | The final index value to be included before the data split.                            | int                       |
| ```first_index```  | The first index value to be included after the index split.                            | int                       |
| ```significance``` | The significance level against which the p-value is assessed. Can be 0.1, 0.05 or 0.01 | float                     |

**Note: The pd.reset_index() function can be invoked in order to obtain an integer index.**


   [abc]: <https://www.jstor.org/stable/1910133?casa_token=5boKBERpursAAAAA%3ABCYkFnXnHBbM0c4thWh5rySthktrt5nLlWE1nwjKbHlwmpH5fTdQoAMzgv82adNdzRzoZBe01scMcO_lDf-mjemPUsRtOmbhXkCsuoc4tUXyWrlJi59Z3Q&seq=1#metadata_info_tab_contents>
   [def]: <https://www.jstor.org/stable/1911796?casa_token=4WNFjhaMRG8AAAAA%3AKzirHep7m9iaXUTF-q90Z-ZyHVHeolvk_cNUlOuZw2bQF4z4UmAvgvejjPlC9woHSTdzBx5PVFSHP1aFhbnvWve1aMPYGO90MkbUTAgQBk-wo6HzVLjLIw&seq=1#metadata_info_tab_contents>
