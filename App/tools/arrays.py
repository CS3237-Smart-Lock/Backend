def is_subarray(larger, smaller):
    n, m = len(larger), len(smaller)
    for i in range(n - m + 1):
        if larger[i:i + m] == smaller:
            return True
    return False

