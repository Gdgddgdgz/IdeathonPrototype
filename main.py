import streamlit as st
from tender_upload import upload_tender
from bidder_upload import add_bidder
from bidder_dashboard import compare_submission, get_tenders, all_bidders_probabilities, submit_proposal
import json
import plotly.express as px

st.set_page_config(page_title="TenderX", layout="wide")
st.title("📝 Tender Ideathon Prototype")

# ------------------ Sidebar ------------------
role = st.sidebar.selectbox("Login as", ["Tender Creator", "Bidder"])
st.sidebar.markdown("---")
if st.sidebar.button("FAQs"):
    st.sidebar.subheader("❓ Generic FAQs")
    with st.sidebar.expander("How is winning probability calculated?"):
        st.write("It uses bidder documents and proposal content against tender requirements.")
    with st.sidebar.expander("Can I submit a tender with missing documents?"):
        st.write("The system flags missing docs and reduces probability.")
    with st.sidebar.expander("Does high rating guarantee winning?"):
        st.write("No, but it increases your chances.")
    with st.sidebar.expander("How often is bidder rating updated?"):
        st.write("After every submission, probability is recalculated.")
    with st.sidebar.expander("Can I see why my profile is low-rated?"):
        st.write("Feedback includes missing docs and proposal match against tender.")

# ------------------ TENDER CREATOR ------------------
if role == "Tender Creator":
    st.header("📤 Tender Creator Dashboard")
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

    st.subheader("Existing Tenders")
    tenders = get_tenders()
    if tenders:
        for t in tenders:
            st.markdown(f"**{t['name']}** - Documents: {', '.join(t['required_docs'])}")
    else:
        st.info("No tenders uploaded yet.")

# ------------------ BIDDER ------------------
elif role == "Bidder":
    st.header("👤 Bidder Dashboard")

    bidder_id = st.number_input("Enter Bidder ID (0 to create new bidder)", min_value=0, step=1)
    create_new = bidder_id == 0

    # Company-specific info
    company_info = {
        1: ["Company: ABC Infra Ltd",
            "Started in 2000",
            "Specializes in building bridges",
            "Projects in 10 cities"],
        2: ["Company: XYZ Infrastructure",
            "Started in 2010",
            "Projects in 5 states",
            "Specializes in road construction"],
    }

    if create_new:
        st.subheader("Create New Bidder")
        bidder_name = st.text_input("Bidder Name")
        docs = st.text_area("Documents (comma separated)")
        if st.button("Add Bidder"):
            if bidder_name and docs:
                documents = [d.strip() for d in docs.split(",")]
                bidder_id = add_bidder(bidder_name, documents)
                st.success(f"Bidder '{bidder_name}' added successfully with ID: {bidder_id}")
            else:
                st.error("Please fill in all fields!")
    else:
        # Load bidder
        with open("data/bidders.json") as f:
            bidders = json.load(f)
        bidder = next((b for b in bidders if b['id'] == bidder_id), None)
        if not bidder:
            st.error("Bidder ID not found")
        else:
            st.success(f"Bidder: {bidder['name']}")

            tenders = get_tenders()
            if not tenders:
                st.info("No tenders available yet.")
            else:
                tender_names = [t['name'] for t in tenders]
                selected_tender = st.selectbox("Select Tender to Submit Proposal", tender_names)

                # Company info always visible
                st.subheader(f"🏢 Company Info: {bidder['name']}")
                if bidder_id in company_info:
                    for info in company_info[bidder_id]:
                        st.markdown(f"- {info}")

                # Proposal submission
                st.subheader("Submit Proposal")
                submission_docs_text = st.text_area("Enter your documents (comma separated)")
                submission_text = st.text_area("Paste your proposal here")

                if st.button("Compare Proposal"):
                    if not submission_docs_text or not submission_text:
                        st.error("Enter documents and proposal text")
                    else:
                        submission_docs = [d.strip() for d in submission_docs_text.split(",")]
                        result = compare_submission(bidder_id, selected_tender, submission_docs, submission_text)
                        if result:
                            prob = result['probability']
                            color = "green" if prob>=70 else ("orange" if prob>=50 else "red")
                            st.markdown(f"**Probability of Winning:** <span style='color:{color}'>{prob}%</span>", unsafe_allow_html=True)

                            st.markdown("**Documents Status:**")
                            for doc in result['present_docs']:
                                st.markdown(f"✅ {doc}")
                            for doc in result['missing_docs']:
                                st.markdown(f"❌ {doc}")

                            st.progress(prob)

                            if result['missing_docs']:
                                st.warning(f"Missing docs: {', '.join(result['missing_docs'])}")
                            if prob < 50:
                                st.info("Consider improving proposal or submitting missing documents.")

                            # Graph
                            all_probs = all_bidders_probabilities(selected_tender)
                            if all_probs:
                                fig = px.bar(all_probs, x="bidder_name", y="probability", color="probability",
                                             color_continuous_scale=["red","orange","green"])
                                fig.update_layout(title=f"All Bidders Probability for '{selected_tender}'")
                                st.plotly_chart(fig, use_container_width=True)

                            # ---------------- Submit Proposal Button ----------------
                            if st.button("Submit Proposal to Tender"):
                                submit_proposal(bidder_id, selected_tender, submission_docs, submission_text)
                                st.success("Proposal submitted successfully!")
                        else:
                            st.error("Bidder or Tender not found.")
