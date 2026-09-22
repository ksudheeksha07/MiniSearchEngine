import os

import search_engine
import semantic_search


# ---------------------------------------
# DEPLOYMENT CONFIGURATION
# ---------------------------------------

ENABLE_SEMANTIC_SEARCH = (
    os.environ.get(
        "ENABLE_SEMANTIC_SEARCH",
        "true"
    ).lower()
    == "true"
)


# ---------------------------------------
# NORMALIZE A SCORE
# ---------------------------------------

def normalize_score(score, min_score, max_score):

    if max_score == min_score:

        if max_score > 0:
            return 1.0

        return 0.0

    return (
        (score - min_score)
        / (max_score - min_score)
    )


# ---------------------------------------
# HYBRID SEARCH
# ---------------------------------------

def hybrid_search(
    query,
    keyword_weight=0.5,
    semantic_weight=0.5,
    limit=5
):

    # -----------------------------------
    # KEYWORD SEARCH
    # -----------------------------------

    keyword_results = (
        search_engine.search_results(query)
    )

    # -----------------------------------
    # DEPLOYMENT MODE
    # -----------------------------------

    if not ENABLE_SEMANTIC_SEARCH:

        results = []

        for result in keyword_results[:limit]:

            results.append({

                "filename": result["filename"],

                "keyword_score": round(
                    result["score"],
                    3
                ),

                "semantic_score": 0.0,

                "hybrid_score": round(
                    result["score"],
                    3
                )

            })

        return results

    # -----------------------------------
    # SEMANTIC SEARCH
    # -----------------------------------

    semantic_results = (
        semantic_search.semantic_search(
            query,
            limit=len(
                search_engine.document_files
            )
        )
    )

    # -----------------------------------
    # CREATE SCORE DICTIONARIES
    # -----------------------------------

    keyword_scores = {}

    for result in keyword_results:

        keyword_scores[
            result["filename"]
        ] = result["score"]

    semantic_scores = {}

    for result in semantic_results:

        semantic_scores[
            result["filename"]
        ] = result["similarity"]

    # -----------------------------------
    # NORMALIZE KEYWORD SCORES
    # -----------------------------------

    if keyword_scores:

        min_keyword = min(
            keyword_scores.values()
        )

        max_keyword = max(
            keyword_scores.values()
        )

    else:

        min_keyword = 0
        max_keyword = 0

    normalized_keyword_scores = {}

    for filename, score in keyword_scores.items():

        normalized_keyword_scores[
            filename
        ] = normalize_score(
            score,
            min_keyword,
            max_keyword
        )

    # -----------------------------------
    # NORMALIZE SEMANTIC SCORES
    # -----------------------------------

    if semantic_scores:

        min_semantic = min(
            semantic_scores.values()
        )

        max_semantic = max(
            semantic_scores.values()
        )

    else:

        min_semantic = 0
        max_semantic = 0

    normalized_semantic_scores = {}

    for filename, score in semantic_scores.items():

        normalized_semantic_scores[
            filename
        ] = normalize_score(
            score,
            min_semantic,
            max_semantic
        )

    # -----------------------------------
    # COMBINE ALL DOCUMENTS
    # -----------------------------------

    all_documents = (
        set(keyword_scores.keys())
        |
        set(semantic_scores.keys())
    )

    # -----------------------------------
    # CALCULATE HYBRID SCORE
    # -----------------------------------

    results = []

    for filename in all_documents:

        keyword_score = (
            normalized_keyword_scores.get(
                filename,
                0.0
            )
        )

        semantic_score = (
            normalized_semantic_scores.get(
                filename,
                0.0
            )
        )

        hybrid_score = (
            keyword_weight * keyword_score
            +
            semantic_weight * semantic_score
        )

        results.append({

            "filename": filename,

            "keyword_score": round(
                keyword_score,
                3
            ),

            "semantic_score": round(
                semantic_score,
                3
            ),

            "hybrid_score": round(
                hybrid_score,
                3
            )

        })

    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    # -----------------------------------
    # RETURN TOP RESULTS
    # -----------------------------------

    return results[:limit]


# ---------------------------------------
# TEST
# ---------------------------------------

if __name__ == "__main__":

    query = "machine learning"

    results = hybrid_search(query)

    print("\nHybrid Search Results")
    print("---------------------")

    for result in results:

        print(
            result["filename"],
            "| Keyword:",
            result["keyword_score"],
            "| Semantic:",
            result["semantic_score"],
            "| Hybrid:",
            result["hybrid_score"]
        )