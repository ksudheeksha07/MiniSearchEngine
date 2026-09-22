import os
import math
import string
import re
import time

from search_engine import normalize_word


# ============================================================
# SETTINGS
# ============================================================

documents_folder = "documents"


# ============================================================
# CLEAN TEXT
# ============================================================

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


# ============================================================
# LOAD DOCUMENTS
# ============================================================

document_files = [
    filename
    for filename in os.listdir(documents_folder)
    if filename.endswith(".txt")
]


# ============================================================
# BUILD INVERTED INDEX
# ============================================================

inverted_index = {}


for filename in document_files:

    file_path = os.path.join(
        documents_folder,
        filename
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    content_words = clean_text(content)

    for word in content_words:

        if word not in inverted_index:

            inverted_index[word] = []

        if filename not in inverted_index[word]:

            inverted_index[word].append(filename)


# ============================================================
# SEARCH HISTORY
# ============================================================

search_history = []


# ============================================================
# SPELLING SUGGESTION
# ============================================================

def get_spelling_suggestion(word):

    word = word.lower().strip()

    best_match = None
    best_distance = float("inf")

    for dictionary_word in inverted_index.keys():

        if abs(len(dictionary_word) - len(word)) > 3:
            continue

        # Simple Levenshtein distance
        rows = len(word) + 1
        cols = len(dictionary_word) + 1

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

                if word[i - 1] == dictionary_word[j - 1]:

                    cost = 0

                else:

                    cost = 1

                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + cost
                )

        distance = matrix[-1][-1]

        if distance < best_distance:

            best_distance = distance
            best_match = dictionary_word

    if best_distance <= 2:

        return best_match

    return None


# ============================================================
# WORD SUGGESTIONS
# ============================================================

def suggest_words(prefix):

    prefix = prefix.lower().strip()

    suggestions = []

    for word in inverted_index.keys():

        if word.startswith(prefix):

            suggestions.append(word)

    suggestions.sort()

    return suggestions[:10]


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search(query):

    start_time = time.perf_counter()

    search_words = clean_text(query)


    # ========================================================
    # EMPTY SEARCH
    # ========================================================

    if not search_words:

        print(
            "Your search contains only common words."
        )

        print(
            "Please enter a more specific search term."
        )

        return


    # ========================================================
    # FIND MATCHING DOCUMENTS
    # ========================================================

    matching_documents = set()

    for word in search_words:

        if word in inverted_index:

            matching_documents.update(
                inverted_index[word]
            )


    # ========================================================
    # REQUIRE ALL WORDS
    # ========================================================

    if len(search_words) > 1:

        exact_matching_documents = set()

        for filename in document_files:

            file_path = os.path.join(
                documents_folder,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            content_words = clean_text(content)

            if all(
                word in content_words
                for word in search_words
            ):

                exact_matching_documents.add(
                    filename
                )

        matching_documents = exact_matching_documents


    # ========================================================
    # NO RESULTS
    # ========================================================

    if not matching_documents:

        print(
            "No exact results found for:",
            query
        )

        # Spelling suggestion

        if len(search_words) == 1:

            suggestion = get_spelling_suggestion(
                search_words[0]
            )

            if suggestion:

                print(
                    "Did you mean:",
                    suggestion + "?"
                )

        return


    # ========================================================
    # TF-IDF RANKING
    # ========================================================

    ranked_results = []

    total_documents = len(document_files)


    for filename in matching_documents:

        file_path = os.path.join(
            documents_folder,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        content_words = clean_text(content)

        score = 0

        matched_words = 0

        phrase_bonus = 0


        # ====================================================
        # PHRASE MATCHING
        # ====================================================

        if len(search_words) > 1:

            phrase = " ".join(search_words)

            cleaned_content = " ".join(
                content_words
            )

            if phrase in cleaned_content:

                phrase_bonus = 0.1


        # ====================================================
        # TF-IDF
        # ====================================================

        for word in search_words:

            term_frequency = (
                content_words.count(word)
                / len(content_words)
                if content_words
                else 0
            )

            if term_frequency > 0:

                matched_words += 1


            document_frequency = len(
                inverted_index.get(
                    word,
                    []
                )
            )


            idf = math.log(
                (total_documents + 1)
                / (document_frequency + 1)
            ) + 1


            tf_idf = (
                term_frequency * idf
            )


            score += tf_idf


        # ====================================================
        # MATCH COVERAGE
        # ====================================================

        match_coverage = (
            matched_words
            / len(search_words)
        )

        coverage_bonus = (
            match_coverage * 0.1
        )


        # ====================================================
        # AND MATCH BONUS
        # ====================================================

        and_bonus = 0

        if matched_words == len(search_words):

            and_bonus = 0.2


        # ====================================================
        # FINAL SCORE
        # ====================================================

        final_score = (
            score
            + phrase_bonus
            + coverage_bonus
            + and_bonus
        )


        ranked_results.append(
            (
                filename,
                final_score,
                matched_words
            )
        )


    # ========================================================
    # SORT RESULTS
    # ========================================================

    ranked_results.sort(
        key=lambda x: (
            x[2],
            x[1]
        ),
        reverse=True
    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    for filename, score, matched_words in ranked_results:

        file_path = os.path.join(
            documents_folder,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()


        # ====================================================
        # CREATE SNIPPET
        # ====================================================

        snippet = (
            content[:100]
            .replace("\n", " ")
        )


        # Find first matching word

        for word in search_words:

            position = content.lower().find(
                word.lower()
            )

            if position != -1:

                start = max(
                    0,
                    position - 40
                )

                end = min(
                    len(content),
                    position + 100
                )

                snippet = (
                    content[start:end]
                    .replace("\n", " ")
                )

                break


        # ====================================================
        # HIGHLIGHT ORIGINAL SEARCH TERMS
        # ====================================================

        original_words = query.lower().split()

        for word in original_words:

            word = word.strip(
                ".,!?;:\"'()[]{}"
            )

            if not word:
                continue

            snippet = re.sub(
                rf"\b{re.escape(word)}\b",
                lambda match:
                f"**{match.group(0)}**",
                snippet,
                flags=re.IGNORECASE
            )


        # ====================================================
        # DISPLAY RESULT
        # ====================================================

        print(
            "\n------------------------------"
        )

        print(
            "📄",
            filename
        )

        print(
            "Matched:",
            matched_words,
            "/",
            len(search_words)
        )

        print(
            "Score:",
            round(score, 3)
        )

        print(
            "Snippet:",
            snippet + "..."
        )


    # ========================================================
    # SEARCH STATISTICS
    # ========================================================

    end_time = time.perf_counter()

    search_time = (
        end_time - start_time
    ) * 1000


    print(
        "Total results:",
        len(ranked_results)
    )

    print(
        "Documents searched:",
        total_documents
    )

    print(
        "Search time:",
        round(search_time, 3),
        "ms"
    )


# ============================================================
# SHOW SEARCH HISTORY
# ============================================================

def show_history():

    print("\nSearch History:")

    if not search_history:

        print("No searches yet.")

        return

    for number, query in enumerate(
        search_history,
        start=1
    ):

        print(
            f"{number}. {query}"
        )


# ============================================================
# CLEAR SEARCH HISTORY
# ============================================================

def clear_history():

    search_history.clear()

    print(
        "\nSearch history cleared."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

print(
    "\n=============================="
)

print(
    "      MINI SEARCH ENGINE"
)

print(
    "=============================="
)

print(
    "Type 'exit' to quit."
)

print(
    "Type 'history' to view search history."
)

print(
    "Type 'suggest <word>' for suggestions."
)

print(
    "Type a misspelled word for a spelling suggestion."
)

print(
    "Type 'clear history' to delete search history."
)

print()


# ============================================================
# CONTINUOUS SEARCH LOOP
# ============================================================

while True:

    search_query = input(
        "What do you want to search for? "
    )


    # ========================================================
    # EXIT
    # ========================================================

    if search_query.lower().strip() == "exit":

        print(
            "\nExiting Mini Search Engine."
        )

        break


    # ========================================================
    # HISTORY
    # ========================================================

    if search_query.lower().strip() == "history":

        show_history()

        continue


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    if search_query.lower().strip() == "clear history":

        clear_history()

        continue


    # ========================================================
    # SUGGEST
    # ========================================================

    if search_query.lower().startswith(
        "suggest "
    ):

        prefix = search_query[
            8:
        ].strip()

        suggestions = suggest_words(
            prefix
        )

        print(
            "\nSuggestions:"
        )

        if suggestions:

            for number, word in enumerate(
                suggestions,
                start=1
            ):

                print(
                    f"{number}. {word}"
                )

        else:

            print(
                "No suggestions found."
            )

        continue


    # ========================================================
    # IGNORE EMPTY INPUT
    # ========================================================

    if not search_query.strip():

        print(
            "Please enter a search term."
        )

        continue


    # ========================================================
    # SAVE SEARCH HISTORY
    # ========================================================

    search_history.append(
        search_query.strip()
    )


    # ========================================================
    # PERFORM SEARCH
    # ========================================================

    search(
        search_query
    )