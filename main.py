import streamlit as st
from tender_upload import upload_tender
from bidder_dashboard import view_tenders

st.set_page_config(page_title="TenderMirror", layout="wide")
st.title("📝 TenderMirror Hackathon Demo")
st.sidebar.header("Menu")
menu = ["Tender Creator", "Bidder Dashboard", "FAQs"]
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

# ------------------ BIDDER DASHBOARD ------------------
elif choice == "Bidder Dashboard":
    st.header("👤 Bidder Dashboard")
    bidder_id = st.number_input("Enter Bidder ID", min_value=1, step=1)

    min_prob = st.sidebar.slider("Minimum Winning Probability %", 0, 100, 0)
    show_high_rated = st.sidebar.checkbox("Show High-Rated Only", value=False)

    if st.button("View Tenders"):
        try:
            tenders_status = view_tenders(bidder_id)
            # DEBUG: Check output
           # st.write(tenders_status)

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
                        color = "green" if t['rating'] == "high" else "red"
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
    st.write("""
    **How is winning probability calculated?**  
    Based on bidder documents and historical performance.

    **Can I submit a tender with missing documents?**  
    Software flags incomplete submission and lowers probability.

    **Does high rating guarantee winning?**  
    No, but it increases chances.

    **How often is bidder rating updated?**  
    After every tender submission.

    **Why is my profile low-rated?**  
    Feedback includes past tender success, documents missing, and timeliness.
    """)
