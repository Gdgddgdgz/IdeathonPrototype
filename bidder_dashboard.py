import json
import os

# Load tenders from JSON
def get_tenders():
    try:
        with open("tenders.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tenders: {e}")
        return []

# Load bidders from JSON
def get_bidders():
    try:
        with open("bidders.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading bidders: {e}")
        return []

# Compare bidder submission against a tender
def compare_submission(bidder, tender):
    required_docs = tender.get("required_documents", [])
    provided_docs = bidder.get("documents", [])

    # Match required vs provided docs
    matched = sum(1 for doc in required_docs if doc in provided_docs)
    doc_score = (matched / len(required_docs)) * 100 if required_docs else 100

    # Get bidder rating
    rating_score = bidder.get("rating", 50)  # default rating = 50 if missing

    # Final probability = 50% docs + 50% rating
    probability = int((doc_score * 0.5) + (rating_score * 0.5))

    return {
        "probability": probability,
        "missing": [doc for doc in required_docs if doc not in provided_docs],
    }

# Calculate probabilities for all bidders for a tender
def all_bidders_probabilities(tender):
    bidders = get_bidders()
    results = []
    for bidder in bidders:
        comparison = compare_submission(bidder, tender)
        results.append({
            "bidder_name": bidder.get("name", "Unknown"),
            "probability": comparison["probability"],
            "missing": comparison["missing"],
        })
    return results

# New: bidder submits a proposal (optional text + docs)
def submit_proposal(bidder_name, tender_name, proposal_text):
    proposals_file = "proposals.json"
    data = []
    if os.path.exists(proposals_file):
        with open(proposals_file, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append({
        "bidder": bidder_name,
        "tender": tender_name,
        "proposal": proposal_text
    })

    with open(proposals_file, "w") as f:
        json.dump(data, f, indent=2)
    return True
