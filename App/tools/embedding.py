def decode_to_vector(s: str) -> list[float]:
    """
    Given a string that looks like 1,2,2,1, ... , decode it into a matrix like 1d vector
    """
    return [float(num) for num in s.split(",")]
