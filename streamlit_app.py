
import streamlit as st

st.set_page_config(
    page_title="LEARNWISE",
    page_icon="📚",
    layout="centered"
)

st.title("📚 LEARNWISE")
st.subheader("Understand what you learn. Discover what needs practice.")

st.write(
    "Welcome! LEARNWISE helps students identify the concepts "
    "they understand and the concepts they may need to revise."
)

st.divider()

st.header("Let's get started!")

student_name = st.text_input("Enter your name")

grade = st.selectbox(
    "Select your grade",
    ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]
)

if st.button("Start learning"):
    if student_name.strip():
        st.success(f"Welcome, {student_name}!")
        st.write(f"Your selected level is {grade}.")
        st.info("Your learning journey starts here!")
    else:
        st.warning("Please enter your name first.")
        
