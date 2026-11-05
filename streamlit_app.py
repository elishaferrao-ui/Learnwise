
import streamlit as st

# --------------------------------
# 1. PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="LEARNWISE",
    page_icon="📚",
    layout="centered"
)

# --------------------------------
# 2. WELCOME SCREEN
# --------------------------------

st.title("📚 LEARNWISE")

st.subheader(
    "Understand what you learn. Discover what needs practice."
)

st.write(
    "LEARNWISE helps students identify concepts "
    "they understand and concepts they may need to revise."
)

st.divider()

# --------------------------------
# 3. STUDENT DETAILS
# --------------------------------

st.header("Student details")

student_name = st.text_input("Enter your name")

grade = st.selectbox(
    "Select your grade",
    ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]
)

# --------------------------------
# 4. QUESTION BANK
# --------------------------------

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
        "answer": "The forces are balanced",
        "explanation": "The book is at rest. Its weight acts downwards and the support force from the table acts upwards. These forces balance each other."
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
        "answer": "The forces are balanced",
        "explanation": "Equal forces acting in opposite directions have a zero resultant force."
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
        "answer": "It starts moving",
        "explanation": "The kick applies an unbalanced force that changes the football's state of motion."
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
        "answer": "Change its state of motion",
        "explanation": "An unbalanced force can change an object's speed, direction or state of motion."
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
        "answer": "Opposite to motion or attempted motion",
        "explanation": "Friction opposes relative motion or the tendency of surfaces to move relative to each other."
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
        "answer": "Friction decreases",
        "explanation": "Lubricants reduce friction between surfaces by making it easier for them to move against each other."
    }
]

# --------------------------------
# 5. START ASSESSMENT
# --------------------------------

if st.button("Start assessment"):

    if student_name.strip():
        st.session_state.started = True
    else:
        st.warning("Please enter your name first.")

# --------------------------------
# 6. DISPLAY QUESTIONS
# --------------------------------

if st.session_state.get("started", False):

    st.divider()

    st.header("📝 Science Assessment")

    st.write(f"Student: {student_name}")
    st.write(f"Grade: {grade}")

    st.write("Choose one answer for every question.")

    with st.form("science_assessment"):

        for i, q in enumerate(questions):

            st.markdown(
                f"**Question {i + 1}: {q['concept']}**"
            )

            st.write(q["question"])

            st.radio(
                "Select your answer:",
                ["Choose an answer"] + q["options"],
                key=f"question_{i}"
            )

        submitted = st.form_submit_button(
            "Submit assessment"
        )

    # --------------------------------
    # 7. CHECK ANSWERS AND CALCULATE SCORES
    # --------------------------------

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

            mistakes = []

            for i, q in enumerate(questions):

                selected = st.session_state[f"question_{i}"]

                scores[q["concept"]][1] += 1

                if selected == q["answer"]:

                    scores[q["concept"]][0] += 1

                else:

                    mistakes.append({
                        "number": i + 1,
                        "concept": q["concept"],
                        "question": q["question"],
                        "selected": selected,
                        "correct": q["answer"],
                        "explanation": q["explanation"]
                    })

            total_correct = sum(
                score[0] for score in scores.values()
            )

            # --------------------------------
            # 8. LEARNING REPORT
            # --------------------------------

            st.divider()

            st.header("📊 Your Learning Report")

            st.metric(
                "Overall score",
                f"{total_correct}/6"
            )

            st.subheader("Concept-wise performance")

            for concept, score in scores.items():

                correct, total = score

                st.write(
                    f"**{concept}: {correct}/{total}**"
                )

                if correct == total:

                    st.success(
                        "Good understanding. Keep practising!"
                    )

                else:

                    st.warning(
                        "This concept needs more revision."
                    )

            # --------------------------------
            # 9. MISTAKE REVIEW
            # --------------------------------

            st.divider()

            st.header("🔍 Mistake Review")

            if mistakes:

                st.write(
                    "Let's understand the questions you "
                    "answered incorrectly."
                )

                for mistake in mistakes:

                    with st.expander(
                        f"Question {mistake['number']}: "
                        f"{mistake['concept']}"
                    ):

                        st.write(mistake["question"])

                        st.error(
                            f"Your answer: {mistake['selected']}"
                        )

                        st.success(
                            f"Correct answer: {mistake['correct']}"
                        )

                        st.markdown("**Why is this correct?**")

                        st.write(mistake["explanation"])

                        st.info(
                            f"Learning tip: Revise "
                            f"{mistake['concept']} and try "
                            f"a similar question."
                        )

            else:

                st.success(
                    "Excellent! You answered every "
                    "question correctly."
                )

            st.caption(
                "LEARNWISE identifies concepts to review. "
                "It does not assume why a student made a mistake."
            )
            
