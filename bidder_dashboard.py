import json
import os

# ------------------ Get all tenders ------------------
def get_tenders():
    tenders_file = "data/tenders.json"
    if not os.path.exists(tenders_file):
        return []
    with open(tenders_file, "r") as f:
        return json.load(f)

# ------------------ Compare bidder submission ------------------
def compare_submission(bidder_id, tender_name, submission_docs, proposal_text):
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return None

    required_docs = tender.get('required_docs', [])
    present_docs = [d for d in submission_docs if d in required_docs]
    missing_docs = [d for d in required_docs if d not in submission_docs]

    # Simple keyword match for proposal vs tender keywords
    keywords = tender.get('keywords', [])
    match_count = sum(1 for k in keywords if k.lower() in proposal_text.lower())
    prob_docs = len(present_docs)/len(required_docs) if required_docs else 1
    prob_keywords = match_count/len(keywords) if keywords else 1

    # Simple weighted probability
    probability = int((0.6*prob_docs + 0.4*prob_keywords)*100)

    return {
        "probability": probability,
        "present_docs": present_docs,
        "missing_docs": missing_docs
    }

# ------------------ All bidders probabilities ------------------
def all_bidders_probabilities(tender_name):
    bidders_file = "data/bidders.json"
    if not os.path.exists(bidders_file):
        return []

    with open(bidders_file, "r") as f:
        bidders = json.load(f)

    results = []
    for bidder in bidders:
        bidder_id = bidder['id']
        documents = bidder.get('documents', [])
        proposal_text = bidder.get('proposal', "")
        comp_result = compare_submission(bidder_id, tender_name, documents, proposal_text)
        if comp_result:
            results.append({
                "bidder_name": bidder['name'],
                "probability": comp_result['probability']
            })
    return results

# ------------------ Submit proposal officially ------------------
def submit_proposal(bidder_id, tender_name, documents, proposal_text):
    submissions_file = "data/submissions.json"
    if not os.path.exists(submissions_file):
        with open(submissions_file, "w") as f:
            json.dump([], f)

    # Load existing submissions
    with open(submissions_file, "r") as f:
        submissions = json.load(f)

    # Check if bidder already submitted for this tender, update if so
    updated = False
    for sub in submissions:
        if sub['bidder_id'] == bidder_id and sub['tender_name'] == tender_name:
            sub['documents'] = documents
            sub['proposal'] = proposal_text
            updated = True
            break

    if not updated:
        submissions.append({
            "bidder_id": bidder_id,
            "tender_name": tender_name,
            "documents": documents,
            "proposal": proposal_text
        })

    # Save back
    with open(submissions_file, "w") as f:
        json.dump(submissions, f, indent=4)

    return "Proposal submitted successfully!"
