import random
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Unit I | Variables & Scales", page_icon="📊", layout="wide")
st.title("Unit I — Descriptive Statistics")
st.subheader("Lessons 1–2: Variables and Measurement Scales")
st.caption("Applied Biostatistics and Data Analytics for Pharmaceutical Sciences")

st.markdown("""
A **variable** is a characteristic that can take different values across people, samples, batches,
or observations. Examples in pharmacy include dosage form, blood pressure, tablet hardness,
drug concentration, and number of adverse-event reports.
""")

with st.expander("Learning objectives", expanded=True):
    st.markdown("""
    - Distinguish categorical variables from numerical variables.
    - Distinguish discrete numerical variables from continuous numerical variables.
    - Identify nominal, ordinal, interval, and ratio scales.
    - Explain why variable type and scale influence meaningful summaries and analyses.
    """)

st.header("Lesson 1 — Types of variables")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Categorical variables")
    st.write("Values are labels or groups rather than quantities to be added or averaged.")
    st.markdown("- Dosage form: tablet, capsule, suspension\n- Blood group\n- Adverse-event type\n- Treatment group\n- Route of administration\n- Batch release status")
with c2:
    st.subheader("Numerical variables")
    st.write("Values represent counts or measurements.")
    st.markdown("**Discrete:** counts, usually whole numbers. Examples: tablets rejected, adverse-event reports, hospital visits.\n\n**Continuous:** measurements that can vary across a continuum. Examples: plasma concentration, body weight, dissolution time, tablet hardness.")

st.info("A number used as a label is not automatically a numerical measurement. A patient ID or batch number is an identifier; arithmetic on it is not meaningful.")

VARIABLES = [
("Dosage form","Categorical","Tablet, capsule and suspension are labels."),
("Blood group","Categorical","A, B, AB and O are categories."),
("Adverse-event type","Categorical","Nausea, headache and rash are labels."),
("Treatment allocation","Categorical","Placebo and active-treatment groups are categories."),
("Tablet coating type","Categorical","Coating types are categories."),
("Manufacturer name","Categorical","Names are labels."),
("Batch release status","Categorical","Pass, fail and hold are categories."),
("Route of administration","Categorical","Oral, topical and intravenous are categories."),
("Diagnosis category","Categorical","Diagnosis labels are categories."),
("Clinical response status","Categorical","Responder/non-responder is a category."),
("Number of tablets rejected in a batch","Discrete numerical","This is a count."),
("Number of adverse-event reports in a week","Discrete numerical","This is a count over a defined period."),
("Number of hospital visits","Discrete numerical","Visits are counted."),
("Number of doses missed","Discrete numerical","Missed doses are counted."),
("Number of colonies on a plate","Discrete numerical","Colonies are counted."),
("Number of patients responding to treatment","Discrete numerical","Responders are counted."),
("Number of medication errors in a shift","Discrete numerical","Errors are counted."),
("Number of repeat tests required","Discrete numerical","Repeat tests are counted."),
("Number of protocol deviations","Discrete numerical","Deviations are counted."),
("Number of participants enrolled","Discrete numerical","Participants are counted."),
("Body weight","Continuous numerical","Weight is measured on a continuum."),
("Height","Continuous numerical","Height is measured on a continuum."),
("Systolic blood pressure","Continuous numerical","Blood pressure is measured quantitatively."),
("Plasma drug concentration","Continuous numerical","Concentration is a measurement."),
("Dissolution time","Continuous numerical","Time is measured on a continuum."),
("Drug content in a tablet","Continuous numerical","Content is measured quantitatively."),
("Tablet hardness","Continuous numerical","Hardness is measured quantitatively."),
("Tablet thickness","Continuous numerical","Thickness is measured quantitatively."),
("pH of a solution","Continuous numerical","pH is numerical; its logarithmic nature matters in interpretation."),
("Area under the concentration-time curve","Continuous numerical","AUC is a pharmacokinetic measurement."),
("Peak plasma concentration","Continuous numerical","Cmax is a quantitative measurement."),
("Time to peak concentration","Continuous numerical","Time is measured quantitatively."),
("Creatinine concentration","Continuous numerical","Concentration is measured quantitatively."),
("Glucose concentration","Continuous numerical","Concentration is measured quantitatively."),
("Dissolution percentage at 30 minutes","Continuous numerical","Percentage dissolution is measured quantitatively."),
("Powder moisture content","Continuous numerical","Moisture content is measured quantitatively."),
("Granule particle size","Continuous numerical","Particle size is measured."),
("Formulation viscosity","Continuous numerical","Viscosity is measured quantitatively."),
("Tablet disintegration time","Continuous numerical","Time is measured quantitatively."),
("Drug loading percentage","Continuous numerical","Loading percentage is measured quantitatively."),
("Number of prescriptions dispensed","Discrete numerical","Prescriptions are counted."),
("Number of tablets in a pack","Discrete numerical","Tablets are counted."),
("Number of positive cultures","Discrete numerical","Positive cultures are counted."),
("Number of doses administered","Discrete numerical","Doses are counted."),
("Number of samples passing assay limits","Discrete numerical","Passing samples are counted."),
("Number of patients withdrawn from a trial","Discrete numerical","Patients are counted."),
("Number of medication orders with errors","Discrete numerical","Orders with errors are counted."),
("Study site","Categorical","Site names identify groups."),
("Packaging material type","Categorical","Material types are categories."),
("Stability outcome category","Categorical","Acceptable/out-of-specification are categories."),
("Tablet shape","Categorical","Shapes are labels."),
("Randomisation arm","Categorical","Trial arms are groups."),
("Dosage strength product category","Categorical","If used to identify a product category, it is a label."),
("Severity category of an adverse event","Categorical","Severity labels are ordered categories."),
("Number of capsules in a pack","Discrete numerical","Capsules are counted."),
("Number of adverse events per patient","Discrete numerical","Events are counted."),
("Drug mass in milligrams","Continuous numerical","Mass is measured quantitatively."),
]

st.subheader("Interactive variable identification")
st.write("Generate a variable, classify it, and check your answer.")
if "var_item" not in st.session_state:
    st.session_state.var_item = random.choice(VARIABLES)
if st.button("Generate a variable"):
    st.session_state.var_item = random.choice(VARIABLES)
vname, vtype, vreason = st.session_state.var_item
st.markdown(f"### Classify: **{vname}**")
vchoice = st.radio("Variable type", ["Categorical", "Discrete numerical", "Continuous numerical"], index=None, horizontal=True, key="vchoice")
if st.button("Check variable type"):
    if vchoice is None:
        st.warning("Choose an answer first.")
    elif vchoice == vtype:
        st.success(f"Correct! {vreason}")
    else:
        st.error(f"Best answer: **{vtype}**. {vreason}")
with st.expander("View the complete variable bank"):
    st.dataframe(pd.DataFrame(VARIABLES, columns=["Variable", "Type", "Explanation"]), use_container_width=True, hide_index=True)
    st.caption(f"{len(VARIABLES)} pharmaceutical and healthcare variables.")

st.divider()
st.header("Lesson 2 — Scales of measurement")
st.markdown("""
**Nominal:** categories without an inherent order. Examples: blood group, dosage form, manufacturer.

**Ordinal:** ordered categories, but gaps between categories are not guaranteed equal. Examples: mild/moderate/severe adverse-event severity; satisfaction from very dissatisfied to very satisfied.

**Interval:** equal intervals, but no true zero. Differences are meaningful, but ratios are not generally meaningful. Example: temperature in °C. A value of 20°C is not twice 10°C.

**Ratio:** equal intervals and a meaningful zero. Ratios can be meaningful. Examples: mass, height, elapsed time, concentration, and number of tablets.
""")
st.warning("pH is logarithmic, so it should not be treated as an ordinary interval-scale example without qualification. Also, numerical codes for categories do not automatically make the data interval or ratio.")

scales_table = [
{"Scale":"Nominal","Ordered?":"No","Equal intervals?":"No","True zero?":"Not applicable","Example":"Blood group"},
{"Scale":"Ordinal","Ordered?":"Yes","Equal intervals?":"Not guaranteed","True zero?":"Not applicable","Example":"Adverse-event severity"},
{"Scale":"Interval","Ordered?":"Yes","Equal intervals?":"Yes","True zero?":"No","Example":"Temperature in °C"},
{"Scale":"Ratio","Ordered?":"Yes","Equal intervals?":"Yes","True zero?":"Yes","Example":"Drug concentration"},
]
st.subheader("Quick comparison")
st.dataframe(pd.DataFrame(scales_table), use_container_width=True, hide_index=True)

SCALES = [
("Blood group","Nominal","Blood groups are categories without natural ranking."),
("Adverse-event severity: mild, moderate, severe","Ordinal","Categories are ordered; gaps are not necessarily equal."),
("Temperature in degrees Celsius","Interval","Differences are meaningful, but 0°C is not absence of temperature."),
("Plasma drug concentration","Ratio","Concentration has a meaningful zero."),
("Patient satisfaction from very dissatisfied to very satisfied","Ordinal","Response categories have an order."),
("Dosage form","Nominal","Tablet, capsule and solution are unordered labels."),
("Elapsed time to disintegration","Ratio","Time has a meaningful zero."),
("Body weight","Ratio","Weight has a meaningful zero."),
("Calendar year of manufacture","Interval","Year differences are meaningful, but year zero is not absence of time."),
("Number of tablets rejected","Ratio","A count has a meaningful zero."),
("Pain rating from 0 to 10","Ordinal","Often treated as ordinal; equal intervals should not be assumed automatically."),
("Temperature in Kelvin","Ratio","Kelvin has an absolute zero."),
("pH of a solution","Special case / needs qualification","pH is logarithmic; interpretation requires care."),
("Clinical response ranked poor, fair, good, excellent","Ordinal","Response categories are ordered."),
("Drug mass in milligrams","Ratio","Mass has a meaningful zero."),
("Manufacturer name","Nominal","Names are categories."),
("Batch release status: pass/fail","Nominal","These are categories."),
("Dissolution percentage","Ratio","A zero means no measured dissolution for the defined measure."),
]
st.subheader("Interactive measurement-scale practice")
if "scale_item" not in st.session_state:
    st.session_state.scale_item = random.choice(SCALES)
if st.button("Generate a scale question"):
    st.session_state.scale_item = random.choice(SCALES)
sname, stype, sreason = st.session_state.scale_item
st.markdown(f"### Identify the scale: **{sname}**")
schoice = st.radio("Measurement scale", ["Nominal", "Ordinal", "Interval", "Ratio", "Special case / needs qualification"], index=None, horizontal=True, key="schoice")
if st.button("Check measurement scale"):
    if schoice is None:
        st.warning("Choose an answer first.")
    elif schoice == stype:
        st.success(f"Correct! {sreason}")
    else:
        st.error(f"Best answer: **{stype}**. {sreason}")
with st.expander("View all measurement-scale practice items"):
    st.dataframe(pd.DataFrame(SCALES, columns=["Variable", "Scale", "Explanation"]), use_container_width=True, hide_index=True)

st.divider()
st.header("End-of-lesson self-check")
quiz = [
("The number of medication errors in a shift is usually:", ["Categorical","Discrete numerical","Continuous numerical","Nominal scale only"], "Discrete numerical", "Medication errors are counted."),
("Which scale has ordered categories but does not guarantee equal distances?", ["Nominal","Ordinal","Interval","Ratio"], "Ordinal", "Ordinal categories are ranked, but spacing is not guaranteed equal."),
("Temperature in degrees Celsius is conventionally:", ["Nominal","Ordinal","Interval","Ratio"], "Interval", "Differences are meaningful, but zero is not an absolute zero."),
("A patient identification number is best treated as:", ["Ratio measurement","Continuous variable","Categorical identifier","Interval measurement"], "Categorical identifier", "The digits identify a patient; arithmetic on them has no quantitative meaning."),
("Which is the clearest ratio-scale example?", ["Blood group","Severity rank","Temperature in °C","Drug mass in mg"], "Drug mass in mg", "Mass has a meaningful zero."),
]
answers = []
for i, (q, options, correct, why) in enumerate(quiz):
    answers.append(st.radio(q, options, index=None, key=f"lessonquiz{i}"))
if st.button("Submit self-check"):
    score = 0
    for i, ((q, options, correct, why), ans) in enumerate(zip(quiz, answers), start=1):
        if ans == correct:
            score += 1
            st.success(f"Q{i}: Correct. {why}")
        else:
            st.error(f"Q{i}: Correct answer: **{correct}**. {why}")
    st.metric("Your score", f"{score}/5")
    if score >= 4:
        st.balloons()
        st.success("Well done! You are ready to continue to data and sources of pharmaceutical data.")
    else:
        st.info("Review the notes and try again. Focus on the distinction between variable type and measurement scale.")

st.caption("This first version uses session-based practice. Progress is not yet saved across browsers or devices.")

