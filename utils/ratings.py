def get_rating(bidder):
    """
    Returns high/low rating based on previous wins
    """
    if bidder['tenders_won'] >= 3 and bidder['on_time'] >= 80:
        return 'high'
    return 'low'
