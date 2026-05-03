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

# 3. Vehicle Identity
st.subheader("Step 1: Vehicle Identity")
col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("Car Brand", placeholder="e.g. Ford, Toyota, Isuzu")
    model = st.text_input("Model", placeholder="e.g. Ranger, Hilux, KB")
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2015)

with col2:
    fuel_type = st.radio("Engine Type", ["Petrol", "Diesel"])
    last_service = st.number_input("Months since last service", min_value=0, max_value=60, value=6)

st.write("---")

# 4. Expanded Diagnostic Data
diagnosis_db = {
    "Loss of Power / Hesitation": {
        "Air & Exhaust Systems": [
            {"q": "Is there thick black smoke on acceleration?", "target": "Stuck EGR Valve or Clogged Air Filter", "fuel": "Diesel", "service": True},
            {"q": "Do you hear a loud whistling or 'whooshing' sound under boost?", "target": "Boost Leak / Split Turbo Pipe", "fuel": "both", "service": False},
            {"q": "Is the car struggling only at high speeds/RPM (feels choked)?", "target": "Clogged Catalytic Converter / DPF", "fuel": "both", "service": True}
        ],
        "Fuel & Spark Systems": [
            {"q": "Does the engine 'stutter' or misfire under load/acceleration?", "target": "Worn Spark Plugs or Failing Coil Pack", "fuel": "Petrol", "service": True},
            {"q": "Is the car hard to start when cold (winter mornings)?", "target": "Failing Glow Plugs or Injector Leak-off", "fuel": "Diesel", "service": True},
            {"q": "Does it feel like the car is 'starving' for fuel uphill?", "target": "Fuel Pump Strainer or Filter Blockage", "fuel": "both", "service": True}
        ]
    },
    "Suspension & Drive-Train Noises": {
        "Wheel & Bearing Sounds": [
            {"q": "Do you hear a 'Whop-Whop' or humming sound that gets faster with speed?", "target": "Wheel Bearing Failure", "fuel": "both", "service": False},
            {"q": "Do you hear a rhythmic 'Click-Click-Click' when turning the steering wheel sharply?", "target": "Outer CV Joint Failure", "fuel": "both", "service": False},
            {"q": "Does the car vibrate or shudder specifically when accelerating?", "target": "Inner CV Joint or Prop-shaft out of balance", "fuel": "both", "service": False}
        ],
        "Knocks & Clunks": [
            {"q": "Do you hear a 'Clunk' when driving over speed bumps?", "target": "Worn Control Arm Bushings or Stabilizer Links", "fuel": "both", "service": False},
            {"q": "Is there a heavy metallic 'Thud' when shifting gears or taking off?", "target": "Engine/Gearbox Mount failure", "fuel": "both", "service": False}
        ]
    },
    "Engine Noises (Mechanical)": {
        "Deep Engine Sounds": [
            {"q": "Is there a heavy metallic 'knock' from the bottom of the engine?", "target": "Big End Bearing Wear (Bottom End Knock)", "fuel": "both", "service": True},
            {"q": "Is there a fast 'tapping' or 'ticking' sound from the top of the engine?", "target": "Hydraulic Lifter / Valve Train wear", "fuel": "both", "service": True}
        ],
        "External Belts": [
            {"q": "Is there a high-pitched 'Squeal' when you first start the car or turn the AC on?", "target": "Fan Belt / Serpentine Belt slipping or worn", "fuel": "both", "service": True}
        ]
    },
    "Starting & Electrical Issues": {
        "Non-Start Issues": [
            {"q": "Do you hear a single 'Click' but the engine doesn't turn over?", "target": "Starter Motor Solenoid Failure", "fuel": "both", "service": False},
            {"q": "Does the engine turn over very slowly (labored cranking)?", "target": "Weak Battery or Poor Earth Connection", "fuel": "both", "service": False},
            {"q": "Does the engine crank perfectly but refuse to 'fire' up?", "target": "Crank Position Sensor or Fuel Pump Relay", "fuel": "both", "service": False}
        ],
        "Charging": [
            {"q": "Has the Battery Light appeared on the dashboard while driving?", "target": "Alternator Failure (Not charging)", "fuel": "both", "service": False}
        ]
    }
}

# 5. Symptom Selection
symptom = st.selectbox("Step 2: What is the main symptom area?", ["Select a symptom"] + list(diagnosis_db.keys()))

if symptom != "Select a symptom":
    st.subheader(f"Step 3: Investigating {symptom}")
    st.write("Check the boxes for any symptoms you notice:")
    
    selected_hits = []
    
    # Filter and display questions based on Fuel Type
    for phase, questions in diagnosis_db[symptom].items():
        with st.expander(phase, expanded=True):
            for item in questions:
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
            st.warning("No specific symptoms matched. If the car feels 'off', it may be a sensor starting to fail or an intermittent electrical fault.")
        else:
            for hit in selected_hits:
                st.subheader(f"📍 Potential Cause: {hit['target']}")
                
                if last_service > 12 and hit['service']:
                    st.error("⚠️ MAINTENANCE ALERT: This issue is likely caused by missing your service interval. A full service is required immediately.")
                elif hit['service']:
                    st.info("ℹ️ Note: This component often fails even with regular servicing due to South African road conditions.")
                else:
                    st.info("ℹ️ Note: This is a mechanical failure that requires part replacement regardless of your last service.")
        
        st.write("---")
        st.write("**ACTION PLAN:** Don't let a small noise become a big bill. Contact Johan for a physical inspection.")
        st.markdown('</div>', unsafe_allow_html=True)

# 7. Contact Footer
st.write("---")
st.markdown("### 📞 NEED A PROFESSIONAL HAND?")
st.markdown(f"## **Contact: 061 888 6110**")
st.write(f"Based in the **East Rand**. I'll get your {brand} sorted out properly.")
