import json
import sys
import time
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
# F1@K
# ---------------------------------------

def f1_at_k(
    precision,
    recall
):

    if precision + recall == 0:
        return 0.0

    return (
        2
        * precision
        * recall
        / (precision + recall)
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
# GET KEYWORD RESULTS
# ---------------------------------------

def get_keyword_results(query):

    results = search_engine.search_results(
        query
    )

    return [
        result["filename"]
        for result in results
    ]


# ---------------------------------------
# GET SEMANTIC RESULTS
# ---------------------------------------

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


# ---------------------------------------
# GET HYBRID RESULTS
# ---------------------------------------

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
    f1_scores = []
    reciprocal_ranks = []
    search_times = []

    query_results = []

    print()
    print("=" * 70)
    print(method_name)
    print("=" * 70)

    for item in evaluation_data:

        query = item["query"]

        relevant_documents = set(
            item["relevant_documents"]
        )

        start_time = time.perf_counter()

        retrieved_documents = (
            search_function(query)
        )

        end_time = time.perf_counter()

        search_time = (
            end_time - start_time
        ) * 1000

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

        f1 = f1_at_k(
            precision,
            recall
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

        f1_scores.append(
            f1
        )

        reciprocal_ranks.append(
            rr
        )

        search_times.append(
            search_time
        )

        query_results.append(
            {
                "query": query,
                "retrieved_documents":
                    retrieved_documents[:5],
                "relevant_documents":
                    list(relevant_documents),
                "precision@5":
                    round(precision, 4),
                "recall@5":
                    round(recall, 4),
                "f1@5":
                    round(f1, 4),
                "reciprocal_rank":
                    round(rr, 4),
                "search_time_ms":
                    round(search_time, 3)
            }
        )

        print()
        print(
            f"Query: {query}"
        )

        print(
            f"Top 5: "
            f"{retrieved_documents[:5]}"
        )

        print(
            f"Precision@5: "
            f"{precision:.3f}"
        )

        print(
            f"Recall@5: "
            f"{recall:.3f}"
        )

        print(
            f"F1@5: "
            f"{f1:.3f}"
        )

        print(
            f"Reciprocal Rank: "
            f"{rr:.3f}"
        )

        print(
            f"Search Time: "
            f"{search_time:.3f} ms"
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

    mean_f1 = (
        sum(f1_scores)
        / len(f1_scores)
    )

    mean_reciprocal_rank = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
    )

    mean_search_time = (
        sum(search_times)
        / len(search_times)
    )

    print()
    print("-" * 70)
    print("AVERAGE RESULTS")
    print("-" * 70)

    print(
        f"Precision@5 : "
        f"{mean_precision:.3f}"
    )

    print(
        f"Recall@5    : "
        f"{mean_recall:.3f}"
    )

    print(
        f"F1@5        : "
        f"{mean_f1:.3f}"
    )

    print(
        f"MRR         : "
        f"{mean_reciprocal_rank:.3f}"
    )

    print(
        f"Avg Time    : "
        f"{mean_search_time:.3f} ms"
    )

    return {
        "precision@5": mean_precision,
        "recall@5": mean_recall,
        "f1@5": mean_f1,
        "mrr": mean_reciprocal_rank,
        "average_search_time_ms":
            mean_search_time,
        "queries": query_results
    }


# ---------------------------------------
# SAVE RESULTS
# ---------------------------------------

def save_results(results):

    output_file = (
        Path(__file__).resolve().parent
        / "results.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print()
    print(
        f"Evaluation results saved to: "
        f"{output_file}"
    )


# ---------------------------------------
# MAIN EVALUATION
# ---------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("MINI SEARCH ENGINE EVALUATION")
    print("=" * 70)

    print(
        f"\nEvaluation queries: "
        f"{len(evaluation_data)}"
    )

    print(
        f"Documents available: "
        f"{len(search_engine.document_files)}"
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

    comparison = {
        "TF-IDF": {
            "precision@5":
                keyword_metrics["precision@5"],
            "recall@5":
                keyword_metrics["recall@5"],
            "f1@5":
                keyword_metrics["f1@5"],
            "mrr":
                keyword_metrics["mrr"],
            "average_search_time_ms":
                keyword_metrics[
                    "average_search_time_ms"
                ]
        },

        "Semantic": {
            "precision@5":
                semantic_metrics["precision@5"],
            "recall@5":
                semantic_metrics["recall@5"],
            "f1@5":
                semantic_metrics["f1@5"],
            "mrr":
                semantic_metrics["mrr"],
            "average_search_time_ms":
                semantic_metrics[
                    "average_search_time_ms"
                ]
        },

        "Hybrid": {
            "precision@5":
                hybrid_metrics["precision@5"],
            "recall@5":
                hybrid_metrics["recall@5"],
            "f1@5":
                hybrid_metrics["f1@5"],
            "mrr":
                hybrid_metrics["mrr"],
            "average_search_time_ms":
                hybrid_metrics[
                    "average_search_time_ms"
                ]
        }
    }

    print()
    print()
    print("=" * 80)
    print("FINAL COMPARISON")
    print("=" * 80)

    print(
        "\nMethod        "
        "Precision@5   "
        "Recall@5   "
        "F1@5      "
        "MRR       "
        "Avg Time (ms)"
    )

    print("-" * 80)

    for method, metrics in comparison.items():

        print(
            f"{method:<13}"
            f"{metrics['precision@5']:<14.3f}"
            f"{metrics['recall@5']:<11.3f}"
            f"{metrics['f1@5']:<10.3f}"
            f"{metrics['mrr']:<10.3f}"
            f"{metrics['average_search_time_ms']:.3f}"
        )

    # ---------------------------------------
    # SAVE EVERYTHING
    # ---------------------------------------

    results = {
        "evaluation_queries":
            len(evaluation_data),

        "documents":
            len(search_engine.document_files),

        "metrics": comparison
    }

    save_results(results)

    print()
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)