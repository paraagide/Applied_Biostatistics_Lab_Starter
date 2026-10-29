
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Python Code Generator",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 Unit I — Learning Python Through Descriptive Statistics")

st.write(
    "Select a descriptive statistic to study a complete Python program. "
    "Each program includes library imports, data, calculations, comments "
    "and instructions for displaying the result."
)

st.info(
    "The displayed Python programs are teaching examples. "
    "This page does not dynamically execute the displayed code."
)

# --------------------------------------------------
# 1. EXAMPLE DATASETS
# --------------------------------------------------

# A small dataset is easier for students to understand.
# These are illustrative teaching values, not real records.

datasets = {
    "Tablet assay (%)": [
        98.2, 99.1, 97.8, 100.0, 98.9, 99.5
    ],

    "Hospitalisation days": [
        2, 4, 3, 3, 2, 3, 2, 5, 4, 3,
        2, 4, 5, 6, 2, 4, 3, 4, 2, 3,
        5, 3, 4, 2, 3
    ],

    "Dissolution at 30 minutes (%)": [
        72, 75, 78, 80, 82, 84,
        85, 87, 88, 90, 91, 93
    ],

    "Time to adverse-event onset (days)": [
        1.2, 2.0, 2.0, 3.5, 4.0, 4.0, 5.5, 7.0
    ],

    "Adverse reaction type": [
        "Nausea", "Headache", "Nausea", "Rash",
        "Nausea", "Headache", "Rash", "Nausea"
    ]
}

# --------------------------------------------------
# 2. SELECT A DATASET
# --------------------------------------------------

st.header("1. Select a teaching dataset")

dataset_name = st.selectbox(
    "Choose an example dataset",
    list(datasets.keys())
)

data = datasets[dataset_name]

st.write("Observations in the selected dataset:")
st.code("data = " + repr(data), language="python")

st.caption(
    "All observations are illustrative teaching data."
)

# Categorical data are appropriate for mode,
# frequency tables and counts, but not numerical
# calculations such as mean or standard deviation.

categorical = dataset_name == "Adverse reaction type"

if categorical:
    statistics = [
        "Mode",
        "Frequency table",
        "Count"
    ]
else:
    statistics = [
        "Mean",
        "Median",
        "Mode",
        "Minimum",
        "Maximum",
        "Range",
        "Population variance",
        "Sample variance",
        "Population standard deviation",
        "Sample standard deviation",
        "First quartile (Q1)",
        "Third quartile (Q3)",
        "Interquartile range (IQR)",
        "Count",
        "Frequency table",
        "Skewness"
    ]

# --------------------------------------------------
# 3. SELECT A STATISTIC
# --------------------------------------------------

st.header("2. Select the statistic to learn")

statistic = st.selectbox(
    "Descriptive statistic",
    statistics
)

# Each entry below is a complete standalone
# Python program that students can copy and study.

programs = {

"Mean": '''
# STEP 1: Import NumPy for numerical calculations.
import numpy as np

# STEP 2: Enter the tablet assay observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into a NumPy array.
values = np.array(data)

# STEP 4: Calculate the arithmetic mean.
# The mean is the sum of observations divided by n.
mean_value = np.mean(values)

# STEP 5: Display the calculated value.
print("Mean assay (%) =", mean_value)
''',

"Median": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate the median.
# For an even number of observations, NumPy averages
# the two middle values after ordering the data.
median_value = np.median(values)

# STEP 5: Display the result.
print("Median assay (%) =", median_value)
''',

"Mode": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter the hospitalisation data.
data = [
    2, 4, 3, 3, 2, 3, 2, 5, 4, 3,
    2, 4, 5, 6, 2, 4, 3, 4, 2, 3,
    5, 3, 4, 2, 3
]

# STEP 3: Convert the list into a Pandas Series.
values = pd.Series(data)

# STEP 4: Find the most frequent value or values.
mode_values = values.mode()

# STEP 5: Display all modes.
print("Mode value(s) =", mode_values.tolist())
''',

"Minimum": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Find the smallest observation.
minimum_value = np.min(values)

# STEP 5: Display the result.
print("Minimum assay (%) =", minimum_value)
''',

"Maximum": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Find the largest observation.
maximum_value = np.max(values)

# STEP 5: Display the result.
print("Maximum assay (%) =", maximum_value)
''',

"Range": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate the range.
# Range = maximum value minus minimum value.
data_range = np.max(values) - np.min(values)

# STEP 5: Display the result.
print("Range of assay (%) =", data_range)
''',

"Population variance": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the population observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate population variance.
# ddof=0 uses N in the denominator.
population_variance = np.var(values, ddof=0)

# STEP 5: Display the result.
print("Population variance =", population_variance)
''',

"Sample variance": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the sample observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate sample variance.
# ddof=1 uses n - 1 in the denominator.
sample_variance = np.var(values, ddof=1)

# STEP 5: Display the result.
print("Sample variance =", sample_variance)
''',

"Population standard deviation": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the population observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate population standard deviation.
# ddof=0 specifies the population calculation.
population_sd = np.std(values, ddof=0)

# STEP 5: Display the result.
print("Population standard deviation =", population_sd)
''',

"Sample standard deviation": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the sample observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Convert the list into a NumPy array.
values = np.array(data)

# STEP 4: Calculate sample standard deviation.
# ddof=1 uses n - 1 in the variance calculation.
sample_sd = np.std(values, ddof=1)

# STEP 5: Display the result.
print("Sample standard deviation =", sample_sd)
''',

"First quartile (Q1)": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the dissolution observations.
data = [72, 75, 78, 80, 82, 84, 85, 87, 88, 90, 91, 93]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate the 25th percentile.
# The 25th percentile is commonly called Q1.
q1 = np.percentile(values, 25)

# STEP 5: Display the result.
print("First quartile (Q1) =", q1)
''',

"Third quartile (Q3)": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the dissolution observations.
data = [72, 75, 78, 80, 82, 84, 85, 87, 88, 90, 91, 93]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate the 75th percentile.
# The 75th percentile is commonly called Q3.
q3 = np.percentile(values, 75)

# STEP 5: Display the result.
print("Third quartile (Q3) =", q3)
''',

"Interquartile range (IQR)": '''
# STEP 1: Import NumPy.
import numpy as np

# STEP 2: Enter the dissolution observations.
data = [72, 75, 78, 80, 82, 84, 85, 87, 88, 90, 91, 93]

# STEP 3: Convert the list into an array.
values = np.array(data)

# STEP 4: Calculate Q1 and Q3.
q1 = np.percentile(values, 25)
q3 = np.percentile(values, 75)

# STEP 5: Calculate the interquartile range.
# IQR = Q3 - Q1.
iqr = q3 - q1

# STEP 6: Display the result.
print("Interquartile range =", iqr)
''',

"Count": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter the observations.
data = [98.2, 99.1, 97.8, 100.0, 98.9, 99.5]

# STEP 3: Create a Pandas Series.
values = pd.Series(data)

# STEP 4: Count the non-missing observations.
number_of_observations = values.count()

# STEP 5: Display the count.
print("Number of observations =", number_of_observations)
''',

"Frequency table": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter the hospitalisation data.
data = [
    2, 4, 3, 3, 2, 3, 2, 5, 4, 3,
    2, 4, 5, 6, 2, 4, 3, 4, 2, 3,
    5, 3, 4, 2, 3
]

# STEP 3: Create a Pandas Series.
values = pd.Series(data)

# STEP 4: Count each distinct value.
# sort_index() arranges values in ascending order.
frequency_table = values.value_counts().sort_index()

# STEP 5: Display the frequency table.
print("Frequency table:")
print(frequency_table)
''',

"Skewness": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter the time-to-onset observations.
data = [1.2, 2.0, 2.0, 3.5, 4.0, 4.0, 5.5, 7.0]

# STEP 3: Create a Pandas Series.
values = pd.Series(data)

# STEP 4: Calculate sample skewness.
# Positive skewness often suggests a longer right tail.
# Negative skewness often suggests a longer left tail.
skewness_value = values.skew()

# STEP 5: Display the result.
print("Skewness =", skewness_value)
'''
}

categorical_programs = {
"Mode": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter adverse reaction categories.
data = [
    "Nausea", "Headache", "Nausea", "Rash",
    "Nausea", "Headache", "Rash", "Nausea"
]

# STEP 3: Create a Pandas Series.
reactions = pd.Series(data)

# STEP 4: Find the most frequently occurring category.
mode_values = reactions.mode()

# STEP 5: Display the mode.
print("Most common reaction type(s) =", mode_values.tolist())
''',

"Frequency table": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter adverse reaction categories.
data = [
    "Nausea", "Headache", "Nausea", "Rash",
    "Nausea", "Headache", "Rash", "Nausea"
]

# STEP 3: Create a Pandas Series.
reactions = pd.Series(data)

# STEP 4: Count each category.
frequency_table = reactions.value_counts()

# STEP 5: Display the frequency table.
print("Frequency of reaction types:")
print(frequency_table)
''',

"Count": '''
# STEP 1: Import Pandas.
import pandas as pd

# STEP 2: Enter adverse reaction categories.
data = [
    "Nausea", "Headache", "Nausea", "Rash",
    "Nausea", "Headache", "Rash", "Nausea"
]

# STEP 3: Create a Pandas Series.
reactions = pd.Series(data)

# STEP 4: Count the recorded categories.
number_of_reports = reactions.count()

# STEP 5: Display the count.
print("Number of reports =", number_of_reports)
'''
}

# --------------------------------------------------
# 4. DISPLAY THE COMPLETE PYTHON PROGRAM
# --------------------------------------------------

if categorical:
    program = categorical_programs[statistic]
else:
    program = programs[statistic]

st.header("3. Complete Python program")

st.write(
    "Read the code from top to bottom. Lines beginning with # are comments. "
    "Python ignores comments when running a program."
)

st.code(program, language="python")

# --------------------------------------------------
# 5. SHOW EXPECTED OUTPUT
# --------------------------------------------------

st.header("4. Expected output")

# Calculate the example result separately for demonstration.
# This is not dynamic execution of the displayed source code.

values = pd.Series(data)

if statistic == "Mean":
    result = values.mean()
elif statistic == "Median":
    result = values.median()
elif statistic == "Mode":
    result = values.mode().tolist()
elif statistic == "Minimum":
    result = values.min()
elif statistic == "Maximum":
    result = values.max()
elif statistic == "Range":
    result = values.max() - values.min()
elif statistic == "Population variance":
    result = values.var(ddof=0)
elif statistic == "Sample variance":
    result = values.var(ddof=1)
elif statistic == "Population standard deviation":
    result = values.std(ddof=0)
elif statistic == "Sample standard deviation":
    result = values.std(ddof=1)
elif statistic == "First quartile (Q1)":
    result = values.quantile(0.25)
elif statistic == "Third quartile (Q3)":
    result = values.quantile(0.75)
elif statistic == "Interquartile range (IQR)":
    result = values.quantile(0.75) - values.quantile(0.25)
elif statistic == "Count":
    result = values.count()
elif statistic == "Frequency table":
    result = values.value_counts().sort_index()
elif statistic == "Skewness":
    result = values.skew()

if isinstance(result, pd.Series):
    st.code(result.to_string(), language="text")
elif isinstance(result, list):
    st.code(repr(result), language="text")
else:
    st.code(f"{statistic} = {result}", language="text")

# --------------------------------------------------
# 6. INTERPRETATION AND LEARNING NOTES
# --------------------------------------------------

st.header("5. What does the code teach us?")

explanations = {
    "Mean": "The mean is the sum of observations divided by their number. It can be influenced by extreme values.",
    "Median": "The median is the middle value after ordering the data. For an even sample size, the two middle values are averaged.",
    "Mode": "The mode is the most frequently occurring value or category. A dataset can have more than one mode.",
    "Minimum": "The minimum is the smallest observed value.",
    "Maximum": "The maximum is the largest observed value.",
    "Range": "Range = maximum minus minimum. It describes the full span of the observations.",
    "Population variance": "ddof=0 uses N in the denominator when the observations represent the population of interest.",
    "Sample variance": "ddof=1 uses n - 1 in the denominator for the usual sample variance estimate.",
    "Population standard deviation": "Population standard deviation is expressed in the same units as the observations.",
    "Sample standard deviation": "Sample standard deviation is the square root of sample variance. ddof=1 specifies the n - 1 denominator.",
    "First quartile (Q1)": "Q1 is the 25th percentile. Software may use different conventions for calculating percentiles.",
    "Third quartile (Q3)": "Q3 is the 75th percentile. Software may use different conventions for calculating percentiles.",
    "Interquartile range (IQR)": "IQR = Q3 - Q1. It describes the spread of the middle 50% of observations.",
    "Count": "Pandas count() counts non-missing observations.",
    "Frequency table": "value_counts() counts how often each distinct value occurs.",
    "Skewness": "Skewness describes asymmetry. Interpret it alongside a graph and the sample size."
}

st.write(explanations[statistic])

with st.expander("Why do we use comments?"):
    st.write(
        "Comments begin with #. They explain the purpose of a line or section "
        "but do not change the calculation."
    )
    st.write(
        "Students can copy a displayed program into a separate .py file, "
        "run it themselves, change the observations, and observe how the result changes."
    )

st.caption(
    "All examples are for teaching. The displayed source program is not dynamically executed."
)
