def polynomial_hash(s):
    hash_value = 0
    for i in range(len(s)):
        hash_value += ord(s[i]) * (26 ** (len(s) - i - 1))
    return hash_value

def polynomial_rolling_hash(previous_hash, c1, c2, pattern_length):
    return (previous_hash - ord(c1) * (26 ** (pattern_length - 1))) * 26 + ord(c2)

def rabin_karp_algorithm_multiple(patterns, text):
    occurrences = {pattern: 0 for pattern in patterns}
    patterns_by_length = {}
    for pattern in patterns:
        patterns_by_length.setdefault(len(pattern), []).append(pattern)
    pattern_hashes = {pattern: polynomial_hash(pattern) for pattern in patterns}
    text_length = len(text)
    
    for length, plist in patterns_by_length.items():
        if length > text_length:
            continue
        substring_hash = polynomial_hash(text[:length])
        for pattern in plist:
            if substring_hash == pattern_hashes[pattern] and text[:length] == pattern:
                occurrences[pattern] += 1
        for i in range(1, text_length - length + 1):
            prev_char = text[i - 1]
            next_char = text[i + length - 1]
            substring_hash = polynomial_rolling_hash(substring_hash, prev_char, next_char, length)
            for pattern in plist:
                if substring_hash == pattern_hashes[pattern] and text[i:i+length] == pattern:
                    occurrences[pattern] += 1
    return occurrences

def rabin_karp_multiple_texts(patterns, texts):
    results = {}
    for idx, text in enumerate(texts):
        results[idx] = rabin_karp_algorithm_multiple(patterns, text)
    return results

# Example usage
patterns = ['ABC', 'BCD', 'CDE', 'DEF']
texts = ['ABCBCDCDEDEF', 'CDEABCDEF', 'XYZABCBCD']
results = rabin_karp_multiple_texts(patterns, texts)

for idx, occ in results.items():
    print(f"Text {idx}: {occ}")
