import streamlit as st

# Page configuration
st.set_page_config(page_title="MediConnect Support", page_icon="💬", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #ffffff; }

/* Force title and text to black */
h1, h2, h3, h4, h5, h6, p, div, span {
    color: #000000 !important;
}

/* Chat bubbles */
.user-msg { background-color: #C6E2FF; padding: 10px; border-radius: 12px; margin: 5px 0; text-align: right; color: #000; max-width: 70%; margin-left: auto; }
.bot-msg { background-color: #F1F0F0; padding: 10px; border-radius: 12px; margin: 5px 0; text-align: left; color: #000; max-width: 70%; margin-right: auto; }

/* Input box text color */
div.stTextInput > label, input[type="text"] { color: #000000; }

/* Placeholder text color */
input::placeholder { color: #555555; }
</style>
""", unsafe_allow_html=True)

# Title and welcome text
st.title("💬 MediConnect - Customer Support")
st.write("Welcome to **MediConnect**! How can we assist you today?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_input("💡 Type your question here:", placeholder="Type your message here...")
    submit_button = st.form_submit_button("Send")

if submit_button and query:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": query})

    # Sample bot responses
    sample_responses = {
        "doctor": "We have specialized doctors in Pediatrics, Cardiology, Dermatology, and Neurology. Would you like to book an appointment?",
        "appointment": "To book an appointment, please provide your preferred doctor and time slot.",
        "location": "📍 MediConnect is located at No. 123, Galle Road, Colombo 03.",
        "contact": "☎️ You can reach us at +94 77 123 4567 or support@mediconnect.lk.",
        "default": "✅ Thank you for your query! Our support team will get back to you shortly."
    }

    # Determine bot response
    response = sample_responses.get(
        next((k for k in sample_responses if k in query.lower()), "default")
    )

    # Save bot response
    st.session_state["messages"].append({"role": "bot", "content": response})

