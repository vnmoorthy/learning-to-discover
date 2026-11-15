WORD_LENGTH = 16
MAX_WORDS = 1 << 14


def descendants(word):
    result = set()
    for i in range(WORD_LENGTH - 1):
        for j in range(i + 1, WORD_LENGTH):
            result.add(word[:i] + word[i + 1:j] + word[j + 1:])
    return result


def evaluate(solution: dict) -> float:
    words = solution["words"]
    if not isinstance(words, list) or not 1 <= len(words) <= MAX_WORDS:
        raise ValueError("Expected between 1 and 16384 codewords")

    checked = set()
    used_descendants = set()
    for word in words:
        if (
            not isinstance(word, str)
            or len(word) != WORD_LENGTH
            or any(bit not in "01" for bit in word)
        ):
            raise ValueError("Every codeword must contain exactly 16 binary digits")
        if word in checked:
            raise ValueError("Codewords must be distinct")
        checked.add(word)

        current_descendants = descendants(word)
        if not used_descendants.isdisjoint(current_descendants):
            raise ValueError("Two codewords share a two-deletion descendant")
        used_descendants.update(current_descendants)

    return float(len(words))