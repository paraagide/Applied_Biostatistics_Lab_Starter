import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Lesson 6: Measures of Dispersion", page_icon="📏", layout="wide")
st.title("📏 Lesson 6: Measures of Dispersion")
st.write("Explore how spread out observations are, even when two datasets have similar means.")
st.info("All examples are synthetic teaching data, not real patient records.")

with st.expander("Learning objectives", expanded=False):
    st.markdown("""
    - Explain why central tendency alone is not enough to describe a dataset.
    - Calculate range, interquartile range (IQR), variance and standard deviation.
    - Distinguish population and sample variance/standard deviation.
    - Compare datasets with similar means but different variability.
    - Analyse a random sample from an Excel workbook.
    """)

st.header("1. Brief notes: why measure dispersion?")
st.markdown("""
A measure of central tendency describes a typical or central value, but not whether observations are
tightly clustered or widely spread. Two pharmaceutical batches can have the same mean assay while one
batch is much more variable. Dispersion measures help describe consistency and variability.
""")
summary = pd.DataFrame([
    {"Measure":"Range","Calculation":"Maximum − minimum","Interpretation":"Total span of observed values","Strength":"Simple to calculate","Limitation":"Uses only extremes; sensitive to outliers"},
    {"Measure":"Interquartile range (IQR)","Calculation":"Q3 − Q1","Interpretation":"Spread of the middle 50%","Strength":"Resistant to extreme values","Limitation":"Does not describe tail spread"},
    {"Measure":"Population variance (σ²)","Calculation":"Σ(x − μ)² ÷ N","Interpretation":"Mean squared deviation in a population","Strength":"Uses all observations","Limitation":"Units are squared"},
    {"Measure":"Sample variance (s²)","Calculation":"Σ(x − x̄)² ÷ (n − 1)","Interpretation":"Estimates population variance from a sample","Strength":"Usual unbiased estimator under standard assumptions","Limitation":"Units are squared"},
    {"Measure":"Standard deviation (SD)","Calculation":"Square root of variance","Interpretation":"Spread in the original measurement units","Strength":"Often easier to interpret than variance","Limitation":"Sensitive to extreme values"},
])
st.dataframe(summary, use_container_width=True, hide_index=True)
with st.expander("Formula reminders"):
    st.image(
    "assets/dispersion_formula_reminders.png",
    caption="Formulae reference: Central Tendency and Dispersion",
    use_container_width=True
)
st.header("2. Compare two datasets with similar means")
sets = {
    "Batch A — lower variability": np.array([98,99,99,100,100,100,101,101,102], dtype=float),
    "Batch B — higher variability": np.array([90,94,97,99,100,101,103,106,110], dtype=float),
}
chosen = st.multiselect("Choose datasets to compare", list(sets.keys()), default=list(sets.keys()))
if chosen:
    rows=[]
    fig, ax = plt.subplots()
    for name in chosen:
        x=sets[name]
        rows.append({"Dataset":name,"n":len(x),"Mean":np.mean(x),"Median":np.median(x),
                     "Range":np.ptp(x),"IQR":np.percentile(x,75)-np.percentile(x,25),
                     "Sample variance (n−1)":np.var(x,ddof=1),"Sample SD (n−1)":np.std(x,ddof=1)})
        ax.hist(x,bins=np.arange(88,113,4),alpha=.55,edgecolor="black",label=name)
    ax.set_xlabel("Value"); ax.set_ylabel("Frequency"); ax.set_title("Compare the distributions"); ax.legend()
    ax.grid(axis="y",alpha=.2); st.pyplot(fig); plt.close(fig)
    st.dataframe(pd.DataFrame(rows).round(3),use_container_width=True,hide_index=True)
    st.write("Similar means do not imply similar variability. Compare the range, IQR and standard deviation.")

st.header("3. Explore the effect of changing observations")
base=[98,99,99,100,100,100,101,101,102]
if st.checkbox("Edit example observations",key="disp_edit"):
    edit=pd.DataFrame({"Observation":np.arange(1,len(base)+1),"Value":base})
    edit=st.data_editor(edit,num_rows="dynamic",use_container_width=True,key="disp_editor")
    values=pd.to_numeric(edit["Value"],errors="coerce").dropna().to_numpy(dtype=float)
else:
    values=np.array(base,dtype=float)
if st.checkbox("Add an extreme observation",key="disp_outlier") and len(values):
    span=max(float(np.ptp(values)),1.0)
    extra=st.number_input("Extreme observation",value=float(np.max(values)+5*span),step=float(span),key="disp_extreme_value")
    values=np.append(values,extra)
if len(values)>=2:
    q1,q3=np.percentile(values,[25,75])
    c=st.columns(5)
    c[0].metric("Range",f"{np.ptp(values):.3f}")
    c[1].metric("IQR",f"{q3-q1:.3f}")
    c[2].metric("Sample variance",f"{np.var(values,ddof=1):.3f}")
    c[3].metric("Sample SD",f"{np.std(values,ddof=1):.3f}")
    c[4].metric("Population SD",f"{np.std(values,ddof=0):.3f}")
    fig,ax=plt.subplots(); ax.boxplot(values,vert=False); ax.set_xlabel("Value"); ax.set_title("Boxplot of observations")
    ax.grid(axis="x",alpha=.2); st.pyplot(fig); plt.close(fig)
else:
    st.warning("Enter at least two valid numeric observations.")

st.header("4. Student lab: calculate dispersion from Excel")
st.write("Choose a numeric variable, draw a random sample, create a frequency distribution and graph, then calculate a dispersion measure.")
project_file=Path(__file__).resolve().parent.parent/"data"/"Health_Records_Teaching_Dataset.xlsx"
source=st.radio("Excel source",["Use workbook in project (if installed)","Upload an Excel workbook"],horizontal=True,key="disp_source")
df=None
if source=="Use workbook in project (if installed)":
    if project_file.exists():
        try:
            df=pd.read_excel(project_file)
            st.success(f"Loaded workbook: {len(df):,} rows and {len(df.columns)} columns.")
        except Exception as exc: st.error(f"Could not read workbook: {exc}")
    else: st.warning("Workbook not found in data/. Add it to the project or choose the upload option.")
else:
    upload=st.file_uploader("Upload .xlsx or .xls",type=["xlsx","xls"],key="disp_upload")
    if upload is not None:
        try:
            df=pd.read_excel(upload)
            st.success(f"Loaded workbook: {len(df):,} rows and {len(df.columns)} columns.")
        except Exception as exc: st.error(f"Could not read workbook: {exc}")

if df is not None:
    cols=[c for c in df.select_dtypes(include="number").columns if df[c].dropna().nunique()>1]
    if not cols: st.warning("No suitable numeric columns found.")
    else:
        variable=st.selectbox("Select a numeric variable",cols,key="disp_variable")
        available=df[variable].dropna().astype(float).to_numpy()
        st.caption(f"{len(available):,} non-missing observations available.")
        if len(available)>=2:
            n=st.slider("Sample size",2,int(len(available)),min(100,int(len(available))),key="disp_n")
            seed=st.number_input("Random seed",0,999999,42,step=1,key="disp_seed")
            if st.button("Generate random sample",type="primary",key="disp_generate"):
                st.session_state["disp_sample"]=np.random.default_rng(int(seed)).choice(available,size=int(n),replace=False)
                st.session_state["disp_variable_saved"]=variable
            if "disp_sample" in st.session_state and st.session_state.get("disp_variable_saved")==variable:
                sample=np.asarray(st.session_state["disp_sample"],dtype=float)
                st.success(f"Sample generated: n = {len(sample)}.")
                with st.expander("View sampled observations"):
                    st.dataframe(pd.DataFrame({"Observation":np.arange(1,len(sample)+1),variable:sample}),use_container_width=True,hide_index=True)
                st.subheader("4A. Frequency distribution")
                typ=st.radio("Table type",["Ungrouped frequency table","Grouped frequency distribution"],horizontal=True,key="disp_table_type")
                edges=None
                if typ=="Ungrouped frequency table":
                    freq=pd.Series(sample).value_counts().sort_index()
                    table=freq.rename_axis("Value").reset_index(name="Frequency")
                    table["Relative frequency"]=table["Frequency"]/len(sample)
                    table["Percentage (%)"]=100*table["Relative frequency"]
                else:
                    method=st.radio("Define intervals by",["Number of intervals","Class width and starting boundary"],horizontal=True,key="disp_method")
                    lo,hi=float(np.min(sample)),float(np.max(sample)); span=hi-lo
                    if method=="Number of intervals":
                        bins=st.slider("Number of intervals",2,min(20,max(2,len(sample))),min(6,max(2,int(np.sqrt(len(sample))))),key="disp_bins")
                        edges=np.histogram_bin_edges(sample,bins=bins)
                    else:
                        default_width=span/min(6,max(3,int(np.sqrt(len(sample)))))
                        if default_width<=0: default_width=1.0
                        width=st.number_input("Class width",min_value=max(span/1000,.001),max_value=max(span*2,1.0),value=float(default_width),step=float(max(span/100,.1)),format="%.3f",key="disp_width")
                        start=st.number_input("Starting lower boundary",value=float(np.floor(lo/width)*width),step=float(width),format="%.3f",key="disp_start")
                        if start>lo:
                            start=float(start-np.ceil((start-lo)/width)*width)
                            st.warning("Starting boundary adjusted downward to include all observations.")
                        count=max(1,int(np.ceil((hi-start)/width)))
                        edges=start+np.arange(count+1)*width
                        if edges[-1]<hi: edges=np.append(edges,edges[-1]+width)
                    counts,edges=np.histogram(sample,bins=edges)
                    table=pd.DataFrame({"Class interval":[f"{edges[i]:.3f} – {edges[i+1]:.3f}" for i in range(len(counts))],
                        "Lower boundary":edges[:-1],"Upper boundary":edges[1:],"Frequency":counts,
                        "Relative frequency":counts/len(sample),"Percentage (%)":100*counts/len(sample)})
                st.dataframe(table,use_container_width=True,hide_index=True)
                fig,ax=plt.subplots()
                if typ=="Ungrouped frequency table":
                    ax.bar(table["Value"].astype(str),table["Frequency"],edgecolor="black"); ax.set_xlabel(variable); ax.tick_params(axis="x",rotation=45)
                else:
                    ax.hist(sample,bins=edges,edgecolor="black"); ax.set_xlabel(variable)
                ax.set_ylabel("Frequency"); ax.set_title(f"{variable} (n={len(sample)})"); ax.grid(axis="y",alpha=.2)
                st.pyplot(fig); plt.close(fig)
                st.subheader("4B. Calculate and check your answer")
                measure=st.selectbox("Choose a dispersion measure",["Range","IQR","Sample variance (n−1)","Sample standard deviation (n−1)","Population variance (N)","Population standard deviation (N)"],key="disp_measure")
                entered=st.number_input("Enter your calculated answer",value=0.0,format="%.6f",key="disp_answer")
                if st.button("Check my answer",key="disp_check"):
                    if measure=="Range": correct=float(np.ptp(sample))
                    elif measure=="IQR": correct=float(np.percentile(sample,75)-np.percentile(sample,25))
                    elif measure=="Sample variance (n−1)": correct=float(np.var(sample,ddof=1))
                    elif measure=="Sample standard deviation (n−1)": correct=float(np.std(sample,ddof=1))
                    elif measure=="Population variance (N)": correct=float(np.var(sample,ddof=0))
                    else: correct=float(np.std(sample,ddof=0))
                    if abs(entered-correct)<=max(.01,abs(correct)*.005): st.success(f"Correct. {measure} = {correct:.4f}.")
                    else: st.error(f"Not quite. Correct value: {correct:.4f}. Check the formula and rounding.")
        else: st.warning("At least two numeric observations are required.")

st.header("5. Quick knowledge check")
q1=st.radio("Which measure describes the spread of the middle 50%?",["Range","IQR","Mean","Mode"],index=None,key="disp_q1")
q2=st.radio("For the usual sample variance estimator, which denominator is used?",["n","n−1","n+1","N²"],index=None,key="disp_q2")
q3=st.radio("Which measure is expressed in the original measurement units?",["Variance","Standard deviation","Squared deviation","None"],index=None,key="disp_q3")
if st.button("Check knowledge-check answers",type="primary",key="disp_quiz"):
    items=[(q1,"IQR","IQR = Q3 − Q1 and describes the middle 50%."),(q2,"n−1","The usual sample variance estimator uses n−1."),(q3,"Standard deviation","SD is the square root of variance and has the original units.")]
    score=0
    for i,(selected,correct,explanation) in enumerate(items,1):
        if selected==correct: score+=1; st.success(f"Question {i}: Correct. {explanation}")
        else: st.error(f"Question {i}: Correct answer: {correct}. {explanation}")
    st.metric("Knowledge-check score",f"{score}/3")

st.divider()
st.markdown("**Key takeaway:** Dispersion complements central tendency. Describe numerical data using an appropriate centre and measure of spread.")
