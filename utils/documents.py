def check_documents(submission_docs, tender):
    """
    Returns present and missing documents for a submission
    """
    present_docs = [doc for doc in tender['required_docs'] if doc in submission_docs]
    missing_docs = [doc for doc in tender['required_docs'] if doc not in submission_docs]
    return present_docs, missing_docs

