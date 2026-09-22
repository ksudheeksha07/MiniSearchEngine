from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import time
import os

import search_engine
import semantic_search
import hybrid_search


app = Flask(__name__)

search_history = []

ENABLE_SEMANTIC_SEARCH = (
    os.environ.get(
        "ENABLE_SEMANTIC_SEARCH",
        "true"
    ).lower()
    == "true"
)


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    semantic_results = []
    hybrid_results = []

    query = ""
    suggestion = None

    search_time = None
    documents_searched = 0
    query_terms = 0

    if request.method == "POST":
        query = request.form.get("query", "").strip()

    else:
        query = request.args.get("query", "").strip()

    if query:

        documents_searched = len(
            search_engine.document_files
        )

        query_terms = len(
            search_engine.clean_text(query)
        )

        start_time = time.perf_counter()

        # -------------------------------
        # KEYWORD SEARCH
        # -------------------------------

        results = search_engine.search_results(
            query
        )

        # -------------------------------
        # SEMANTIC + HYBRID SEARCH
        # -------------------------------

        if ENABLE_SEMANTIC_SEARCH:

            semantic_results = (
                semantic_search.semantic_search(
                    query
                )
            )

            hybrid_results = (
                hybrid_search.hybrid_search(
                    query
                )
            )

        else:

            semantic_results = []

            hybrid_results = (
                hybrid_search.hybrid_search(
                    query
                )
            )

        # -------------------------------
        # SEARCH TIME
        # -------------------------------

        end_time = time.perf_counter()

        search_time = round(
            (end_time - start_time) * 1000,
            3
        )

        # -------------------------------
        # SEARCH HISTORY
        # -------------------------------

        if query not in search_history:

            search_history.append(query)

        # -------------------------------
        # SPELLING SUGGESTION
        # -------------------------------

        if (
            not results
            and len(query.split()) == 1
        ):

            suggestion = (
                search_engine
                .get_spelling_suggestion(query)
            )

    return render_template(
        "index.html",
        query=query,
        results=results,
        semantic_results=semantic_results,
        hybrid_results=hybrid_results,
        suggestion=suggestion,
        history=search_history,
        search_time=search_time,
        documents_searched=documents_searched,
        query_terms=query_terms
    )


@app.route("/suggest")
def suggest():

    prefix = request.args.get(
        "q",
        ""
    )

    suggestions = (
        search_engine
        .get_suggestions(prefix)
    )

    return {
        "suggestions": suggestions
    }


@app.route("/document/<filename>")
def open_document(filename):

    return send_from_directory(
        search_engine.documents_folder,
        filename
    )


@app.route("/clear-history")
def clear_history():

    search_history.clear()

    return redirect(
        url_for("home")
    )


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )