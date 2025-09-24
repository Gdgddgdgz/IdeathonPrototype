import streamlit as st
from tender_upload import upload_tender
from bidder_dashboard import view_tenders
from bidder_upload import add_bidder

st.set_page_config(page_title="TenderMirror", layout="wide")
st.title("📝 TenderX Ideathon Demo")
st.sidebar.header("Menu")
menu = ["Tender Creator", "Bidder Creator", "Bidder Dashboard", "FAQs"]
choice = st.sidebar.selectbox("Go to", menu)

# ------------------ TENDER CREATOR ------------------
if choice == "Tender Creator":
    st.header("📤 Upload Tender")
    tender_name = st.text_input("Tender Name")
    docs = st.text_area("Required Documents (comma separated)")

    if st.button("Upload Tender"):
        if tender_name and docs:
            required_docs = [d.strip() for d in docs.split(",")]
            message = upload_tender(tender_name, required_docs)
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

    min_prob = st.sidebar.slider("Minimum Winning Probability %", 0, 100, 0)
    show_high_rated = st.sidebar.checkbox("Show High-Rated Only", value=False)

    if st.button("View Tenders"):
        try:
            tenders_status = view_tenders(bidder_id)

            filtered = []
            for t in tenders_status:
                prob = t['probability']
                rating = t['rating']
                if prob >= min_prob:
                    if show_high_rated and rating != 'high':
                        continue
                    filtered.append(t)

            if not filtered:
                st.info("No tenders match the selected filters.")
            else:
                for t in filtered:
                    with st.expander(t['tender_name']):
                        # Colored rating
                        color = "green" if t['rating'] == "high" else ("orange" if t['rating']=="medium" else "red")
                        st.markdown(f"<span style='color:{color}; font-weight:bold'>{t['rating'].upper()} RATED</span>", unsafe_allow_html=True)
                        st.markdown(f"**Probability:** {t['probability']}%")
                        st.markdown("**Documents:**")
                        for doc in t['present_docs']:
                            st.markdown(f"✅ {doc}")
                        for doc in t['missing_docs']:
                            st.markdown(f"❌ {doc}")

        except Exception as e:
            st.error(f"Error loading bidder data: {e}")

# ------------------ FAQ SECTION ------------------
elif choice == "FAQs":
    st.header("❓ FAQs")

    with st.expander("How is winning probability calculated?"):
        st.write("It uses bidder documents and historical performance to estimate the chance of winning a tender.")

    with st.expander("Can I submit a tender with missing documents?"):
        st.write("The software will flag incomplete submissions and reduce the probability score.")

    with st.expander("Does high rating guarantee winning?"):
        st.write("No. High rating increases chances, but tender-specific factors matter.")

    with st.expander("How often is bidder rating updated?"):
        st.write("After each tender submission, ratings are recalculated automatically.")

    with st.expander("Can I see why my profile is low-rated?"):
        st.write("Yes. The software provides feedback on past tenders, document gaps, and on-time submission stats.")

    with st.expander("Is my data secure?"):
        st.write("Yes. We use encryption and secure storage to protect your information.")
