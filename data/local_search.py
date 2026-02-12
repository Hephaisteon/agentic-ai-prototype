#########################
# PDF Similarity Search #
#########################

# Packages to create embeddings of PDF files, and store in FAISS vector
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Define embedding model to convert text to vectors
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Similarity threshold for only considering strong matches (lower value means higher semantic similarity)
similarity_threshold = 0.35

# Load pre-built FAISS vectorstores for all documentation domains.
vector_stores = {
    "installation": FAISS.load_local(
        "vectorstores/installation",
        embeddings,
        allow_dangerous_deserialization=True,
    ),
    "roles_rights": FAISS.load_local(
        "vectorstores/roles_rights",
        embeddings,
        allow_dangerous_deserialization=True,
    ),
    "user_manual": FAISS.load_local(
        "vectorstores/user_manual",
        embeddings,
        allow_dangerous_deserialization=True,
    ),
    "customization": FAISS.load_local(
        "vectorstores/customization",
        embeddings,
        allow_dangerous_deserialization=True,
    ),
}


def search_local_docs(query: str, k: int = 4) -> str:
    """
    Function to perform semantic search across all local vectorstores.

    The function retrieves the "k" most similar chunks per vectorstore,
    filters them using a similarity threshold, and returns the results including the source and the similiarity score.
    """

    results = []

    for name, store in vector_stores.items():

        # Perform similarity search
        docs = store.similarity_search_with_score(query, k=k)

        for doc, score in docs:

            # Filter results based on similarity threshold
            if score <= similarity_threshold:
                results.append(
                    f"[SOURCE: {name} | score={score:.3f}]\n{doc.page_content}"
                )

    # Return a single context string containing all results
    return "\n\n".join(results)

