import json
import sys
from pathlib import Path

# Allow Python to import files from the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import search_engine
import semantic_search
import hybrid_search


# ---------------------------------------
# LOAD EVALUATION DATASET
# ---------------------------------------

evaluation_file = (
    Path(__file__).resolve().parent
    / "queries.json"
)

with open(
    evaluation_file,
    "r",
    encoding="utf-8"
) as file:

    evaluation_data = json.load(file)


# ---------------------------------------
# PRECISION@K
# ---------------------------------------

def precision_at_k(
    retrieved_documents,
    relevant_documents,
    k
):

    retrieved = retrieved_documents[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1
        for document in retrieved
        if document in relevant_documents
    )

    return relevant_count / len(retrieved)


# ---------------------------------------
# RECALL@K
# ---------------------------------------

def recall_at_k(
    retrieved_documents,
    relevant_documents,
    k
):

    if not relevant_documents:
        return 0.0

    retrieved = retrieved_documents[:k]

    relevant_count = sum(
        1
        for document in retrieved
        if document in relevant_documents
    )

    return relevant_count / len(
        relevant_documents
    )


# ---------------------------------------
# RECIPROCAL RANK
# ---------------------------------------

def reciprocal_rank(
    retrieved_documents,
    relevant_documents
):

    for rank, document in enumerate(
        retrieved_documents,
        start=1
    ):

        if document in relevant_documents:

            return 1 / rank

    return 0.0


# ---------------------------------------
# GET DOCUMENT NAMES
# ---------------------------------------

def get_keyword_results(query):

    results = search_engine.search_results(
        query
    )

    return [
        result["filename"]
        for result in results
    ]


def get_semantic_results(query):

    results = semantic_search.semantic_search(
        query,
        limit=len(
            search_engine.document_files
        )
    )

    return [
        result["filename"]
        for result in results
    ]


def get_hybrid_results(query):

    results = hybrid_search.hybrid_search(
        query,
        limit=len(
            search_engine.document_files
        )
    )

    return [
        result["filename"]
        for result in results
    ]


# ---------------------------------------
# EVALUATE ONE SEARCH METHOD
# ---------------------------------------

def evaluate_method(
    method_name,
    search_function
):

    precision_scores = []
    recall_scores = []
    reciprocal_ranks = []

    print()
    print("=" * 60)
    print(method_name)
    print("=" * 60)

    for item in evaluation_data:

        query = item["query"]

        relevant_documents = set(
            item["relevant_documents"]
        )

        retrieved_documents = (
            search_function(query)
        )

        precision = precision_at_k(
            retrieved_documents,
            relevant_documents,
            5
        )

        recall = recall_at_k(
            retrieved_documents,
            relevant_documents,
            5
        )

        rr = reciprocal_rank(
            retrieved_documents,
            relevant_documents
        )

        precision_scores.append(
            precision
        )

        recall_scores.append(
            recall
        )

        reciprocal_ranks.append(
            rr
        )

        print(
            f"\nQuery: {query}"
        )

        print(
            f"Top 5: {retrieved_documents[:5]}"
        )

        print(
            f"Precision@5: {precision:.3f}"
        )

        print(
            f"Recall@5: {recall:.3f}"
        )

        print(
            f"Reciprocal Rank: {rr:.3f}"
        )

    # ---------------------------------------
    # AVERAGES
    # ---------------------------------------

    mean_precision = (
        sum(precision_scores)
        / len(precision_scores)
    )

    mean_recall = (
        sum(recall_scores)
        / len(recall_scores)
    )

    mean_reciprocal_rank = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
    )

    print()
    print("-" * 60)
    print("AVERAGE RESULTS")
    print("-" * 60)

    print(
        f"Precision@5 : {mean_precision:.3f}"
    )

    print(
        f"Recall@5    : {mean_recall:.3f}"
    )

    print(
        f"MRR         : {mean_reciprocal_rank:.3f}"
    )

    return {
        "precision@5": mean_precision,
        "recall@5": mean_recall,
        "mrr": mean_reciprocal_rank
    }


# ---------------------------------------
# MAIN EVALUATION
# ---------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("MINI SEARCH ENGINE EVALUATION")
    print("=" * 60)

    print(
        f"\nEvaluation queries: "
        f"{len(evaluation_data)}"
    )

    # ---------------------------------------
    # TF-IDF
    # ---------------------------------------

    keyword_metrics = evaluate_method(
        "TF-IDF / KEYWORD SEARCH",
        get_keyword_results
    )

    # ---------------------------------------
    # SEMANTIC
    # ---------------------------------------

    semantic_metrics = evaluate_method(
        "SEMANTIC SEARCH",
        get_semantic_results
    )

    # ---------------------------------------
    # HYBRID
    # ---------------------------------------

    hybrid_metrics = evaluate_method(
        "HYBRID SEARCH",
        get_hybrid_results
    )

    # ---------------------------------------
    # FINAL COMPARISON
    # ---------------------------------------

    print()
    print()
    print("=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)

    print(
        "\nMethod              Precision@5   Recall@5   MRR"
    )

    print("-" * 60)

    print(
        f"TF-IDF              "
        f"{keyword_metrics['precision@5']:.3f}          "
        f"{keyword_metrics['recall@5']:.3f}       "
        f"{keyword_metrics['mrr']:.3f}"
    )

    print(
        f"Semantic             "
        f"{semantic_metrics['precision@5']:.3f}          "
        f"{semantic_metrics['recall@5']:.3f}       "
        f"{semantic_metrics['mrr']:.3f}"
    )

    print(
        f"Hybrid               "
        f"{hybrid_metrics['precision@5']:.3f}          "
        f"{hybrid_metrics['recall@5']:.3f}       "
        f"{hybrid_metrics['mrr']:.3f}"
    )

    print()
    print("=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)