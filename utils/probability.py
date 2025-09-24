def calculate_probability(bidder, tender, submission_docs, submission_text=""):
    """
    Returns probability (%) of winning a tender for a bidder.
    Considers documents and proposal content match.
    """
    base_score = 50
    total_docs = len(tender['required_docs'])
    present_docs = [d for d in tender['required_docs'] if d in submission_docs]
    missing_docs = [d for d in tender['required_docs'] if d not in submission_docs]

    # Document score
    doc_score = (len(present_docs) / total_docs) * 50

    # Proposal text match score (simple keyword presence)
    tender_keywords = [word.lower() for word in tender.get('description_keywords', [])]
    proposal_words = submission_text.lower().split()
    if tender_keywords:
        match_count = sum(1 for kw in tender_keywords if kw in proposal_words)
        proposal_score = (match_count / len(tender_keywords)) * 20
    else:
        proposal_score = 0

    # Penalize missing docs
    doc_penalty = (len(missing_docs) / total_docs) * 50

    probability = base_score + doc_score + proposal_score - doc_penalty
    return min(round(probability), 100)


