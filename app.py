import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Johan's Judgement", page_icon="🔧", layout="wide")

# 2. App Styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        width: 100%; 
        background-color: #d32f2f; 
        color: white; 
        height: 3em; 
        font-size: 20px;
    }
    .report-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        border-left: 10px solid #d32f2f;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔧 Johan's Judgement: Advanced Diagnostic")
st.write("---")

# 3. Enhanced Troubleshooting Database
kb = {
    "Loss of power": {
        "Phase 1: Air & Exhaust": [
            {"q": "Is there thick black smoke during acceleration?", "target": "EGR Valve stuck or Carbon buildup", "detail": "Excessive soot indicates air starvation or a stuck EGR valve."},
            {"q": "Do you hear a high-pitched whistling or 'whoosh' sound?", "target": "Boost leak or Turbocharger failure", "detail": "Common on diesels; check intercooler pipes for cracks."},
        ],
        "Phase 2: Fuel & Delivery": [
            {"q": "Does the engine 'stutter' or hesitate only when going uphill?", "target": "Weak Fuel Pump or clogged strainer", "detail": "The pump is struggling to maintain pressure under load."},
            {"q": "Is the car harder to start when the engine is already hot?", "target": "Leaking Fuel Injectors", "detail": "Injectors may be 'dripping' fuel, causing a flooded start."}
        ],
        "Phase 3: Sensors & Electrical": [
            {"q": "Is the 'Check Engine' light flashing specifically under load?", "target": "Ignition Coil Misfire", "detail": "Common in petrol engines; spark is failing under compression."},
            {"q": "Does the car feel normal until you reach a certain speed/RPM?", "target": "MAF Sensor or Limp Mode", "detail": "The ECU might be restricting power due to bad sensor readings."}
        ]
    },
    "Brake / Suspension Issues": {
        "Phase 1: Vibration": [
            {"q": "Does the steering wheel shake only when braking?", "target": "Warped Brake Discs", "detail": "Heat has distorted the rotors, causing an uneven surface."},
            {"q": "Does the car pull to one side when you aren't braking?", "target": "Wheel Alignment or Control Arm Bushings", "detail": "Suspension geometry is out of spec."}
        ]
    }
}

# 4. Sidebar Profile
st.sidebar.header("Vehicle Profile")
brand = st.sidebar.text_input("Brand", "Toyota")
fuel = st.sidebar.radio("Engine Type", ["Petrol", "Diesel"])
mileage = st.sidebar.number_input("Current Mileage (km)", value=150000, step=10000)
last_service = st.sidebar.slider("Months since last service", 0, 48, 6)

# 5. Diagnostic Workflow
symptom = st.selectbox("Select the primary symptom:", ["Select one"] + list(kb.keys()))

if symptom != "Select one":
    st.write(f"### Investigating: {symptom}")
    st.write("Answer the following to eliminate unlikely causes:")
    
    user_hits = []
    
    # Loop through the phases
    for phase, questions in kb[symptom].items():
        with st.expander(phase, expanded=True):
            for item in questions:
                choice = st.radio(item['q'], ["No / Not Sure", "Yes"], key=item['q'])
                if choice == "Yes":
                    user_hits.append(item)

    st.write("---")
    if st.button("GENERATE JUDGEMENT"):
        if not user_hits:
            st.error("No specific indicators found. This suggests a general mechanical wear issue (like a clogged filter) or a deep internal engine problem.")
        else:
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.header("🏁 Johan's Final Report")
            for hit in user_hits:
                st.subheader(f"📍 Potential: {hit['target']}")
                st.write(f"**Why?** {hit['detail']}")
            
            # Add a specific advice based on the user's mileage
            if mileage > 200000:
                st.warning("⚠️ High Mileage Note: At this distance, consider checking timing chains and compression.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# 6. Footer
st.write("---")
st.markdown("### 📞 NEED A PROFESSIONAL HAND?")
st.markdown(f"## **Contact: 061 888 6110**")
st.write("Call me if you are in the **East Rand**!")
