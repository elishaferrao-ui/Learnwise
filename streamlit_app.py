
import streamlit as st

st.set_page_config(
    page_title="LEARNWISE",
    page_icon="📚",
    layout="centered"
)

st.title("📚 LEARNWISE")
st.subheader("Understand what you learn. Discover what needs practice.")

st.write(
    "LEARNWISE helps students identify concepts "
    "they understand and concepts they may need to revise."
)

st.divider()

# STUDENT DETAILS

st.header("Student details")

student_name = st.text_input("Enter your name")

grade = st.selectbox(
    "Select your grade",
    ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]
)

# QUESTION BANK
# Every question is linked to a specific concept.

questions = [
    {
        "concept": "Balanced forces",
        "question": "A book is resting on a table. What can we say about the forces acting on it?",
        "options": [
            "The forces are balanced",
            "The forces are unbalanced",
            "There is no gravity",
            "The book has no weight"
        ],
        "answer": "The forces are balanced"
    },
    {
        "concept": "Balanced forces",
        "question": "Two teams pull a rope with equal forces in opposite directions. What happens?",
        "options": [
            "The rope moves towards the first team",
            "The rope moves towards the second team",
            "The forces are balanced",
            "The rope disappears"
        ],
        "answer": "The forces are balanced"
    },
    {
        "concept": "Unbalanced forces",
        "question": "A stationary football is kicked. What happens to its motion?",
        "options": [
            "It starts moving",
            "It remains stationary forever",
            "Its mass becomes zero",
            "Gravity disappears"
        ],
        "answer": "It starts moving"
    },
    {
        "concept": "Unbalanced forces",
        "question": "What can an unbalanced force do to an object?",
        "options": [
            "Change its state of motion",
            "Always keep it at rest",
            "Remove its mass",
            "Destroy its weight"
        ],
        "answer": "Change its state of motion"
    },
    {
        "concept": "Friction",
        "question": "In which direction does friction generally act?",
        "options": [
            "Opposite to motion or attempted motion",
            "Always upwards",
            "Always downwards",
            "In the direction of motion"
        ],
        "answer": "Opposite to motion or attempted motion"
    },
    {
        "concept": "Friction",
        "question": "What generally happens when lubricant is applied between two surfaces?",
        "options": [
            "Friction decreases",
            "Friction always increases",
            "Mass increases",
            "Gravity increases"
        ],
        "answer": "Friction decreases"
    }
]

# START ASSESSMENT

if st.button("Start assessment"):
    if student_name.strip():
        st.session_state.started = True
    else:
        st.warning("Please enter your name first.")

# DISPLAY QUESTIONS

if st.session_state.get("started", False):

    st.divider()
    st.header("📝 Science Assessment")
    st.write(f"Student: {student_name} | Grade: {grade}")
    st.write("Choose one answer for every question.")

    with st.form("science_assessment"):

        for i, q in enumerate(questions):
            st.markdown(f"**Question {i + 1}: {q['concept']}**")
            st.write(q["question"])

            st.radio(
                "Select your answer:",
                ["Choose an answer"] + q["options"],
                key=f"question_{i}"
            )

        submitted = st.form_submit_button("Submit assessment")

    if submitted:

        unanswered = [
            i for i in range(len(questions))
            if st.session_state.get(f"question_{i}")
            == "Choose an answer"
        ]

        if unanswered:
            st.warning("Please answer all six questions.")
        else:

            scores = {
                "Balanced forces": [0, 0],
                "Unbalanced forces": [0, 0],
                "Friction": [0, 0]
            }

            for i, q in enumerate(questions):
                scores[q["concept"]][1] += 1

                if st.session_state[f"question_{i}"] == q["answer"]:
                    scores[q["concept"]][0] += 1

            total_correct = sum(
                score[0] for score in scores.values()
            )

            st.divider()
            st.header("📊 Your Learning Report")

            st.metric(
                "Overall score",
                f"{total_correct}/6"
            )

            st.subheader("Concept-wise performance")

            for concept, score in scores.items():

                correct, total = score

                st.write(f"**{concept}: {correct}/{total}**")

                if correct == total:
                    st.success("Good understanding. Keep practising!")
                else:
                    st.warning(
                        "This concept needs more revision and practice."
                    )

            st.info(
                "This report identifies concepts to review. "
                "It does not diagnose the reason for an incorrect answer."
            )
            
