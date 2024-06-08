import hashlib
import math

def gameResult(seed, salt, h=1):
    """
    Calculates the game result based on the provided seed, salt, and h value.

    Args:
        seed (str): The seed string.
        salt (str): The salt string.
        h (int, optional): The value of h (defaults to 1).

    Returns:
        float: The game result.
    """

    nBits = 52  # Number of most significant bits to use

    # 1. HMAC_SHA256(message=seed, key=salt)
    if salt:
        hmac = hashlib.sha256(salt.encode('utf-8') + seed.encode('utf-8')).hexdigest()
        seed = hmac

    # 2. r = 52 most significant bits
    seed = seed[:nBits // 4]
    r = int(seed, 16)

    # 3. X = r / 2^52
    X = r / math.pow(2, nBits)  # Uniformly distributed in [0; 1)
    X = float(format(X, '.9g'))  # Normalize to 9 digits of precision

    # 4. X = (100-h) / (1-X)
    X = (100 - h) / (1 - X)

    # 5. return max(trunc(X), 100)
    result = math.floor(X)
    return max(1, result / 100)

def generate_chain(initial_hash, salt, num_games):
    """
    Generates a chain of hashes using the gameResult function.

    Args:
        initial_hash (str): The initial hash.
        salt (str): The salt string.
        num_games (int): The number of games to generate.

    Returns:
        list: A list of tuples (hash, bust) representing the chain.
    """

    chain = []
    current_hash = initial_hash
    for i in range(num_games):
        bust = gameResult(current_hash, salt)
        chain.append((current_hash, bust))
        current_hash = hashlib.sha256(current_hash.encode('utf-8')).hexdigest()
    return chain

if __name__ == "__main__":
    initial_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    salt = "0000000000000000000301e2801a9a9598bfb114e574a91a887f2132f33047e6"
    num_games = 10000000

    chain = generate_chain(initial_hash, salt, num_games)
    for hash, bust in chain:
        print(f"Hash: {hash}, Bust: {bust}")
