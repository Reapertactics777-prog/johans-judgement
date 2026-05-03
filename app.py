import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Johan's Judgement", page_icon="🔧", layout="centered")

# 2. Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #d32f2f; color: white; height: 3em; border-radius: 5px; font-weight: bold; }
    .report-card { padding: 20px; border: 2px solid #d32f2f; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔧 Johan's Judgement")
st.write("### Advanced Mechanical Diagnostic Engine")
st.write("---")

# 3. Vehicle Identity (The "Filter" Inputs)
st.subheader("Step 1: Vehicle Identity")
col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("Car Brand", placeholder="e.g. Ford, VW, Toyota")
    model = st.text_input("Model", placeholder="e.g. Ranger, Golf, Hilux")
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2015)

with col2:
    fuel_type = st.radio("Engine Type", ["Petrol", "Diesel"])
    last_service = st.number_input("Months since last service", min_value=0, max_value=60, value=6)

st.write("---")

# 4. Diagnostic Data (Branching Logic)
# Format: {Symptom: {Phase: [{q: question, target: cause, fuel: type, service_link: bool}]}}
diagnosis_db = {
    "Loss of Power / Hesitation": {
        "Air & Exhaust Systems": [
            {"q": "Is there thick black smoke on acceleration?", "target": "Stuck EGR Valve or Clogged Air Filter", "fuel": "Diesel", "service": True},
            {"q": "Do you hear a loud whistling or 'whooshing' sound?", "target": "Boost Leak / Split Turbo Pipe", "fuel": "both", "service": False},
            {"q": "Is the car struggling only at high speeds/RPM?", "target": "Clogged Catalytic Converter / DPF", "fuel": "both", "service": True}
        ],
        "Fuel & Spark Systems": [
            {"q": "Does the engine 'stutter' or misfire under load?", "target": "Worn Spark Plugs or Failing Coil Pack", "fuel": "Petrol", "service": True},
            {"q": "Is the car hard to start when cold?", "target": "Failing Glow Plugs or Diesel Injector Leak-off", "fuel": "Diesel", "service": True},
            {"q": "Does it feel like the car is 'starving' for fuel uphill?", "target": "Fuel Pump Strainer or Filter Blockage", "fuel": "both", "service": True}
        ]
    },
    "Engine Noises": {
        "Internal Noises": [
            {"q": "Is there a heavy metallic 'knock' from the bottom of the engine?", "target": "Big End Bearing Wear", "fuel": "both", "service": True},
            {"q": "Is there a fast 'tapping' sound from the top of the engine?", "target": "Hydraulic Lifter / Valve Train wear", "fuel": "both", "service": True}
        ],
        "External Noises": [
            {"q": "Is there a high-pitched squeal when you start the car?", "target": "Fan Belt (Serpentine Belt) slipping", "fuel": "both", "service": True}
        ]
    }
}

# 5. Symptom Selection
symptom = st.selectbox("Step 2: What is the main symptom?", ["Select a symptom"] + list(diagnosis_db.keys()))

if symptom != "Select a symptom":
    st.subheader(f"Step 3: Investigating {symptom}")
    st.write("Answer 'Yes' to any that apply:")
    
    selected_hits = []
    
    # Filter and display questions based on Fuel Type
    for phase, questions in diagnosis_db[symptom].items():
        with st.expander(phase):
            for item in questions:
                # ONLY show question if it matches the car's fuel type or applies to 'both'
                if item['fuel'] == fuel_type or item['fuel'] == "both":
                    user_input = st.checkbox(item['q'], key=item['q'])
                    if user_input:
                        selected_hits.append(item)

    # 6. Final Judgement Generation
    if st.button("GENERATE FINAL JUDGEMENT"):
        st.write("---")
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.header(f"🏁 Johan's Report: {year} {brand} {model}")
        
        if not selected_hits:
            st.warning("No specific symptoms matched. If the car feels 'off' but has no smoke or noise, it is likely a sensor (MAF/Oxygen) failing without a total breakdown yet.")
        else:
            for hit in selected_hits:
                st.subheader(f"📍 Potential Cause: {hit['target']}")
                
                # Logic to check if it's service related
                if last_service > 12 and hit['service']:
                    st.error("⚠️ MAINTENANCE ALERT: This issue is highly likely caused by missing your service interval. A standard service may fix this.")
                elif hit['service']:
                    st.info("ℹ️ Note: Even though you've serviced recently, this part may have reached its end-of-life.")
                else:
                    st.info("ℹ️ Note: This is a mechanical/electrical failure not typically covered by a standard oil change.")
        
        st.write("---")
        st.write("**REQUIRED ACTION:** Please bring the vehicle for a physical inspection to confirm these findings.")
        st.markdown('</div>', unsafe_allow_html=True)

# 7. Contact Footer
st.write("---")
st.markdown("### 📞 NEED A PROFESSIONAL HAND?")
st.markdown(f"## **Contact: 061 888 6110**")
st.write(f"Call me if you are in the **East Rand**! I'll get your {brand} back on the road.")
