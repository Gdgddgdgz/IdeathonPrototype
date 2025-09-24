import streamlit as st
from tender_upload import upload_tender
from bidder_upload import add_bidder
from bidder_dashboard import compare_submission, get_tenders, all_bidders_probabilities
import plotly.express as px

st.set_page_config(page_title="TenderMirror", layout="wide")
st.title("📝 TenderX Ideathon Prototype")
st.sidebar.header("Menu")
menu = ["Tender Creator", "Bidder Creator", "Bidder Dashboard", "FAQs"]
choice = st.sidebar.selectbox("Go to", menu)

# ------------------ TENDER CREATOR ------------------
if choice == "Tender Creator":
    st.header("📤 Upload Tender")
    tender_name = st.text_input("Tender Name")
    docs = st.text_area("Required Documents (comma separated)")
    keywords = st.text_area("Keywords for Proposal Matching (comma separated)")

    if st.button("Upload Tender"):
        if tender_name and docs:
            required_docs = [d.strip() for d in docs.split(",")]
            description_keywords = [k.strip() for k in keywords.split(",")] if keywords else []
            message = upload_tender(tender_name, required_docs, description_keywords)
            st.success(message)
        else:
            st.error("Please fill in all fields!")

# ------------------ BIDDER CREATOR ------------------
elif choice == "Bidder Creator":
    st.header("👤 Create New Bidder")
    bidder_name = st.text_input("Bidder Name")
    docs = st.text_area("Documents (comma separated)")
    if st.button("Add Bidder"):
        if bidder_name and docs:
            documents = [d.strip() for d in docs.split(",")]
            bidder_id = add_bidder(bidder_name, documents)
            st.success(f"Bidder '{bidder_name}' added successfully with ID: {bidder_id}")
        else:
            st.error("Please fill in all fields!")

# ------------------ BIDDER DASHBOARD ------------------
elif choice == "Bidder Dashboard":
    st.header("👤 Bidder Dashboard")
    bidder_id = st.number_input("Enter Bidder ID", min_value=1, step=1)
    tenders = get_tenders()
    if not tenders:
        st.info("No tenders available yet.")
    else:
        tender_names = [t['name'] for t in tenders]
        selected_tender = st.selectbox("Select Tender to Submit Proposal", tender_names)

        submission_docs_text = st.text_area("Enter your documents for submission (comma separated)")
        submission_text = st.text_area("Paste your proposal text here")

        if st.button("Compare Proposal"):
            if not submission_docs_text or not submission_text:
                st.error("Please enter documents and proposal text")
            else:
                submission_docs = [d.strip() for d in submission_docs_text.split(",")]
                result = compare_submission(bidder_id, selected_tender, submission_docs, submission_text)
                if result:
                    # Individual bidder result
                    prob = result['probability']
                    color = "green" if prob>=70 else ("orange" if prob>=50 else "red")
                    st.markdown(f"**Probability of Winning:** <span style='color:{color}'>{prob}%</span>", unsafe_allow_html=True)

                    st.markdown("**Documents Status:**")
                    for doc in result['present_docs']:
                        st.markdown(f"✅ {doc}")
                    for doc in result['missing_docs']:
                        st.markdown(f"❌ {doc}")

                    # Visual probability bar
                    st.progress(prob)

                    # Suggestions
                    if result['missing_docs']:
                        st.warning(f"Missing documents: {', '.join(result['missing_docs'])}")
                    if prob < 50:
                        st.info("Consider improving your proposal or submitting missing documents.")

                    # ---------------- Graph: All bidders probability for this tender ----------------
                    all_probs = all_bidders_probabilities(selected_tender)
                    if all_probs:
                        fig = px.bar(all_probs, x="bidder_name", y="probability", color="probability",
                                     color_continuous_scale=["red","orange","green"],
                                     labels={"probability":"Winning Probability (%)", "bidder_name":"Bidder"})
                        fig.update_layout(title="All Bidders Probability for this Tender")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Bidder or Tender not found.")

# ------------------ FAQ SECTION ------------------
elif choice == "FAQs":
    st.header("❓ FAQs")
    with st.expander("How is winning probability calculated?"):
        st.write("It uses bidder documents and proposal content against tender requirements.")
    with st.expander("Can I submit a tender with missing documents?"):
        st.write("The system flags missing docs and reduces probability.")
    with st.expander("Does high rating guarantee winning?"):
        st.write("No, but it increases your chances.")
    with st.expander("How often is bidder rating updated?"):
        st.write("After every submission, probability is recalculated.")
    with st.expander("Can I see why my profile is low-rated?"):
        st.write("Feedback includes missing docs and proposal match against tender.")
    with st.expander("Is my data secure?"):
        st.write("Yes. We use encryption and secure storage to protect your information.")
