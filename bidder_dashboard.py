import json
from utils.probability import calculate_probability
from utils.documents import check_documents

def view_tenders(bidder_id):
    """
    Returns list of tenders with probability, documents, and dynamic rating.
    """
    # Load bidders
    with open("data/bidders.json") as f:
        bidders = json.load(f)
    bidder = next((b for b in bidders if b['id'] == bidder_id), None)
    if not bidder:
        raise ValueError("Bidder ID not found!")

    # Load tenders
    with open("data/tenders.json") as f:
        tenders = json.load(f)

    tender_status = []
    for tender in tenders:
        prob = calculate_probability(bidder, tender)
        rating = 'high' if prob >= 70 else 'low'
        present_docs, missing_docs = check_documents(bidder, tender)

        tender_status.append({
            "tender_name": tender['name'],
            "probability": prob,
            "present_docs": present_docs,
            "missing_docs": missing_docs,
            "rating": rating  # ✅ ensures rating key exists
        })

    return tender_status

