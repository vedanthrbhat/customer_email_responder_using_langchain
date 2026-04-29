# ---------------- Streamlit UI ----------------
from main import generate_response
import streamlit as st

st.set_page_config(
    page_title="AI Email Responder",
    page_icon="📧",
    layout="wide",
)

# Header
st.title("📧 AI Email Responder")
st.caption("Automatically classify customer emails and generate professional replies using LLM chains.")

# Sidebar
with st.sidebar:
    st.header("⚙️ About")
    st.markdown(
        """
        This app uses a **two-step LLM pipeline**:
        1. **Intent Chain** — classifies the email's intent  
        2. **Response Chain** — drafts a reply based on the intent
        """
    )
    st.divider()
    st.subheader("📝 Sample Emails")
    samples = {
        "Refund Issue": "Hi,\nI haven't received my refund yet.\nPlease help.",
        "Order Status": "Hello,\nCan you tell me where my order #12345 is?\nThanks.",
        "Complaint": "I'm very disappointed with the product quality. It broke after one day!",
        "General Inquiry": "Hi team,\nDo you ship internationally?\nRegards.",
    }
    selected_sample = st.selectbox("Load a sample", ["-- None --"] + list(samples.keys()))

# Initialize session state
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

if selected_sample != "-- None --":
    st.session_state.email_text = samples[selected_sample]

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("✉️ Customer Email")
    email_input = st.text_area(
        "Paste the customer's email below:",
        value=st.session_state.email_text,
        height=300,
        placeholder="Hi,\nI haven't received my refund yet.\nPlease help.",
    )

    generate_btn = st.button("🚀 Generate Reply", type="primary", use_container_width=True)

with col2:
    st.subheader("🤖 AI Response")

    if generate_btn:
        if not email_input.strip():
            st.warning("⚠️ Please enter an email first.")
        else:
            try:
                with st.spinner("Analyzing intent and drafting reply..."):
                    intent, reply = generate_response(email_input)

                st.success("✅ Reply generated successfully!")

                # Show intent badge
                st.markdown(f"**Detected Intent:** `{intent}`")

                # Show reply
                st.markdown("**Suggested Reply:**")
                st.text_area("Reply", value=reply, height=250, label_visibility="collapsed")

                # Download button
                st.download_button(
                    label="⬇️ Download Reply as .txt",
                    data=f"Intent: {intent}\n\nReply:\n{reply}",
                    file_name="email_reply.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.info("👈 Enter an email and click **Generate Reply** to see the AI response.")

# Footer
st.divider()
st.caption("Built with 🦜 LangChain + Streamlit")