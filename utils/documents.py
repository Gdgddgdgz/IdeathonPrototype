def check_documents(bidder, tender):
    """
    Returns lists of present and missing documents.
    """
    present_docs = [doc for doc in tender['required_docs'] if doc in bidder['documents']]
    missing_docs = [doc for doc in tender['required_docs'] if doc not in bidder['documents']]
    return present_docs, missing_docs

