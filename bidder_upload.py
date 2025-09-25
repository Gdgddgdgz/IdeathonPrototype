import json
import os

DATA_DIR = "data"
BIDDERS_FILE = os.path.join(DATA_DIR, "bidders.json")

# Ensure data dir and file exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(BIDDERS_FILE):
    with open(BIDDERS_FILE, "w") as f:
        json.dump([], f)

def add_bidder(name, documents):
    with open(BIDDERS_FILE, "r") as f:
        bidders = json.load(f)

    new_id = len(bidders) + 1
    new_bidder = {
        "id": new_id,
        "name": name,
        "documents": documents
    }
    bidders.append(new_bidder)

    with open(BIDDERS_FILE, "w") as f:
        json.dump(bidders, f, indent=2)

    return new_id

