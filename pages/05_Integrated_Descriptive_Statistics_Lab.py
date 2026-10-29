
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Integrated Descriptive Statistics Lab",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Unit I — Integrated Descriptive Statistics Lab")
st.write(
    "An integrated practical exercise covering frequency distributions, "
    "graphs, central tendency, variance and standard deviation."
)

st.info(
    "All datasets in this lesson are synthetic teaching data. "
    "They are not real patient records."
)


# --------------------------------------------------
# 1. Generate synthetic pharmaceutical datasets
# --------------------------------------------------
@st.cache_data
def create_datasets():
    rng = np.random.default_rng(2026)
    n = 240

    clinical = pd.DataFrame({
        "Patient_ID": [f"CT{i:03d}" for i in range(1, n + 1)],
        "Age_years": np.clip(
            np.round(rng.normal(46, 13, n)), 18, 85
        ).astype(int),
        "Systolic_BP_mmHg": np.round(
            rng.normal(125, 15, n), 1
        ),
        "Treatment_Group": rng.choice(
            ["Placebo", "Drug A", "Drug B"], n
        )
    })

    pharmacovigilance = pd.DataFrame({
        "Report_ID": [f"ADR{i:03d}" for i in range(1, n + 1)],
        "Age_years": np.clip(
            np.round(rng.normal(50, 16, n)), 18, 90
        ).astype(int),
        "Onset_days": np.round(
            rng.exponential(5, n), 1
        ),
        "Severity": rng.choice(
            ["Mild", "Moderate", "Severe"],
            n,
            p=[0.56, 0.34, 0.10]
        )
    })

    pk = pd.DataFrame({
        "Subject_ID": [f"PK{i:03d}" for i in range(1, n + 1)],
        "Dose_mg": rng.choice([50, 100, 200, 400], n),
        "Cmax_ng_mL": np.round(
            rng.lognormal(np.log(1200), 0.35, n), 1
        ),
        "AUC_ng_h_mL": np.round(
            rng.lognormal(np.log(8500), 0.32, n), 1
        )
    })

    qc = pd.DataFrame({
        "Batch_ID": [f"TB{i:03d}" for i in range(1, n + 1)],
        "Assay_percent": np.round(
            rng.normal(99.2, 1.25, n), 2
        ),
        "Dissolution_percent": np.round(
            np.clip(rng.normal(87, 6, n), 55, 100), 2
        ),
        "Tablet_hardness_N": np.round(
            rng.normal(72, 8, n), 1
        ),
        "Defects": rng.choice([0, 1, 2, 3], n)
    })

    return {
        "Clinical trial": clinical,
        "Pharmacovigilance": pharmacovigilance,
        "Pharmacokinetics": pk,
        "Quality control": qc
    }


datasets = create_datasets()


# --------------------------------------------------
# 2. Select dataset and variable
# --------------------------------------------------
st.header("1. Explore the data")

dataset_name = st.selectbox(
    "Select a pharmaceutical dataset",
    list(datasets.keys())
)

df = datasets[dataset_name]

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

variable = st.selectbox(
    "Select a numeric variable",
    numeric_columns
)

values = df[variable].dropna().to_numpy(dtype=float)

st.write(f"Selected variable: **{variable}**")
st.write(f"Number of observations: **{len(values)}**")

st.subheader("Raw observations")

st.dataframe(
    df[[variable]].head(25),
    use_container_width=True
)

with st.expander("View the complete dataset"):
    st.dataframe(df, use_container_width=True)


# --------------------------------------------------
# 3. Frequency distribution
# --------------------------------------------------
st.header("2. Construct a frequency distribution")

table_type = st.radio(
    "Choose the type of distribution",
    ["Ungrouped", "Grouped"],
    horizontal=True
)

if table_type == "Ungrouped":

    frequencies = (
        pd.Series(values)
        .value_counts()
        .sort_index()
    )

    frequency_table = pd.DataFrame({
        "Value": frequencies.index,
        "Frequency": frequencies.values,
        "Relative frequency": frequencies.values / len(values),
        "Percentage (%)": 100 * frequencies.values / len(values)
    })

else:

    method = st.radio(
        "Define the class intervals using",
        ["Number of bins", "Class width"],
        horizontal=True
    )

    if method == "Number of bins":

        number_of_bins = st.slider(
            "Number of bins", 3, 20, 8
        )

        counts, edges = np.histogram(
            values, bins=number_of_bins
        )

    else:

        default_width = max(
            0.01,
            round((values.max() - values.min()) / 8, 2)
        )

        width = st.number_input(
            "Class width",
            min_value=0.01,
            value=float(default_width)
        )

        start = st.number_input(
            "Starting boundary",
            value=float(np.floor(values.min()))
        )

        edges = np.arange(
            start,
            values.max() + width * 1.01,
            width
        )

        if len(edges) < 2:
            edges = np.array([start, start + width])

        if edges[-1] <= values.max():
            edges = np.append(edges, edges[-1] + width)

        counts, edges = np.histogram(values, bins=edges)

    intervals = [
        f"{edges[i]:.3g} – {edges[i + 1]:.3g}"
        for i in range(len(edges) - 1)
    ]

    frequency_table = pd.DataFrame({
        "Class interval": intervals,
        "Frequency": counts,
        "Relative frequency": counts / len(values),
        "Percentage (%)": 100 * counts / len(values)
    })

st.dataframe(
    frequency_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 4. Graphical representation
# --------------------------------------------------
st.header("3. Visualize the distribution")

graph_type = st.radio(
    "Select a graph",
    ["Histogram", "Bar graph", "Pie chart"],
    horizontal=True
)

fig, ax = plt.subplots()

if graph_type == "Histogram":

    bins = st.slider(
        "Histogram bins", 3, 25, 10
    )

    ax.hist(values, bins=bins, edgecolor="black")
    ax.set_xlabel(variable)
    ax.set_ylabel("Frequency")

elif graph_type == "Bar graph":

    frequencies = pd.Series(values).value_counts().sort_index()

    if len(frequencies) > 30:
        counts, edges = np.histogram(values, bins=10)

        labels = [
            f"{edges[i]:.2g}–{edges[i + 1]:.2g}"
            for i in range(len(counts))
        ]

        ax.bar(labels, counts, edgecolor="black")

    else:
        ax.bar(
            [str(x) for x in frequencies.index],
            frequencies.values,
            edgecolor="black"
        )

    ax.set_xlabel(variable)
    ax.set_ylabel("Frequency")
    ax.tick_params(axis="x", rotation=45)

else:

    frequencies = pd.Series(values).value_counts().sort_index()

    if len(frequencies) > 12:

        counts, edges = np.histogram(values, bins=8)
        mask = counts > 0

        labels = [
            f"{edges[i]:.2g}–{edges[i + 1]:.2g}"
            for i in range(len(counts)) if mask[i]
        ]

        ax.pie(
            counts[mask],
            labels=labels,
            autopct="%1.1f%%"
        )

    else:
        ax.pie(
            frequencies.values,
            labels=[str(x) for x in frequencies.index],
            autopct="%1.1f%%"
        )

st.pyplot(fig, use_container_width=True)
plt.close(fig)


# --------------------------------------------------
# 5. Central tendency
# --------------------------------------------------
st.header("4. Calculate central tendency")

measure = st.selectbox(
    "Choose a measure",
    ["Mean", "Median", "Mode"]
)

if measure == "Mean":
    correct_answer = float(np.mean(values))
    st.latex(r"\bar{x}=\frac{\sum x_i}{n}")

elif measure == "Median":
    correct_answer = float(np.median(values))
    st.write(
        "Arrange the observations in order. "
        "For an even number of observations, average the two middle values."
    )

else:
    modes = pd.Series(values).mode()
    correct_answer = float(modes.iloc[0])
    st.write(
        "The mode is the most frequently occurring value. "
        "If there are multiple modes, the app uses the first mode for checking."
    )

student_answer = st.number_input(
    "Enter your calculated answer",
    value=0.0,
    format="%.6f"
)

if st.button("Check central tendency answer"):

    tolerance = max(0.01, abs(correct_answer) * 0.01)

    if abs(student_answer - correct_answer) <= tolerance:
        st.success("Correct! Your answer is within the rounding tolerance.")
    else:
        st.error(
            f"Not quite. The reference answer is "
            f"{correct_answer:.4f}."
        )

with st.expander("Reveal the reference answer"):
    st.write(f"{measure}: **{correct_answer:.4f}**")

    if measure == "Mode":
        st.write(f"Mode value(s): {modes.tolist()}")


# --------------------------------------------------
# 6. Variance and sample standard deviation
# --------------------------------------------------
st.header("5. Calculate variance and sample standard deviation")

st.markdown("**Sample variance**")
st.latex(
    r"s^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}"
)

st.markdown("**Sample standard deviation**")
st.latex(
    r"s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}"
)

st.write(
    "For this exercise, use the sample formula and divide by n − 1."
)

mean_value = float(np.mean(values))
sample_variance = float(np.var(values, ddof=1))
sample_sd = float(np.std(values, ddof=1))

c1, c2, c3 = st.columns(3)

c1.metric("Mean", f"{mean_value:.4f}")
c2.metric("Sample variance", f"{sample_variance:.4f}")
c3.metric("Sample SD", f"{sample_sd:.4f}")

student_variance = st.number_input(
    "Enter your sample variance",
    value=0.0,
    format="%.6f"
)

if st.button("Check sample variance"):

    tolerance = max(0.01, abs(sample_variance) * 0.01)

    if abs(student_variance - sample_variance) <= tolerance:
        st.success("Correct sample variance!")
    else:
        st.error(
            f"Reference variance: {sample_variance:.4f}. "
            "Remember to divide by n − 1."
        )

student_sd = st.number_input(
    "Enter your sample standard deviation",
    value=0.0,
    format="%.6f"
)

if st.button("Check sample standard deviation"):

    tolerance = max(0.01, abs(sample_sd) * 0.01)

    if abs(student_sd - sample_sd) <= tolerance:
        st.success("Correct sample standard deviation!")
    else:
        st.error(
            f"Reference SD: {sample_sd:.4f}. "
            "Take the square root of the sample variance."
        )


# --------------------------------------------------
# 7. Interpretation
# --------------------------------------------------
st.header("6. Interpret the results")

with st.expander("Show interpretation"):

    median_value = float(np.median(values))

    st.write(
        f"For **{variable}** in the **{dataset_name}** dataset:"
    )

    st.write(f"- Mean: {mean_value:.3f}")
    st.write(f"- Median: {median_value:.3f}")
    st.write(f"- Sample standard deviation: {sample_sd:.3f}")

    st.write(
        "Standard deviation describes spread in the same units as "
        "the observations. Variance is expressed in squared units. "
        "Use the graph as well as the numerical summaries when "
        "interpreting the distribution."
    )


# --------------------------------------------------
# 8. Self-assessment
# --------------------------------------------------
st.header("7. Self-assessment")

questions = [
    (
        "Which measure is usually less affected by extreme values?",
        ["Mean", "Median", "Range"],
        "Median"
    ),
    (
        "What denominator is used in the usual sample variance formula?",
        ["n", "n − 1", "n + 1"],
        "n − 1"
    ),
    (
        "Which graph is generally suitable for continuous numeric data?",
        ["Histogram", "Pie chart only", "Word cloud"],
        "Histogram"
    )
]

responses = []

for i, (question, options, correct) in enumerate(questions):
    response = st.radio(question, options, key=f"lesson7_q{i}")
    responses.append(response)

if st.button("Submit self-assessment"):

    score = sum(
        responses[i] == questions[i][2]
        for i in range(len(questions))
    )

    st.metric("Your score", f"{score}/3")

    for i, (_, _, correct) in enumerate(questions):

        if responses[i] == correct:
            st.success(f"Question {i + 1}: Correct.")

        else:
            st.error(
                f"Question {i + 1}: Correct answer — {correct}."
            )

st.divider()
st.caption(
    "All records are synthetic teaching data and are not for clinical use."
)
