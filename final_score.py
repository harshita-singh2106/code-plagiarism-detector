from lexical import tokenize
from semantic import extract_features
from normalize import normalize_code


def get_ngrams(tokens, n=3):
    return list(zip(*[tokens[i:] for i in range(n)]))


def ngram_similarity(t1, t2):
    ngrams1 = set(get_ngrams(t1))
    ngrams2 = set(get_ngrams(t2))

    return len(ngrams1 & ngrams2) / len(ngrams1 | ngrams2) if (ngrams1 | ngrams2) else 1.0


def calculate_score(code1, code2):

    # -------- NORMALIZE --------
    code1 = normalize_code(code1)
    code2 = normalize_code(code2)

    # -------- TOKENS --------
    tokens1 = tokenize(code1)
    tokens2 = tokenize(code2)

    # -------- LEXICAL --------
    t1 = set(tokens1)
    t2 = set(tokens2)
    lexical_score = len(t1 & t2) / len(t1 | t2) if (t1 | t2) else 1.0

    # -------- NGRAM --------
    ngram_score = ngram_similarity(tokens1, tokens2)

    # -------- SEMANTIC --------
    f1 = extract_features(code1)
    f2 = extract_features(code2)
    semantic_score = len(f1 & f2) / len(f1 | f2) if (f1 | f2) else 1.0

    # -------- FINAL --------
    final_score = (
        0.25 * lexical_score +
        0.35 * ngram_score +
        0.40 * semantic_score
    )

    return lexical_score, ngram_score, semantic_score, final_score