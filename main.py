import streamlit as st
from tender_upload import upload_tender
from bidder_upload import add_bidder
from bidder_dashboard import (
    compare_submission,
    get_tenders,
    all_bidders_probabilities,
    submit_proposal,
    add_review,
    get_reviews
)
import json
import plotly.express as px

# ---------------- Page config ----------------
st.set_page_config(page_title="TenderX", layout="wide")

# ---------------- Centered Top Title ----------------
st.markdown(
    """
    <h1 style='text-align: center; margin-top: 0px;'>📝 TenderX Ideathon Prototype</h1>
    """,
    unsafe_allow_html=True
)

# ------------------ Sidebar ------------------
menu = st.sidebar.radio("Navigate", ["Tender Creator", "Bidder", "Reviews", "FAQs"])

# ------------------ TENDER CREATOR ------------------
if menu == "Tender Creator":
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
elif menu == "Bidder":
    st.header("👤 Bidder Dashboard")

    bidder_id = st.number_input("Enter Bidder ID (0 to create new bidder)", min_value=0, step=1)
    create_new = bidder_id == 0

    company_info = {
        1: ["Company: Bidder 1",
            "Started in 2015",
            "Provides Road infrastructure solutions",
            "Specializes in highway construction"],
        2: ["Company: Bidder 2",
            "Started in 2018",
            "Provides bridge construction services",
            "Specializes in bridge infrastructure projects"],
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
        try:
            with open("data/bidders.json") as f:
                bidders = json.load(f)
        except FileNotFoundError:
            bidders = []

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

                st.subheader(f"🏢 Company Info: {bidder['name']}")
                if bidder_id in company_info:
                    for info in company_info[bidder_id]:
                        st.markdown(f"- {info}")

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
                            color = "green" if prob >= 70 else ("orange" if prob >= 50 else "red")
                            st.markdown(
                                f"**Probability of Winning:** <span style='color:{color}'>{prob}%</span>",
                                unsafe_allow_html=True
                            )

                            st.markdown("**Documents Status:**")
                            for doc in result['present_docs']:
                                st.markdown(f"✅ {doc}")
                            for doc in result['missing_docs']:
                                st.markdown(f"❌ {doc}")

                            st.progress(prob)

                            if result['missing_docs'] or prob < 50:
                                st.info("💡 Suggestions to improve proposal:")
                                for sug in result.get("suggestions", []):
                                    st.markdown(f"- {sug}")

                            all_probs = all_bidders_probabilities(selected_tender)
                            if all_probs:
                                fig = px.bar(all_probs, x="bidder_name", y="probability", color="probability",
                                             color_continuous_scale=["red", "orange", "green"])
                                fig.update_layout(title=f"All Bidders Probability for '{selected_tender}'")
                                st.plotly_chart(fig, use_container_width=True)

                            if st.button("Submit Proposal to Tender"):
                                submit_proposal(bidder_id, selected_tender, submission_docs, submission_text)
                                st.success("Proposal submitted successfully!")

                            # ------------------ Tender Reviews (inside Bidder workflow) ------------------
                            st.subheader("🌟 Tender Review for this Submission")
                            rating = st.slider("Rating", 1, 5, 3, key=f"rating_{bidder_id}_{selected_tender}")
                            review_text = st.text_area("Write Review", key=f"review_{bidder_id}_{selected_tender}")
                            if st.button("Submit Review", key=f"reviewbtn_{bidder_id}_{selected_tender}"):
                                add_review(selected_tender, bidder_id, rating, review_text)
                                st.success("Review added successfully!")

# ------------------ REVIEWS ------------------
elif menu == "Reviews":
    st.header("🌟 Tender Reviews & Ratings")

    with st.expander("Add Review for Submission"):
        tenders = get_tenders()
        if tenders:
            tender_name = st.selectbox("Select Tender", [t["name"] for t in tenders])
            bidder_id = st.text_input("Enter Bidder ID")
            rating = st.slider("Rating", 1, 5, 3)
            review_text = st.text_area("Write Review")
            if st.button("Submit Review"):
                add_review(tender_name, bidder_id, rating, review_text)
                st.success("Review added successfully!")
        else:
            st.info("No tenders available to review.")

    with st.expander("View Reviews"):
        tenders = get_tenders()
        if tenders:
            tender_name = st.selectbox("Select Tender to View Reviews", [t["name"] for t in tenders])
            reviews = get_reviews(tender_name)
            if reviews:
                for r in reviews:
                    st.write(f"**Bidder:** {r['bidder_id']} | **Rating:** {r['rating']} 🌟")
                    st.write(f"Review: {r['review']}")
                    st.markdown("---")
            else:
                st.info("No reviews yet for this tender.")
        else:
            st.info("No tenders available.")

# ------------------ FAQS PAGE ------------------
elif menu == "FAQs":
    st.header("❓ Frequently Asked Questions")

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




