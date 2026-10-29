
# ================================================================
# APPLIED BIOSTATISTICS LAB
# Lesson 4: Frequency Distributions
# ================================================================
#
# Learning objectives
# 1. Understand grouped and ungrouped frequency distributions.
# 2. Generate samples from a larger population.
# 3. Construct frequency tables and calculate relative frequencies.
# 4. Change class width and class intervals.
# 5. Select suitable graphical representations.
# 6. Compare a sample distribution with its population distribution.
#
# IMPORTANT:
# All datasets generated in this application are synthetic.
# The population pool is hidden from students by default.
# This is an educational demonstration, not a secure data system.
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------

st.set_page_config(
    page_title="Lesson 4: Frequency Distributions",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Lesson 4: Frequency Distributions")

st.markdown("""
### Learning objectives

By the end of this practical, you should be able to:

- Distinguish between grouped and ungrouped frequency distributions.
- Draw a random sample from a larger population.
- Construct a frequency distribution table.
- Calculate relative and percentage frequencies.
- Change the number and width of class intervals.
- Select an appropriate graph for a variable.
- Interpret the shape of a distribution.
""")

st.info(
    "The application maintains a synthetic population pool of 1,000 "
    "observations for each variable. You will normally see only the "
    "sample you generate from that pool."
)


# ------------------------------------------------
# 2. GENERATE THE SYNTHETIC POPULATION POOLS
# ------------------------------------------------

@st.cache_data
def create_population_pools():
    """
    Generate reproducible synthetic populations.

    The fixed random seed makes the population pools reproducible.
    These populations remain the same across reruns of this function.
    """

    rng = np.random.default_rng(2026)
    n = 1000

    # Tablet weights: approximately normally distributed.
    tablet_weight = rng.normal(
        loc=500,
        scale=5,
        size=n
    )
    tablet_weight = np.round(tablet_weight, 1)

    # Tablet assay: approximately normal, expressed as percentage.
    tablet_assay = rng.normal(
        loc=100,
        scale=2,
        size=n
    )
    tablet_assay = np.clip(tablet_assay, 90, 110)
    tablet_assay = np.round(tablet_assay, 2)

    # Dissolution at 30 minutes: bounded between 0 and 100%.
    dissolution = rng.normal(
        loc=85,
        scale=7,
        size=n
    )
    dissolution = np.clip(dissolution, 0, 100)
    dissolution = np.round(dissolution, 1)

    # Hospitalisation days: non-negative integer values.
    # A Poisson model creates a discrete distribution.
    hospital_days = rng.poisson(
        lam=4,
        size=n
    )

    # Adverse-event reports per day: count data.
    adverse_reports = rng.poisson(
        lam=3,
        size=n
    )

    # Time to adverse-event onset: positive, right-skewed data.
    onset_days = rng.lognormal(
        mean=1.2,
        sigma=0.65,
        size=n
    )
    onset_days = np.round(onset_days, 1)

    pools = {
        "Tablet weight (mg)": {
            "values": tablet_weight,
            "description": (
                "Continuous measurement; approximately normal."
            ),
            "unit": "mg",
            "recommended": "Grouped",
            "variable_type": "Continuous"
        },
        "Tablet assay (%)": {
            "values": tablet_assay,
            "description": (
                "Continuous measurement; approximately normal, "
                "with values restricted to a plausible teaching range."
            ),
            "unit": "%",
            "recommended": "Grouped",
            "variable_type": "Continuous"
        },
        "Dissolution at 30 minutes (%)": {
            "values": dissolution,
            "description": (
                "Continuous percentage bounded between 0 and 100."
            ),
            "unit": "%",
            "recommended": "Grouped",
            "variable_type": "Continuous"
        },
        "Hospitalisation days": {
            "values": hospital_days,
            "description": (
                "Discrete, non-negative count data."
            ),
            "unit": "days",
            "recommended": "Ungrouped",
            "variable_type": "Discrete"
        },
        "Adverse-event reports per day": {
            "values": adverse_reports,
            "description": (
                "Discrete count data generated using a Poisson model."
            ),
            "unit": "reports",
            "recommended": "Ungrouped",
            "variable_type": "Discrete"
        },
        "Time to adverse-event onset (days)": {
            "values": onset_days,
            "description": (
                "Positive, right-skewed continuous data."
            ),
            "unit": "days",
            "recommended": "Grouped",
            "variable_type": "Continuous"
        }
    }

    return pools


pools = create_population_pools()


# ------------------------------------------------
# 3. SELECT THE VARIABLE
# ------------------------------------------------

st.header("Step 1: Select a variable")

dataset_name = st.selectbox(
    "Choose a pharmaceutical or healthcare variable",
    options=list(pools.keys())
)

selected_data = pools[dataset_name]
population = selected_data["values"]

st.write("**Variable:**", dataset_name)
st.write("**Variable type:**", selected_data["variable_type"])
st.write("**Description:**", selected_data["description"])
st.write("**Unit:**", selected_data["unit"])
st.write("**Population pool size:** 1,000 observations")

with st.expander("Why do these variables have different distributions?"):
    st.markdown("""
    - **Tablet weight:** often treated as approximately normal in a
      controlled manufacturing process.
    - **Tablet assay:** a continuous quality measurement that may be
      approximately normal within an acceptable range.
    - **Dissolution:** a percentage bounded between 0 and 100.
    - **Hospitalisation days:** discrete count data.
    - **Adverse-event reports:** discrete count data.
    - **Time to adverse-event onset:** time measurements are often
      non-negative and may be right-skewed.

    These are illustrative synthetic distributions. Real datasets may
    have different shapes, and real observations should be examined
    rather than assumed to follow a particular distribution.
    """)


# ------------------------------------------------
# 4. GENERATE A RANDOM SAMPLE
# ------------------------------------------------

st.header("Step 2: Generate a random sample")

st.write("""
Choose the number of observations you want to study. The application
will draw a sample **without replacement** from the 1,000-value pool.
""")

col1, col2 = st.columns(2)

with col1:
    sample_size = st.select_slider(
        "Sample size",
        options=[20, 30, 50, 75, 100, 150, 250, 500, 750, 1000],
        value=50
    )

with col2:
    seed = st.number_input(
        "Random seed",
        min_value=0,
        max_value=999999,
        value=42,
        step=1,
        help=(
            "The same seed, population and sample size reproduce "
            "the same sample."
        )
    )

if st.button("🎲 Generate / refresh sample", type="primary"):
    rng = np.random.default_rng(int(seed))

    sample = rng.choice(
        population,
        size=int(sample_size),
        replace=False
    )

    st.session_state["lesson4_sample"] = sample
    st.session_state["lesson4_sample_name"] = dataset_name
    st.session_state["lesson4_sample_size"] = int(sample_size)
    st.session_state["lesson4_seed"] = int(seed)

# Generate an initial sample automatically if needed.
if (
    "lesson4_sample" not in st.session_state
    or st.session_state.get("lesson4_sample_name") != dataset_name
    or st.session_state.get("lesson4_sample_size") != int(sample_size)
    or st.session_state.get("lesson4_seed") != int(seed)
):
    rng = np.random.default_rng(int(seed))
    st.session_state["lesson4_sample"] = rng.choice(
        population,
        size=int(sample_size),
        replace=False
    )
    st.session_state["lesson4_sample_name"] = dataset_name
    st.session_state["lesson4_sample_size"] = int(sample_size)
    st.session_state["lesson4_seed"] = int(seed)

sample = np.asarray(st.session_state["lesson4_sample"])

st.success(
    f"Your sample contains {len(sample)} observations "
    f"selected from the population pool."
)


# ------------------------------------------------
# 5. DISPLAY THE SAMPLE
# ------------------------------------------------

st.header("Step 3: Examine your sample")

with st.expander("View the sampled observations", expanded=True):
    sample_df = pd.DataFrame({
        "Observation number": np.arange(1, len(sample) + 1),
        dataset_name: sample
    })

    st.dataframe(
        sample_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = sample_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download sample as CSV",
        data=csv_data,
        file_name="lesson4_sample.csv",
        mime="text/csv"
    )


# ------------------------------------------------
# 6. CHOOSE GROUPED OR UNGROUPED DISTRIBUTION
# ------------------------------------------------

st.header("Step 4: Choose the frequency distribution")

st.write("""
A frequency distribution summarises how often each value or class
interval occurs.
""")

distribution_choice = st.radio(
    "Which type of frequency distribution would you like to construct?",
    options=["Ungrouped frequency distribution",
             "Grouped frequency distribution"],
    horizontal=True
)

if distribution_choice == "Ungrouped frequency distribution":
    st.caption(
        "An ungrouped table lists individual values and their frequencies. "
        "It is often useful for discrete variables with relatively few "
        "distinct values."
    )
else:
    st.caption(
        "A grouped table combines observations into class intervals. "
        "It is often useful for continuous measurements or datasets "
        "with many distinct values."
    )


# ------------------------------------------------
# 7. CREATE AN UNGROUPED FREQUENCY TABLE
# ------------------------------------------------

def make_ungrouped_frequency_table(values):
    """
    Create a frequency table for individual observed values.
    """

    series = pd.Series(values)

    table = (
        series.value_counts()
        .sort_index()
        .rename_axis("Value")
        .reset_index(name="Frequency")
    )

    table["Relative frequency"] = (
        table["Frequency"] / len(series)
    )

    table["Percentage (%)"] = (
        table["Relative frequency"] * 100
    )

    table["Cumulative frequency"] = (
        table["Frequency"].cumsum()
    )

    return table


# ------------------------------------------------
# 8. CREATE A GROUPED FREQUENCY TABLE
# ------------------------------------------------

def make_grouped_frequency_table(values, number_of_classes, class_width, start_boundary):
    """
    Create a grouped frequency table using user-selected class settings.

    If class width is specified, class intervals are built starting at
    the selected boundary and extended far enough to include all values.
    """

    values = np.asarray(values, dtype=float)

    minimum = float(np.min(values))
    maximum = float(np.max(values))

    # Ensure a positive class width.
    class_width = max(float(class_width), 0.000001)

    # If the starting boundary is above the smallest observation,
    # extend the intervals backwards so that all observations are included.
    if start_boundary > minimum:
        steps_back = int(
            np.ceil((start_boundary - minimum) / class_width)
        )
        start_boundary = start_boundary - steps_back * class_width

    # Calculate enough intervals to include the maximum observation.
    number_needed = int(
        np.floor((maximum - start_boundary) / class_width)
    ) + 1

    number_needed = max(number_needed, 1)

    edges = (
        start_boundary
        + np.arange(number_needed + 1) * class_width
    )

    # If a value lies exactly at the last boundary, extend one more interval.
    while maximum >= edges[-1]:
        edges = np.append(edges, edges[-1] + class_width)

    frequencies, edges = np.histogram(
        values,
        bins=edges
    )

    table = pd.DataFrame({
        "Class interval": [
            f"{edges[i]:.3f} – < {edges[i + 1]:.3f}"
            for i in range(len(frequencies))
        ],
        "Lower boundary": edges[:-1],
        "Upper boundary": edges[1:],
        "Frequency": frequencies
    })

    table["Relative frequency"] = (
        table["Frequency"] / len(values)
    )

    table["Percentage (%)"] = (
        table["Relative frequency"] * 100
    )

    table["Cumulative frequency"] = (
        table["Frequency"].cumsum()
    )

    return table, edges


# ------------------------------------------------
# 9. CONFIGURE CLASS INTERVALS
# ------------------------------------------------

frequency_table = None
class_edges = None

if distribution_choice == "Ungrouped frequency distribution":

    frequency_table = make_ungrouped_frequency_table(sample)

else:

    st.subheader("Configure your class intervals")

    col1, col2, col3 = st.columns(3)

    sample_min = float(np.min(sample))
    sample_max = float(np.max(sample))
    sample_range = sample_max - sample_min

    # Use a sensible default class width.
    if sample_range > 0:
        default_width = sample_range / 5
    else:
        default_width = 1.0

    if selected_data["variable_type"] == "Discrete":
        default_width = max(1.0, round(default_width))
        width_step = 1.0
    else:
        width_step = max(default_width / 10, 0.1)

    with col1:
        number_of_classes = st.number_input(
            "Suggested number of classes",
            min_value=2,
            max_value=30,
            value=5,
            step=1
        )

    with col2:
        class_width = st.number_input(
            "Class width",
            min_value=0.0001,
            value=float(round(default_width, 3)),
            step=float(round(width_step, 3)),
            format="%.3f"
        )

    with col3:
        start_boundary = st.number_input(
            "Starting class boundary",
            value=float(np.floor(sample_min)),
            step=float(1.0 if selected_data["variable_type"] == "Discrete" else 0.5),
            format="%.3f"
        )

    st.caption(
        "The table is constructed using your selected class width and "
        "starting boundary. The number of classes is a guide; the app "
        "extends the intervals if necessary to include every observation."
    )

    frequency_table, class_edges = make_grouped_frequency_table(
        sample,
        int(number_of_classes),
        float(class_width),
        float(start_boundary)
    )


# ------------------------------------------------
# 10. DISPLAY FREQUENCY TABLE
# ------------------------------------------------

st.header("Step 5: Frequency distribution table")

st.dataframe(
    frequency_table,
    use_container_width=True,
    hide_index=True
)

total_frequency = int(frequency_table["Frequency"].sum())
total_percentage = float(frequency_table["Percentage (%)"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("Sample size", f"{len(sample)}")
col2.metric("Total frequency", f"{total_frequency}")
col3.metric("Total percentage", f"{total_percentage:.2f}%")

if total_frequency == len(sample):
    st.success("Check passed: all sampled observations are included.")
else:
    st.error(
        "The frequencies do not add up to the sample size. "
        "Review the class intervals."
    )


# ------------------------------------------------
# 11. GRAPHICAL REPRESENTATION
# ------------------------------------------------

st.header("Step 6: Graphical representation")

if distribution_choice == "Ungrouped frequency distribution":
    graph_options = [
        "Bar chart",
        "Pie chart"
    ]
else:
    graph_options = [
        "Histogram",
        "Frequency polygon"
    ]

graph_choice = st.selectbox(
    "Choose a graph",
    options=graph_options
)

fig, ax = plt.subplots(figsize=(10, 5))

if graph_choice == "Bar chart":

    ax.bar(
        frequency_table["Value"].astype(str),
        frequency_table["Frequency"]
    )

    ax.set_xlabel(dataset_name)
    ax.set_ylabel("Frequency")
    ax.set_title("Bar chart of the ungrouped frequency distribution")
    ax.tick_params(axis="x", rotation=45)

elif graph_choice == "Pie chart":

    ax.pie(
        frequency_table["Frequency"],
        labels=frequency_table["Value"].astype(str),
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Pie chart of the ungrouped frequency distribution")

elif graph_choice == "Histogram":

    ax.hist(
        sample,
        bins=class_edges,
        edgecolor="black"
    )

    ax.set_xlabel(dataset_name)
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of the sample")

elif graph_choice == "Frequency polygon":

    frequencies = frequency_table["Frequency"].to_numpy()

    midpoints = (
        class_edges[:-1] + class_edges[1:]
    ) / 2

    ax.plot(
        midpoints,
        frequencies,
        marker="o"
    )

    ax.set_xlabel("Class midpoint")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequency polygon")
    ax.grid(True, alpha=0.3)

st.pyplot(fig)
plt.close(fig)


# ------------------------------------------------
# 12. DESCRIPTIVE INTERPRETATION
# ------------------------------------------------

st.header("Step 7: Interpret your sample")

sample_mean = float(np.mean(sample))
sample_median = float(np.median(sample))
sample_sd = float(np.std(sample, ddof=1)) if len(sample) > 1 else 0.0

col1, col2, col3 = st.columns(3)

col1.metric("Sample mean", f"{sample_mean:.3f}")
col2.metric("Sample median", f"{sample_median:.3f}")
col3.metric("Sample SD", f"{sample_sd:.3f}")

if sample_mean > sample_median:
    shape_message = (
        "The sample mean is greater than the median. This can occur "
        "in a right-skewed distribution, although it does not prove "
        "that the distribution is right-skewed."
    )
elif sample_mean < sample_median:
    shape_message = (
        "The sample mean is less than the median. This can occur "
        "in a left-skewed distribution, although it does not prove "
        "that the distribution is left-skewed."
    )
else:
    shape_message = (
        "The sample mean and median are equal or very close. "
        "This alone does not establish that the distribution is symmetric."
    )

st.write(shape_message)

with st.expander("How should I interpret the frequency table?"):
    st.markdown("""
    Consider the following points:

    1. Which value or class interval has the highest frequency?
    2. Are most observations concentrated in a small range?
    3. Does the distribution appear approximately symmetric?
    4. Is there a long tail towards higher or lower values?
    5. Would a grouped or ungrouped table communicate the data more clearly?
    6. Does the graph support the interpretation suggested by the table?
    """)


# ------------------------------------------------
# 13. OPTIONAL POPULATION COMPARISON
# ------------------------------------------------

st.header("Optional: Compare sample and population")

st.write("""
After completing your analysis, you may reveal the population distribution
to see how your sample compares with the full pool.
""")

reveal_population = st.checkbox(
    "Reveal the population distribution for comparison",
    value=False
)

if reveal_population:

    st.warning(
        "Instructor/learning comparison: the full population distribution "
        "is now displayed. In a public application, this is not a secure "
        "way to conceal data from users who can inspect the source code."
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    if selected_data["variable_type"] == "Discrete":
        all_values = np.arange(
            int(np.min(population)),
            int(np.max(population)) + 2
        ) - 0.5

        ax2.hist(
            population,
            bins=all_values,
            edgecolor="black",
            alpha=0.6,
            density=True,
            label="Population"
        )

        ax2.hist(
            sample,
            bins=all_values,
            edgecolor="black",
            alpha=0.6,
            density=True,
            label="Sample"
        )

    else:
        shared_bins = np.histogram_bin_edges(
            population,
            bins="auto"
        )

        ax2.hist(
            population,
            bins=shared_bins,
            alpha=0.55,
            density=True,
            label="Population"
        )

        ax2.hist(
            sample,
            bins=shared_bins,
            alpha=0.55,
            density=True,
            label="Sample"
        )

    ax2.set_xlabel(dataset_name)
    ax2.set_ylabel("Density")
    ax2.set_title("Sample versus population distribution")
    ax2.legend()

    st.pyplot(fig2)
    plt.close(fig2)

    population_mean = float(np.mean(population))
    population_median = float(np.median(population))
    population_sd = float(np.std(population, ddof=0))

    comparison = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Standard deviation"],
        "Sample": [
            sample_mean,
            sample_median,
            sample_sd
        ],
        "Population": [
            population_mean,
            population_median,
            population_sd
        ]
    })

    st.dataframe(
        comparison.round(3),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "The population SD uses denominator N; the sample SD shown above "
        "uses denominator n − 1."
    )


# ------------------------------------------------
# 14. PRACTICE QUESTIONS
# ------------------------------------------------

st.header("📝 Practice questions")

st.markdown("""
Answer the questions below. Submit your answers to receive feedback.
""")

# Question 1
st.subheader("Question 1: Frequency")

if distribution_choice == "Ungrouped frequency distribution":
    values_for_question = frequency_table["Value"].tolist()

    selected_value = st.selectbox(
        "Select a value whose frequency you want to check",
        options=values_for_question
    )

    correct_frequency = int(
        frequency_table.loc[
            frequency_table["Value"] == selected_value,
            "Frequency"
        ].iloc[0]
    )

    student_frequency = st.number_input(
        "Enter the frequency of this value",
        min_value=0,
        max_value=len(sample),
        value=0,
        step=1,
        key="q1_ungrouped"
    )

    if st.button("Check Question 1"):
        if int(student_frequency) == correct_frequency:
            st.success("Correct!")
        else:
            st.error(
                f"Not quite. The correct frequency is {correct_frequency}."
            )

else:
    interval_options = frequency_table["Class interval"].tolist()

    selected_interval = st.selectbox(
        "Select a class interval",
        options=interval_options
    )

    correct_frequency = int(
        frequency_table.loc[
            frequency_table["Class interval"] == selected_interval,
            "Frequency"
        ].iloc[0]
    )

    student_frequency = st.number_input(
        "Enter the frequency of this class interval",
        min_value=0,
        max_value=len(sample),
        value=0,
        step=1,
        key="q1_grouped"
    )

    if st.button("Check Question 1"):
        if int(student_frequency) == correct_frequency:
            st.success("Correct!")
        else:
            st.error(
                f"Not quite. The correct frequency is {correct_frequency}."
            )


# Question 2
st.divider()
st.subheader("Question 2: Relative frequency")

st.write(
    "Relative frequency is calculated by dividing a frequency "
    "by the total number of observations."
)

student_relative_frequency = st.number_input(
    "Enter the relative frequency of the first row in the table",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01,
    format="%.4f",
    key="q2_relative"
)

correct_relative_frequency = float(
    frequency_table["Frequency"].iloc[0] / len(sample)
)

if st.button("Check Question 2"):
    if np.isclose(
        student_relative_frequency,
        correct_relative_frequency,
        atol=0.005
    ):
        st.success("Correct!")
    else:
        st.error(
            "Review the formula: relative frequency = frequency / "
            f"sample size. Correct answer: {correct_relative_frequency:.4f}."
        )


# Question 3
st.divider()
st.subheader("Question 3: Choosing a distribution")

student_choice = st.radio(
    "For continuous measurements with many distinct values, which "
    "table is generally more useful for summarising the overall distribution?",
    options=[
        "Ungrouped frequency distribution",
        "Grouped frequency distribution"
    ],
    key="q3_choice"
)

if st.button("Check Question 3"):
    if student_choice == "Grouped frequency distribution":
        st.success(
            "Correct! Grouping can summarise continuous measurements "
            "into manageable class intervals."
        )
    else:
        st.info(
            "An ungrouped table can be useful for a small number of "
            "distinct values, but a grouped table is often clearer "
            "for continuous measurements with many distinct values."
        )


# ------------------------------------------------
# 15. KEY TAKEAWAYS
# ------------------------------------------------

st.divider()
st.header("Key takeaways")

st.markdown("""
- A **frequency** is the number of observations in a value or class.
- **Relative frequency** is frequency divided by the sample size.
- **Percentage frequency** is relative frequency multiplied by 100.
- **Ungrouped tables** list individual values.
- **Grouped tables** summarise values using class intervals.
- A **bar chart** is commonly used for categorical or discrete values.
- A **histogram** is commonly used for grouped continuous measurements.
- Sample distributions vary because different samples contain different
  observations.
- A larger sample often gives a more stable picture of the population,
  but does not eliminate bias or guarantee representativeness.
""")

st.success(
    "Lesson 4 completed. Try different variables, sample sizes, "
    "random seeds, class widths and graphs to explore how frequency "
    "distributions change."
)
