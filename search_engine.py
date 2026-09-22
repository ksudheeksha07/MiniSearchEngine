from pathlib import Path
import string
import math
import re


# -------------------------------
# DOCUMENT FOLDER
# -------------------------------

documents_folder = (
    Path(__file__).resolve().parent / "documents"
)


# -------------------------------
# WORD NORMALIZATION
# -------------------------------

def normalize_word(word):

    word = word.lower().strip(string.punctuation)

    word_families = {

        "connection": "connect",
        "connections": "connect",
        "connected": "connect",
        "connecting": "connect",
        "connects": "connect",

        "programming": "program",
        "programmed": "program",
        "programs": "program",

        "learning": "learn",
        "learned": "learn",
        "learns": "learn",

        "computers": "computer",
        "computing": "compute"
    }

    if word in word_families:
        return word_families[word]

    if word.endswith("ing") and len(word) > 5:

        word = word[:-3]

        if len(word) >= 2 and word[-1] == word[-2]:
            word = word[:-1]

        return word

    if word.endswith("ed") and len(word) > 4:
        return word[:-2]

    if word.endswith("ly") and len(word) > 4:
        return word[:-2]

    if word.endswith("es") and len(word) > 4:
        return word[:-2]

    if word.endswith("s") and len(word) > 3:
        return word[:-1]

    return word


# -------------------------------
# CLEAN TEXT
# -------------------------------

def clean_text(text):

    stop_words = {
        "the", "is", "a", "an", "and",
        "in", "of", "to", "for", "on",
        "are", "was", "were", "with",
        "that", "this", "from", "by"
    }

    words = text.lower().translate(
        str.maketrans("", "", string.punctuation)
    ).split()

    cleaned_words = []

    for word in words:

        if word and word not in stop_words:

            word = normalize_word(word)

            cleaned_words.append(word)

    return cleaned_words


# -------------------------------
# LOAD DOCUMENTS
# -------------------------------

document_files = [
    file_path.name
    for file_path in documents_folder.glob("*.txt")
]


# -------------------------------
# BUILD INVERTED INDEX
# -------------------------------

inverted_index = {}

for filename in document_files:

    file_path = documents_folder / filename

    content = file_path.read_text(
        encoding="utf-8"
    )

    content_words = clean_text(content)

    for word in content_words:

        if word not in inverted_index:
            inverted_index[word] = set()

        inverted_index[word].add(filename)


# -------------------------------
# FIND DOCUMENTS
# -------------------------------

def find_documents(query):

    search_words = clean_text(query)

    if not search_words:
        return set()

    matching_documents = set()

    for word in search_words:

        if word in inverted_index:

            matching_documents.update(
                inverted_index[word]
            )

    # Require all words for multi-word search
    if len(search_words) > 1:

        exact_matching_documents = set()

        for filename in document_files:

            file_path = documents_folder / filename

            content = file_path.read_text(
                encoding="utf-8"
            )

            content_words = clean_text(content)

            if all(
                word in content_words
                for word in search_words
            ):

                exact_matching_documents.add(
                    filename
                )

        matching_documents = (
            exact_matching_documents
        )

    return matching_documents


# -------------------------------
# HIGHLIGHT SEARCH TERMS
# -------------------------------

def highlight_text(text, original_words):

    for word in original_words:

        word = word.strip(
            ".,!?;:\"'()[]{}"
        )

        if not word:
            continue

        text = re.sub(
            rf"\b{re.escape(word)}\b",
            lambda match:
                f"<strong>{match.group(0)}</strong>",
            text,
            flags=re.IGNORECASE
        )

    return text


# -------------------------------
# CREATE SNIPPET
# -------------------------------

def create_snippet(content, original_words):

    snippet = (
        content[:180]
        .replace("\n", " ")
    )

    lower_content = content.lower()

    for word in original_words:

        clean_word = word.strip(
            ".,!?;:\"'()[]{}"
        )

        if not clean_word:
            continue

        position = lower_content.find(
            clean_word.lower()
        )

        if position != -1:

            start = max(
                0,
                position - 60
            )

            end = min(
                len(content),
                position + 140
            )

            snippet = (
                content[start:end]
                .replace("\n", " ")
            )

            break

    return highlight_text(
        snippet,
        original_words
    )


# -------------------------------
# SEARCH RESULTS
# -------------------------------

def search_results(query):

    search_words = clean_text(query)

    if not search_words:
        return []

    matching_documents = find_documents(query)

    if not matching_documents:
        return []

    total_documents = len(document_files)

    results = []

    original_words = query.split()

    for filename in matching_documents:

        file_path = documents_folder / filename

        content = file_path.read_text(
            encoding="utf-8"
        )

        content_words = clean_text(content)

        score = 0
        matched_words = 0
        phrase_bonus = 0

        # -------------------------------
        # PHRASE BONUS
        # -------------------------------

        if len(search_words) > 1:

            phrase = " ".join(search_words)

            cleaned_content = " ".join(
                content_words
            )

            if phrase in cleaned_content:

                phrase_bonus = 0.1

        # -------------------------------
        # TF-IDF
        # -------------------------------

        for word in search_words:

            if not content_words:
                continue

            term_frequency = (
                content_words.count(word)
                / len(content_words)
            )

            if term_frequency > 0:
                matched_words += 1

            document_frequency = len(
                inverted_index.get(word, set())
            )

            idf = math.log(
                (total_documents + 1)
                / (document_frequency + 1)
            ) + 1

            score += (
                term_frequency * idf
            )

        # -------------------------------
        # COVERAGE BONUS
        # -------------------------------

        match_coverage = (
            matched_words
            / len(search_words)
        )

        coverage_bonus = (
            match_coverage * 0.1
        )

        # -------------------------------
        # AND BONUS
        # -------------------------------

        and_bonus = 0

        if matched_words == len(search_words):
            and_bonus = 0.2

        # -------------------------------
        # FINAL SCORE
        # -------------------------------

        final_score = (
            score
            + phrase_bonus
            + coverage_bonus
            + and_bonus
        )

        snippet = create_snippet(
            content,
            original_words
        )

        results.append({

            "filename": filename,

            "score": round(
                final_score,
                3
            ),

            "matched_words": matched_words,

            "total_words": len(
                search_words
            ),

            "snippet": snippet
        })

    results.sort(
        key=lambda result: (
            result["matched_words"],
            result["score"]
        ),
        reverse=True
    )

    return results


# -------------------------------
# LEVENSHTEIN DISTANCE
# -------------------------------

def levenshtein_distance(word1, word2):

    rows = len(word1) + 1
    cols = len(word2) + 1

    matrix = [
        [0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):
        matrix[i][0] = i

    for j in range(cols):
        matrix[0][j] = j

    for i in range(1, rows):

        for j in range(1, cols):

            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

    return matrix[-1][-1]


# -------------------------------
# SPELLING SUGGESTION
# -------------------------------

def get_spelling_suggestion(word):

    word = word.lower().strip(
        string.punctuation
    )

    if not word:
        return None

    vocabulary = list(
        inverted_index.keys()
    )

    best_word = None
    best_distance = float("inf")

    for candidate in vocabulary:

        distance = levenshtein_distance(
            word,
            candidate
        )

        if distance < best_distance:

            best_distance = distance
            best_word = candidate

    if best_distance <= 2:
        return best_word

    return None


# -------------------------------
# SEARCH SUGGESTIONS
# -------------------------------
def get_suggestions(prefix, limit=5):
    prefix = prefix.lower().strip(
        string.punctuation
    )
    if not prefix:
        return []
    suggestions = []
    for word in inverted_index:
        if word.startswith(prefix):
            suggestions.append(word)
    suggestions.sort()
    return suggestions[:limit]