"""
collection: figures out which coins the player has collected this frame.
"""


def check_collection(player, coins):
    """
    Returns the list of coins the player is currently overlapping.
    """
    player_rect = player.get_rect()
    collected = []
    for coin in coins:
        if player_rect.colliderect(coin.get_rect()):
            collected.append(coin)
    return collected
