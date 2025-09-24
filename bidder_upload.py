import json

def add_bidder(name, documents):
    """
    Adds a new bidder to bidders.json
    """
    new_bidder = {
        "id": None,
        "name": name,
        "documents": documents
    }

    # Load existing bidders
    try:
        with open("data/bidders.json") as f:
            bidders = json.load(f)
    except FileNotFoundError:
        bidders = []

    # Assign a new ID
    if bidders:
        new_bidder["id"] = max(b['id'] for b in bidders) + 1
    else:
        new_bidder["id"] = 1

    bidders.append(new_bidder)

    # Save back
    with open("data/bidders.json", "w") as f:
        json.dump(bidders, f, indent=4)

    return new_bidder["id"]
