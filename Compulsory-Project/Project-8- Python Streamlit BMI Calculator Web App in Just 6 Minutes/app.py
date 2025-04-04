import streamlit as st

# Set page config
st.set_page_config(page_title="BMI Calculator", page_icon="💪", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .big-font {
            font-size:30px !important;
            font-weight:600;
            color:#4CAF50;
        }
        .result-font {
            font-size:24px !important;
            font-weight:500;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<p class="big-font">💪 BMI Calculator</p>', unsafe_allow_html=True)

# Input Section
st.subheader("Enter your details:")

name = st.text_input("Your Name", "")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0, step=0.1)
weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=250.0, step=0.1)

# BMI Calculation
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def get_bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight 😟"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight 😊"
    elif 25 <= bmi < 29.9:
        return "Overweight 😐"
    else:
        return "Obese 😟"

# Button to calculate
if st.button("Calculate BMI"):
    if height > 0 and weight > 0 and gender != "Select":
        bmi = calculate_bmi(weight, height)
        status = get_bmi_status(bmi)

        st.markdown(f"<p class='result-font'>Hi <strong>{name}</strong>, your BMI is: <strong>{bmi}</strong></p>", unsafe_allow_html=True)
        st.success(f"BMI Status: {status}")
    else:
        st.error("Please fill in all the details correctly!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
