def calculate_probability(bidder, tender):
    base_score = 50
    total_docs = len(tender['required_docs'])
    present_docs = [d for d in tender['required_docs'] if d in bidder['documents']]
    missing_docs = [d for d in tender['required_docs'] if d not in bidder['documents']]

    # Document score
    doc_score = (len(present_docs) / total_docs) * 50

    # Penalize for missing docs
    doc_penalty = (len(missing_docs) / total_docs) * 50

    probability = base_score + doc_score - doc_penalty
    return min(round(probability), 100)

