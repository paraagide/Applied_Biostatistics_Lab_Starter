import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

st.set_page_config(page_title="Lesson 5: Central Tendency", page_icon="📍", layout="wide")
st.title("📍 Lesson 5: Measures of Central Tendency")
st.write("Learn why central tendency is useful, compare the mean, median and mode, and practise selecting and calculating a suitable measure.")
st.info("The supplied health-record workbook is a synthetic teaching dataset, not real patient data.")

with st.expander("Learning objectives", expanded=False):
    st.markdown("""
    - Explain why a dataset is summarised by a measure of central tendency.
    - Calculate and interpret mean, median and mode.
    - Select a measure appropriate to the variable and distribution.
    - Explore how outliers and skewness affect the mean and median.
    - Create a frequency distribution and graph from a random sample.
    """)

st.header("1. Brief notes: why do we need central tendency?")
st.markdown("""
A dataset may contain dozens, hundreds or thousands of observations. A **measure of central tendency**
provides a single representative value that helps summarise and communicate where observations tend to lie.
It supports comparisons between groups or batches. However, it should be interpreted alongside variability,
sample size, distribution shape and the context of the measurement.
""")
notes = pd.DataFrame([
    {"Measure":"Arithmetic mean","How calculated":"Sum of numerical observations divided by their number.",
     "Useful when":"Numerical data are reasonably symmetric and extreme values do not dominate.",
     "Strength":"Uses every numerical observation; useful in further statistical calculations.",
     "Limitation":"Sensitive to extreme values and skewed distributions.",
     "Example":"Mean tablet assay (%) in a batch."},
    {"Measure":"Median","How calculated":"Sort values; take the middle value, or average the two middle values.",
     "Useful when":"Data are skewed or contain extreme values; also useful for ordinal data.",
     "Strength":"Usually resistant to a small number of extreme values.",
     "Limitation":"Does not use the magnitude of every observation in the same way as the mean.",
     "Example":"Median hospital length of stay."},
    {"Measure":"Mode","How calculated":"Value or category that occurs most frequently.",
     "Useful when":"Finding the most common value/category; works with nominal data.",
     "Strength":"Can summarise categorical data and identifies the most frequent response.",
     "Limitation":"There may be ties, multiple modes or no useful unique mode.",
     "Example":"Most common blood group or tablet defect."},
])
st.dataframe(notes, use_container_width=True, hide_index=True)
st.caption("No measure is best in every situation. Consider measurement scale, distribution and the question being asked.")
with st.expander("Formula reminders"):
    st.latex(r"\\bar{x}=\\frac{\\sum_{i=1}^{n}x_i}{n}")
    st.markdown("- **Mean:** sum of values divided by n.\n- **Median:** middle value(s) after sorting.\n- **Mode:** value or category with the highest frequency.")

st.header("2. Guided demonstration: compare the measures")
DATASETS = {
    "Tablet assay (%)": {"values":[98.1,99.2,97.8,98.7,99.0,98.4,97.9,98.8,99.1,98.5,98.2,99.0,98.6,97.7,98.9,98.3,99.2,98.4,98.7,98.5],"description":"Synthetic tablet assay results.","unit":"%"},
    "Dissolution at 30 min (%)": {"values":[62,65,67,68,69,70,70,71,72,72,73,74,74,75,76,77,78,80,82,85],"description":"Synthetic percentage dissolved at 30 minutes.","unit":"%"},
    "Hospital length of stay (days)": {"values":[1,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,7,8,10,18],"description":"Synthetic hospital length-of-stay observations.","unit":"days"},
    "Adverse-event reports per day": {"values":[0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,7,8,9,12],"description":"Synthetic daily counts of reports.","unit":"reports"},
}
demo_name = st.selectbox("Choose a demonstration dataset", list(DATASETS.keys()))
demo = DATASETS[demo_name]
st.caption(demo["description"])
demo_values = np.array(demo["values"], dtype=float)
if st.checkbox("Edit demonstration observations", key="edit_demo"):
    edf = pd.DataFrame({"Observation":np.arange(1,len(demo_values)+1),"Value":demo_values})
    edf = st.data_editor(edf, num_rows="dynamic", use_container_width=True, key="demo_editor")
    demo_values = pd.to_numeric(edf["Value"], errors="coerce").dropna().to_numpy(dtype=float)
if st.checkbox("Add an extreme observation", key="outlier_demo") and len(demo_values):
    span = max(float(np.max(demo_values)-np.min(demo_values)),1.0)
    extreme = st.number_input("Added extreme value", value=float(np.max(demo_values)+5*span), step=float(span), key="demo_extreme_value")
    demo_values = np.append(demo_values, extreme)

def show_measures(values, title, xlabel="Value"):
    vals = np.asarray(values, dtype=float)
    vals = vals[np.isfinite(vals)]
    if len(vals)==0:
        st.warning("No valid numeric observations to analyse.")
        return
    mean_v, median_v = float(np.mean(vals)), float(np.median(vals))
    mode_result = stats.mode(vals, keepdims=False)
    mode_v, mode_n = float(mode_result.mode), int(mode_result.count)
    c1,c2,c3=st.columns(3)
    c1.metric("Mean",f"{mean_v:.3f}")
    c2.metric("Median",f"{median_v:.3f}")
    c3.metric("Mode",f"{mode_v:g} ({mode_n} occurrence{'s' if mode_n!=1 else ''})")
    fig,ax=plt.subplots()
    ax.hist(vals,bins="auto",edgecolor="black")
    ax.axvline(mean_v,linestyle="--",linewidth=2,label=f"Mean = {mean_v:.2f}")
    ax.axvline(median_v,linestyle="-.",linewidth=2,label=f"Median = {median_v:.2f}")
    ax.axvline(mode_v,linestyle=":",linewidth=2,label=f"Mode = {mode_v:g}")
    ax.set_xlabel(xlabel); ax.set_ylabel("Frequency"); ax.set_title(title); ax.legend(); ax.grid(axis="y",alpha=.2)
    st.pyplot(fig); plt.close(fig)
    diff=mean_v-median_v
    if np.isclose(diff,0):
        st.write("The mean and median are equal or very close in this sample.")
    elif diff>0:
        st.write("The mean is greater than the median. Larger values may pull the mean upward; inspect the graph before deciding the distribution is right-skewed.")
    else:
        st.write("The mean is less than the median. Smaller values may pull the mean downward; inspect the graph before deciding the distribution is left-skewed.")

show_measures(demo_values,demo_name, demo.get("unit","Value"))
st.write("**Frequency table**")
st.dataframe(pd.Series(demo_values).value_counts().sort_index().rename_axis("Value").reset_index(name="Frequency"),use_container_width=True,hide_index=True)

st.header("3. Student lab: select, sample and analyse a variable from Excel")
st.write("Select a numeric variable, generate a random sample, build a frequency distribution, inspect its graph, choose a measure and check your calculation.")

project_file = Path(__file__).resolve().parent.parent / "data" / "Health_Records_Teaching_Dataset.xlsx"
source_choice = st.radio("Excel source",["Use workbook in project (if installed)","Upload an Excel workbook"],horizontal=True,key="ct_source_choice")
health_df=None
if source_choice=="Use workbook in project (if installed)":
    if project_file.exists():
        try:
            health_df=pd.read_excel(project_file)
            st.success(f"Loaded workbook: {len(health_df):,} rows and {len(health_df.columns)} columns.")
        except Exception as exc:
            st.error(f"Could not read workbook: {exc}")
    else:
        st.warning("The workbook is not in the project's data folder yet. You can upload it below or add it to data/ using the instructions provided with this file.")
else:
    uploaded=st.file_uploader("Upload .xlsx or .xls",type=["xlsx","xls"],key="ct_excel_upload")
    if uploaded is not None:
        try:
            health_df=pd.read_excel(uploaded)
            st.success(f"Loaded uploaded workbook: {len(health_df):,} rows and {len(health_df.columns)} columns.")
        except Exception as exc:
            st.error(f"Could not read this Excel file: {exc}")

if health_df is not None:
    numeric_cols=[c for c in health_df.select_dtypes(include="number").columns if health_df[c].dropna().nunique()>1]
    if not numeric_cols:
        st.warning("No suitable numeric columns were found.")
    else:
        variable=st.selectbox("Select a numeric variable",numeric_cols,key="ct_excel_variable")
        available=health_df[variable].dropna().astype(float).to_numpy()
        st.caption(f"{len(available):,} non-missing observations are available for {variable}.")
        if len(available)>=2:
            max_n=int(len(available))
            default_n=min(100,max_n)
            sample_size=st.slider("Sample size",min_value=2,max_value=max_n,value=default_n,key="ct_excel_n")
            seed=st.number_input("Random seed (change to generate a different sample)",min_value=0,max_value=999999,value=42,step=1,key="ct_excel_seed")
            if st.button("Generate random sample",type="primary",key="ct_generate_sample"):
                rng=np.random.default_rng(int(seed))
                st.session_state["ct_lab_sample"]=rng.choice(available,size=int(sample_size),replace=False)
                st.session_state["ct_lab_variable"]=variable
                for k in ["ct_shape_answer","ct_measure_answer","ct_numeric_answer"]:
                    st.session_state.pop(k,None)
            if "ct_lab_sample" in st.session_state and st.session_state.get("ct_lab_variable")==variable:
                sample=np.asarray(st.session_state["ct_lab_sample"],dtype=float)
                st.success(f"Sample ready: n = {len(sample)} for {variable}.")
                with st.expander("View sampled observations"):
                    st.dataframe(pd.DataFrame({"Observation":np.arange(1,len(sample)+1),variable:sample}),use_container_width=True,hide_index=True)

                st.subheader("3A. Create the frequency distribution")
                dist_type=st.radio("Frequency table type",["Ungrouped frequency table","Grouped frequency distribution"],horizontal=True,key="ct_lab_distribution_type")
                edges=None
                if dist_type=="Ungrouped frequency table":
                    freq=pd.Series(sample).value_counts().sort_index()
                    lab_table=freq.rename_axis("Value").reset_index(name="Frequency")
                    lab_table["Relative frequency"]=lab_table["Frequency"]/len(sample)
                    lab_table["Percentage (%)"]=100*lab_table["Relative frequency"]
                else:
                    method=st.radio("Define class intervals by",["Number of intervals","Class width and starting boundary"],horizontal=True,key="ct_lab_interval_method")
                    dmin,dmax=float(np.min(sample)),float(np.max(sample)); drange=dmax-dmin
                    if method=="Number of intervals":
                        bins=st.slider("Number of class intervals",min_value=2,max_value=min(20,max(2,len(sample))),value=min(6,max(2,int(np.sqrt(len(sample))))),key="ct_lab_bins")
                        edges=np.histogram_bin_edges(sample,bins=bins)
                    else:
                        default_width=drange/min(6,max(3,int(np.sqrt(len(sample)))))
                        if default_width<=0: default_width=1.0
                        width=st.number_input("Class width",min_value=max(drange/1000,.001),max_value=max(drange*2,1.0),value=float(default_width),step=float(max(drange/100,.1)),format="%.3f",key="ct_lab_width")
                        start_default=float(np.floor(dmin/width)*width)
                        start=st.number_input("Starting lower boundary",value=start_default,step=float(width),format="%.3f",key="ct_lab_start")
                        if start>dmin:
                            start=float(start-np.ceil((start-dmin)/width)*width)
                            st.warning("Starting boundary adjusted downward so all observations are included.")
                        n_intervals=max(1,int(np.ceil((dmax-start)/width)))
                        edges=start+np.arange(n_intervals+1)*width
                        if edges[-1]<dmax: edges=np.append(edges,edges[-1]+width)
                    counts,edges=np.histogram(sample,bins=edges)
                    lab_table=pd.DataFrame({"Class interval":[f"{edges[i]:.3f} – {edges[i+1]:.3f}" for i in range(len(counts))],
                        "Lower boundary":edges[:-1],"Upper boundary":edges[1:],"Frequency":counts,
                        "Relative frequency":counts/len(sample),"Percentage (%)":100*counts/len(sample)})
                st.dataframe(lab_table,use_container_width=True,hide_index=True)

                st.subheader("3B. Graph and interpret the distribution")
                fig,ax=plt.subplots()
                if dist_type=="Ungrouped frequency table":
                    ax.bar(lab_table["Value"].astype(str),lab_table["Frequency"],edgecolor="black")
                    ax.set_xlabel(variable); ax.tick_params(axis="x",rotation=45)
                else:
                    ax.hist(sample,bins=edges,edgecolor="black"); ax.set_xlabel(variable)
                ax.set_ylabel("Frequency"); ax.set_title(f"{variable} (n={len(sample)})"); ax.grid(axis="y",alpha=.2)
                st.pyplot(fig); plt.close(fig)
                shape_answer=st.radio("Which description best fits the graph?",["Approximately symmetric","Right-skewed (long tail to larger values)","Left-skewed (long tail to smaller values)","Cannot tell from this graph"],index=None,key="ct_shape_answer")
                if st.button("Check distribution-shape answer",key="ct_check_shape"):
                    skew=float(stats.skew(sample,bias=False)) if len(sample)>=3 and np.std(sample)>0 else 0.0
                    expected=("Right-skewed (long tail to larger values)" if skew>.5 else "Left-skewed (long tail to smaller values)" if skew<-.5 else "Approximately symmetric")
                    if shape_answer==expected:
                        st.success(f"Correct under this simplified rule. Sample skewness = {skew:.3f}.")
                    else:
                        st.info(f"Reference answer: **{expected}**. Sample skewness = {skew:.3f}. This rule uses > 0.5 for right skew, < -0.5 for left skew, and otherwise approximately symmetric.")
                    st.caption("Skewness is a guide, not a substitute for inspecting the graph; samples may not fit a category perfectly.")

                st.subheader("3C. Choose a suitable measure")
                measure_answer=st.radio("Which measure would you choose as the main summary?",["Mean","Median","Mode"],index=None,key="ct_measure_answer")
                if st.button("Check measure choice",key="ct_check_measure"):
                    skew=float(stats.skew(sample,bias=False)) if len(sample)>=3 and np.std(sample)>0 else 0.0
                    preferred="Median" if abs(skew)>.5 else "Mean"
                    rationale=("The sample is noticeably skewed by the simplified rule, so the median is often a robust summary." if preferred=="Median" else "The sample is approximately symmetric by the simplified rule, so the mean is a reasonable summary.")
                    if measure_answer==preferred: st.success(f"Reasonable choice under this rule. {rationale}")
                    else: st.warning(f"Reference choice: **{preferred}**. {rationale} The best measure also depends on the question; more than one choice can sometimes be defended.")
                    st.caption("If the question asks for the most common value/category, the mode may be the most relevant measure.")

                st.subheader("3D. Calculate and check your answer")
                answer_measure=st.selectbox("Choose which measure you will calculate",["Mean","Median","Mode"],key="ct_numeric_measure")
                numeric_answer=st.number_input("Enter your calculated value",value=0.0,format="%.6f",key="ct_numeric_answer")
                if st.button("Check my calculated answer",key="ct_check_numeric"):
                    if answer_measure=="Mean": correct=float(np.mean(sample))
                    elif answer_measure=="Median": correct=float(np.median(sample))
                    else: correct=float(stats.mode(sample,keepdims=False).mode)
                    tolerance=max(.01,abs(correct)*.005)
                    if abs(numeric_answer-correct)<=tolerance: st.success(f"Correct. Sample {answer_measure.lower()} = {correct:.4f}.")
                    else: st.error(f"Not quite. Sample {answer_measure.lower()} = {correct:.4f}. Check your arithmetic and rounding.")
                    st.caption("If multiple values tie for the mode, the reference answer displays one of the tied values.")
        else:
            st.warning("At least two non-missing numeric observations are required.")

st.header("4. Quick knowledge check")
st.write("For the five observations 96, 98, 98, 99, 100:")
q1=st.radio("What is the median?",["96","98","98.2","99"],index=None,key="ct_q1")
q2=st.radio("Which measure is generally less affected by one very large outlier?",["Mean","Median","Both equally","Neither"],index=None,key="ct_q2")
q3=st.radio("Which measure identifies the most frequently occurring value or category?",["Mean","Median","Mode","Range"],index=None,key="ct_q3")
if st.button("Check knowledge-check answers",type="primary",key="ct_final_quiz"):
    answers=[(q1,"98","The middle value is 98."),(q2,"Median","The median is usually less affected by a single extreme value."),(q3,"Mode","The mode is the most frequently occurring value or category.")]
    score=0
    for i,(selected,correct,explanation) in enumerate(answers,1):
        if selected==correct: score+=1; st.success(f"Question {i}: Correct. {explanation}")
        else: st.error(f"Question {i}: Correct answer: {correct}. {explanation}")
    st.metric("Knowledge-check score",f"{score}/3")
st.divider()
st.markdown("**Key takeaway:** The mean uses every numerical value and is sensitive to extremes; the median is often more robust to outliers; the mode identifies the most frequent value or category. Choose a measure that fits the data and the question.")
