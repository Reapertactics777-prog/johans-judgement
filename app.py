import streamlit as st

# Page Configuration
st.set_page_config(page_title="Johan's Judgement", page_icon="🔧")

# App Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #d32f2f;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔧 Johan's Judgement")
st.write("### Professional Mechanic Diagnosis")
st.write("---")

# Vehicle Inputs
col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Car Brand", placeholder="e.g. Toyota")
    model = st.text_input("Model", placeholder="e.g. Hilux")
    year = st.number_input("Year", min_value=1980, max_value=2026, value=2018)

with col2:
    fuel = st.radio("Engine Type", ["Petrol", "Diesel"])
    last_service = st.number_input("Months since last service", min_value=0, max_value=60, value=6)

symptom = st.selectbox("What is the main symptom?", [
    "Select a symptom",
    "Knocking noise from engine",
    "Overheating",
    "Black smoke from exhaust",
    "White smoke from exhaust",
    "Loss of power",
    "Squealing noise when braking",
    "Hard to start"
])

# Diagnosis Data
knowledge_base = {
    "Knocking noise from engine": [{"cause": "Low oil levels or worn bearings", "fuel": "both", "service": True}],
    "Overheating": [{"cause": "Coolant leak or faulty thermostat", "fuel": "both", "service": True}],
    "Black smoke from exhaust": [
        {"cause": "Clogged air filter", "fuel": "both", "service": True},
        {"cause": "Faulty diesel injectors", "fuel": "Diesel", "service": False}
    ],
    "Loss of power": [{"cause": "Fuel filter blockage", "fuel": "both", "service": True}],
    "Hard to start": [
        {"cause": "Worn spark plugs", "fuel": "Petrol", "service": True},
        {"cause": "Glow plugs failing", "fuel": "Diesel", "service": True}
    ]
}

if st.button("GET JUDGEMENT"):
    if symptom == "Select a symptom":
        st.error("Please select a symptom first.")
    else:
        st.write(f"#### Results for your {year} {brand}:")
        found = False
        for issue in knowledge_base.get(symptom, []):
            if issue['fuel'] == fuel or issue['fuel'] == "both":
                found = True
                if last_service > 12 and issue['service']:
                    st.warning(f"⚠️ Likely {issue['cause']} (Due to lack of service)")
                else:
                    st.info(f"✅ Potential Issue: {issue['cause']}")
        
        if not found:
            st.write("Specialized diagnosis required.")

# Footer
st.write("---")
st.markdown("### 📞 NEED A PROFESSIONAL HAND?")
st.markdown("## **Contact: 061 888 6110**")
st.write("Call me if you are in the **East Rand**!")
