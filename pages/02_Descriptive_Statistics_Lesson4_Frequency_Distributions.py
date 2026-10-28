import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Unit I | Frequency Distributions", page_icon="📊", layout="wide")
st.title("Unit I — Lesson 4: Frequency Distributions")
st.caption("Organising raw pharmaceutical data into useful summaries")

st.markdown("""
A **frequency distribution** organises observations into values or classes and shows how often
each value or class occurs. It helps us see patterns that may be difficult to detect in a long list
of raw observations.

- **Ungrouped frequency distribution:** lists each distinct value or category and its frequency.
- **Grouped frequency distribution:** combines numerical observations into class intervals.
- Use an ungrouped table when the number of distinct values is small and meaningful.
- Use a grouped table when there are many distinct numerical values and grouping makes the pattern easier to interpret.
""")

st.subheader("1. Choose a synthetic pharmaceutical dataset")
datasets = {
    "Hospitalisation days (count)": pd.DataFrame({"Hospitalisation days": [2,4,3,3,2,3,2,5,4,3,2,4,5,6,2,4,3,4,2,3,5,3,4,2,3]}),
    "Tablet assay (%)": pd.DataFrame({"Tablet assay (%)": [98.4,99.1,97.8,100.2,98.9,99.4,101.1,97.5,98.7,99.8,100.4,96.9,99.2,98.1,100.0,101.5,97.9,98.6,99.7,100.8,98.3,99.0,97.2,100.1,99.5,98.8,101.0,97.7,99.3,100.5]}),
    "Dissolution at 30 min (%)": pd.DataFrame({"Dissolution at 30 min (%)": [72,75,78,80,82,84,85,86,87,88,88,89,90,91,92,93,94,95,96,96,97,98,99,100,83,87,91,94,76,89]}),
    "Number of adverse-event reports per day": pd.DataFrame({"Reports per day": [0,1,0,2,1,0,3,1,2,0,1,1,0,4,2,1,0,2,1,0,3,1,0,1,2,0,1,2,0,1]}),
}
choice = st.selectbox("Dataset", list(datasets.keys()))
df = datasets[choice]
col = df.columns[0]
values = df[col].astype(float).to_numpy()
st.write(f"**{len(df)} observations** in the selected synthetic dataset.")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("2. Decide whether to group the data")
kind = st.radio(
    "Which frequency table would you create?",
    ["Ungrouped frequency distribution", "Grouped frequency distribution"],
    index=None,
)
if st.button("Check my choice"):
    distinct = len(np.unique(values))
    if kind is None:
        st.warning("Choose an option first.")
    elif distinct <= 10 and kind.startswith("Ungrouped"):
        st.success(f"Reasonable choice. This dataset has {distinct} distinct values, so listing each value is clear.")
    elif distinct > 10 and kind.startswith("Grouped"):
        st.success(f"Reasonable choice. This dataset has {distinct} distinct values; grouping can make the overall pattern easier to see.")
    else:
        st.info(f"Your choice can still be useful depending on the purpose. There are {distinct} distinct values. For this activity, prefer {'ungrouped' if distinct <= 10 else 'grouped'} to keep the table readable.")

st.subheader("3. Generate a frequency distribution")
method = st.radio("Table type", ["Ungrouped", "Grouped"], horizontal=True)
if method == "Ungrouped":
    freq = df[col].value_counts().sort_index()
    out = pd.DataFrame({col: freq.index, "Frequency": freq.values})
    out["Relative frequency"] = out["Frequency"] / len(df)
    out["Percentage (%)"] = 100 * out["Relative frequency"]
    st.dataframe(out, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots()
    ax.bar(out[col].astype(str), out["Frequency"])
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.set_title("Ungrouped frequency distribution")
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig)
else:
    if np.all(np.isclose(values, np.round(values))) and len(np.unique(values)) <= 10:
        st.caption("This dataset has relatively few distinct integer values. Grouping is possible, but an ungrouped table may be easier to interpret.")

    interval_method = st.radio(
        "How would you like to define the class intervals?",
        ["Choose number of intervals", "Choose class width and starting boundary"],
        horizontal=True,
        key="interval_method",
    )

    data_min = float(np.min(values))
    data_max = float(np.max(values))
    data_range = data_max - data_min

    if interval_method == "Choose number of intervals":
        default_bins = min(8, max(3, int(np.sqrt(len(values)))))
        bins = st.slider("Number of class intervals", min_value=3, max_value=12, value=default_bins)
        edges = np.histogram_bin_edges(values, bins=bins)
        st.caption(f"The software calculates the class width automatically (approximately {edges[1] - edges[0]:.3g}).")
    else:
        suggested_width = data_range / min(6, max(3, int(np.sqrt(len(values)))))
        if suggested_width <= 0:
            suggested_width = 1.0
        width = st.number_input(
            "Class width",
            min_value=max(data_range / 1000, 0.001),
            max_value=max(data_range * 2, 1.0),
            value=float(suggested_width),
            step=float(max(data_range / 100, 0.1)),
            format="%.3f",
            help="The difference between the lower and upper boundaries of each class.",
            key="custom_class_width",
        )
        suggested_start = float(np.floor(data_min / width) * width)
        start = st.number_input(
            "Starting lower boundary",
            value=suggested_start,
            step=float(width),
            format="%.3f",
            help="Choose the lower boundary of the first class. It should be at or below the smallest observation.",
            key="custom_class_start",
        )

        if start > data_min:
            st.warning("The starting lower boundary is above the smallest observation. The first class will be extended downward so every observation is included.")
            start = float(start - np.ceil((start - data_min) / width) * width)

        number_needed = max(1, int(np.ceil((data_max - start) / width)))
        edges = start + np.arange(number_needed + 1, dtype=float) * width
        if edges[-1] < data_max:
            edges = np.append(edges, edges[-1] + width)

        st.caption(f"Using class width {width:g}, starting at {start:g}, across {len(edges) - 1} intervals.")

    counts, edges = np.histogram(values, bins=edges)
    out = pd.DataFrame({
        "Class interval": [f"{edges[i]:.3f} – {edges[i+1]:.3f}" for i in range(len(counts))],
        "Lower boundary": edges[:-1],
        "Upper boundary": edges[1:],
        "Frequency": counts,
        "Relative frequency": counts / len(values),
        "Percentage (%)": 100 * counts / len(values),
    })
    st.dataframe(out, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots()
    ax.hist(values, bins=edges, edgecolor="black")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.set_title("Grouped frequency distribution (histogram)")
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig)
    st.caption("Class intervals are contiguous. Values on a shared boundary are assigned consistently; the final interval includes the maximum value.")

st.subheader("4. Practice")
st.write("A batch contains 12 tablets with assay results (%): 98, 99, 98, 100, 99, 98, 101, 99, 100, 98, 99, 100.")
ans = st.radio("How many tablets have assay 98%?", ["2", "3", "4", "5"], index=None, key="freq_practice")
if st.button("Check practice answer"):
    if ans == "4":
        st.success("Correct. The value 98 occurs four times.")
    elif ans is None:
        st.warning("Choose an answer first.")
    else:
        st.error("Not quite. Count the number of occurrences of 98 in the raw list.")

st.subheader("Key interpretation")
st.markdown("""
A frequency table tells us how observations are distributed across values or intervals. Relative
frequency and percentage express the counts in relation to the total. Tables and graphs should be
chosen to suit the variable type and the question being asked.
""")
