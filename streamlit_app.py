
import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="LEARNWISE",
    page_icon="📘",
    layout="wide"
)

# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eee9ff, #e5f2ff, #e3fff5);
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}
h1, h2, h3 {
    color: #30345f;
}
div.stButton > button {
    background-color: #6657c8;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.2rem;
}
div.stButton > button:hover {
    background-color: #5042a8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

st.title("📘 LEARNWISE")
st.caption("Understand the gap. Support the learner. Strengthen learning.")

if not st.user.is_logged_in:
    st.markdown("### Welcome to LEARNWISE!")
    st.write(
        "Sign in with your Google account to access the student "
        "or teacher experience."
    )

    st.info(
        "Your Google account handles sign-in. LEARNWISE does not "
        "ask you to create or share a password inside this app."
    )

    if st.button("Sign in with Google"):
        st.login()

    st.stop()

# Get authenticated account information
user_email = st.user.email.lower()
user_name = st.user.get("name", "LEARNWISE User")

# Read authorised email lists from Streamlit secrets
teacher_emails = [
    email.lower()
    for email in st.secrets["app"]["teacher_emails"]
]

student_emails = [
    email.lower()
    for email in st.secrets["app"]["student_emails"]
]

# Decide role using the authenticated email
if user_email in teacher_emails:
    user_role = "teacher"
elif user_email in student_emails:
    user_role = "student"
else:
    st.error(
        "This account has not been authorised to use LEARNWISE. "
        "Please contact the person managing the prototype."
    )
    if st.button("Sign out"):
        st.logout()
    st.stop()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "practice_question" not in st.session_state:
    st.session_state.practice_question = None

if "student_attempts" not in st.session_state:
    st.session_state.student_attempts = []

# --------------------------------------------------
# QUESTION BANK
# --------------------------------------------------

questions = [
    {
        "question": "1. What happens when balanced forces act on a stationary object?",
        "options": [
            "It starts moving",
            "It remains stationary",
            "It changes direction",
            "It speeds up"
        ],
        "answer": "It remains stationary",
        "concept": "Balanced Forces",
        "explanation": (
            "Balanced forces have a net force of zero. "
            "A stationary object remains stationary when the forces "
            "acting on it are balanced."
        )
    },
    {
        "question": "2. Which statement describes balanced forces?",
        "options": [
            "The forces are always very large",
            "The forces act in the same direction",
            "The resultant force is zero",
            "The object must be moving"
        ],
        "answer": "The resultant force is zero",
        "concept": "Balanced Forces",
        "explanation": (
            "Balanced forces cancel each other out. "
            "Their resultant or net force is zero."
        )
    },
    {
        "question": "3. What can an unbalanced force do to an object?",
        "options": [
            "Change its motion",
            "Always keep it stationary",
            "Make all forces disappear",
            "Have no effect on motion"
        ],
        "answer": "Change its motion",
        "concept": "Unbalanced Forces",
        "explanation": (
            "An unbalanced force produces a non-zero resultant force. "
            "It can change an object's speed or direction."
        )
    },
    {
        "question": "4. A football is kicked and begins moving. What caused this change?",
        "options": [
            "Balanced forces",
            "An unbalanced force",
            "No force",
            "Gravity disappearing"
        ],
        "answer": "An unbalanced force",
        "concept": "Unbalanced Forces",
        "explanation": (
            "The kick applies a force that changes the ball's state "
            "of motion. This is an example of an unbalanced force."
        )
    },
    {
        "question": "5. What is friction?",
        "options": [
            "A force that opposes relative motion",
            "A force that always increases speed",
            "A type of light",
            "A form of energy"
        ],
        "answer": "A force that opposes relative motion",
        "concept": "Friction",
        "explanation": (
            "Friction acts between surfaces in contact and opposes "
            "their relative motion or tendency to move."
        )
    },
    {
        "question": "6. Which surface usually produces more friction?",
        "options": [
            "A smooth, polished surface",
            "A rough surface",
            "A surface with no contact",
            "A perfectly frictionless surface"
        ],
        "answer": "A rough surface",
        "concept": "Friction",
        "explanation": (
            "Rough surfaces generally produce more friction than "
            "smooth surfaces because of their surface irregularities."
        )
    }
]

# --------------------------------------------------
# PRACTICE QUESTIONS
# --------------------------------------------------

practice_questions = {
    "Balanced Forces": {
        "question": "A book rests on a table. Which statement is correct?",
        "options": [
            "The downward gravitational force is balanced by the upward support force",
            "There are no forces acting on the book",
            "The book is accelerating downward",
            "The table has no effect on the book"
        ],
        "answer": (
            "The downward gravitational force is balanced by "
            "the upward support force"
        ),
        "explanation": (
            "The book remains at rest because the upward support "
            "force balances its weight."
        )
    },
    "Unbalanced Forces": {
        "question": "A moving bicycle slows down when the rider applies the brakes. Why?",
        "options": [
            "The forces are balanced",
            "An opposing force changes its motion",
            "Its mass disappears",
            "Gravity stops acting"
        ],
        "answer": "An opposing force changes its motion",
        "explanation": (
            "The braking force acts against the bicycle's motion, "
            "causing it to slow down."
        )
    },
    "Friction": {
        "question": "Why do shoes have patterned soles?",
        "options": [
            "To reduce grip",
            "To increase friction and improve grip",
            "To remove gravity",
            "To make shoes weightless"
        ],
        "answer": "To increase friction and improve grip",
        "explanation": (
            "Sole patterns help provide grip by increasing the "
            "friction between the shoe and the ground."
        )
    }
}

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.sidebar.success("Signed in")
st.sidebar.write(f"**Account:** {user_email}")
st.sidebar.write(
    "**Access:** Teacher" if user_role == "teacher"
    else "**Access:** Student"
)

if st.sidebar.button("Sign out"):
    st.logout()

st.divider()

# ==================================================
# STUDENT VIEW
# ==================================================

if user_role == "student":

    st.header("🎓 Student Learning Space")
    st.write(f"Welcome, {user_name}!")
    st.write(
        "LEARNWISE helps you understand concepts, "
        "review mistakes and practise what you have learned."
    )

    st.info(
        "Your assessment is for learning and improvement. "
        "It is not a judgement of your ability."
    )

    st.subheader("Science Assessment")
    st.write("Topic: Forces and Motion")

    # Start or restart assessment
    if st.button("Start a new assessment"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.practice_question = None

    # Display assessment
    with st.form("science_assessment"):

        selected_answers = {}

        for index, question in enumerate(questions):
            st.markdown(f"**{question['question']}**")

            selected_answers[index] = st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"answer_{index}",
                label_visibility="collapsed"
            )

            st.write("")

        submitted = st.form_submit_button("Submit assessment")

    if submitted:
        if any(answer is None for answer in selected_answers.values()):
            st.warning("Please answer all six questions before submitting.")
        else:
            st.session_state.answers = selected_answers
            st.session_state.submitted = True
            st.session_state.practice_question = None

    # Results
    if st.session_state.submitted:

        st.divider()
        st.subheader("📊 Your Learning Results")

        correct_count = 0
        concept_scores = {
            "Balanced Forces": [0, 0],
            "Unbalanced Forces": [0, 0],
            "Friction": [0, 0]
        }

        for index, question in enumerate(questions):
            chosen = st.session_state.answers[index]
            concept = question["concept"]

            concept_scores[concept][1] += 1

            if chosen == question["answer"]:
                correct_count += 1
                concept_scores[concept][0] += 1

        percentage = round((correct_count / len(questions)) * 100)

        col1, col2, col3 = st.columns(3)

        col1.metric("Correct answers", f"{correct_count}/6")
        col2.metric("Assessment score", f"{percentage}%")
        col3.metric("Concepts assessed", "3")

        st.subheader("Concept-level understanding")

        for concept, scores in concept_scores.items():
            earned, total = scores
            accuracy = round((earned / total) * 100)

            st.write(f"**{concept}: {earned}/{total} ({accuracy}%)**")
            st.progress(accuracy / 100)

        # Mistake review
        st.divider()
        st.subheader("🔍 Mistake Review")

        for index, question in enumerate(questions):
            chosen = st.session_state.answers[index]

            if chosen != question["answer"]:
                with st.expander(
                    f"Question {index + 1}: Review your answer"
                ):
                    st.write(f"**Your answer:** {chosen}")
                    st.write(f"**Correct answer:** {question['answer']}")
                    st.write(f"**Concept:** {question['concept']}")
                    st.info(question["explanation"])

        # Practice recommendation
        st.divider()
        st.subheader("🎯 Your Next Practice")

        weaker_concepts = [
            concept
            for concept, scores in concept_scores.items()
            if scores[0] < scores[1]
        ]

        if weaker_concepts:
            st.write(
                "These concepts may benefit from another round "
                "of practice:"
            )

            for concept in weaker_concepts:
                st.write(f"• {concept}")

            selected_concept = st.selectbox(
                "Choose a concept to practise:",
                weaker_concepts
            )

            if st.button("Try a similar question"):
                st.session_state.practice_question = selected_concept

        else:
            st.success(
                "You answered every question correctly. "
                "Try explaining these concepts in your own words next!"
            )

        # Practice question display
        if st.session_state.practice_question:

            concept = st.session_state.practice_question
            practice = practice_questions[concept]

            st.divider()
            st.subheader(f"Practice: {concept}")

            practice_answer = st.radio(
                practice["question"],
                practice["options"],
                key=f"practice_{concept}"
            )

            if st.button("Check practice answer"):
                if practice_answer == practice["answer"]:
                    st.success("Correct! Great concept understanding.")
                else:
                    st.warning(
                        f"Correct answer: {practice['answer']}"
                    )
                    st.info(practice["explanation"])

    st.divider()
    st.caption(
        "LEARNWISE Student Dignity Principle: "
        "A learning gap is an opportunity for support, not a label."
    )

# ==================================================
# TEACHER VIEW
# ==================================================

elif user_role == "teacher":

    st.header("👩‍🏫 Teacher Dashboard")
    st.write(f"Welcome, {user_name}!")

    st.info(
        "DEMO DASHBOARD: The figures below are fictional sample data. "
        "They are not collected from real students."
    )

    st.subheader("Class Learning Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Demo learners", "30")
    col2.metric("Average class score", "78%")
    col3.metric("Concepts monitored", "3")

    # Sample concept data
    concept_data = pd.DataFrame({
        "Concept": [
            "Balanced Forces",
            "Unbalanced Forces",
            "Friction"
        ],
        "Class Accuracy (%)": [86, 53, 72]
    })

    st.subheader("Concept-level Class Performance")

    st.bar_chart(
        concept_data,
        x="Concept",
        y="Class Accuracy (%)"
    )

    st.write(
        "The overview helps teachers identify concepts "
        "that may need additional classroom attention."
    )

    st.subheader("📌 Suggested Teaching Actions")

    st.markdown("""
    **Balanced Forces**
    - Review with a short real-world demonstration.
    - Ask learners to explain why stationary objects remain at rest.

    **Unbalanced Forces**
    - Revisit resultant force and changes in motion.
    - Use examples involving bicycles, footballs and moving objects.

    **Friction**
    - Compare rough and smooth surfaces.
    - Ask learners to connect friction to everyday situations.
    """)

    st.divider()

    st.subheader("Individual Learning Reports")

    st.caption(
        "Fictional examples for demonstrating the intended report layout."
    )

    learner_reports = {
        "Learner 01": {
            "Balanced Forces": 100,
            "Unbalanced Forces": 50,
            "Friction": 100
        },
        "Learner 02": {
            "Balanced Forces": 50,
            "Unbalanced Forces": 50,
            "Friction": 50
        },
        "Learner 03": {
            "Balanced Forces": 100,
            "Unbalanced Forces": 100,
            "Friction": 50
        }
    }

    selected_learner = st.selectbox(
        "Select a fictional learner report:",
        list(learner_reports.keys())
    )

    learner_scores = learner_reports[selected_learner]

    st.write(f"**Report: {selected_learner}**")

    for concept, score in learner_scores.items():
        st.write(f"**{concept}: {score}%**")
        st.progress(score / 100)

    st.info(
        "A score indicates how a learner performed on this assessment. "
        "It does not define the learner or prove the reason for a mistake."
    )

    st.divider()

    st.subheader("🔐 Privacy and Student Dignity")

    st.markdown("""
    LEARNWISE is designed around these principles:

    - No public student rankings.
    - No labels such as 'weak student' or 'poor learner'.
    - Individual reports should only be available to authorised educators.
    - Learning data should support teaching, not punishment.
    - Teachers remain responsible for interpreting results and deciding
      what support is appropriate.
    - Real student data must only be used with appropriate school
      permission and secure data protections.
    """)

    st.caption(
        "The current dashboard is a demonstration. "
        "It is not connected to a live class database."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LEARNWISE | A prototype for earlier identification "
    "of learning gaps and more targeted classroom support."
)
