import json

def add_bidder(name, documents):
    """
    Adds a new bidder to bidders.json
    """
    new_bidder = {"id": None, "name": name, "documents": documents}

    try:
        with open("data/bidders.json") as f:
            bidders = json.load(f)
    except FileNotFoundError:
        bidders = []

    new_bidder["id"] = max([b['id'] for b in bidders], default=0) + 1
    bidders.append(new_bidder)

    with open("data/bidders.json", "w") as f:
        json.dump(bidders, f, indent=4)
    return new_bidder["id"]
