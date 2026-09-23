from app.rag.retriever import retrieve_documents
from app.rag.llm import llm


RELEVANCE_THRESHOLD = 0.30


def is_casual_message(question: str) -> bool:

    casual_messages = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "hola",
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "bye",
        "goodbye",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how are you?",
        "who are you",
        "who are you?",
    }

    normalized_question = question.lower().strip()

    return normalized_question in casual_messages


def generate_answer(
    question: str,
    session_id: str
):

    # -----------------------------------------
    # 1. Handle casual conversation
    # -----------------------------------------

    if is_casual_message(question):

        prompt = f"""
You are a friendly AI support assistant.

The user is having a casual conversation with you.

Respond naturally, briefly, and politely.

Do not talk about document retrieval unless necessary.

User message:

{question}
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": []
        }


    # -----------------------------------------
    # 2. Retrieve document information
    # -----------------------------------------

    results = retrieve_documents(
        question=question,
        session_id=session_id,
        k=5
    )


    # -----------------------------------------
    # 3. Apply relevance threshold
    # -----------------------------------------

    relevant_documents = []

    for document, score in results:

        if score >= RELEVANCE_THRESHOLD:

            relevant_documents.append(
                (document, score)
            )


    # -----------------------------------------
    # 4. Nothing relevant found
    # -----------------------------------------

    if not relevant_documents:

        return {
            "answer": (
                "I couldn't find that information "
                "in the uploaded document."
            ),
            "sources": []
        }


    # -----------------------------------------
    # 5. Build context
    # -----------------------------------------

    context = "\n\n".join(

        document.page_content

        for document, score in relevant_documents

    )


    # -----------------------------------------
    # 6. Generate document-based answer
    # -----------------------------------------

    prompt = f"""
You are an AI support assistant.

The user is asking about the uploaded document.

Use the provided context to answer the question.

IMPORTANT RULES:

1. Use the document context for document-related questions.

2. Do not invent information.

3. Do not make up facts that are not supported
   by the context.

4. If the answer cannot be found in the context,
   say:

   "I couldn't find that information in the uploaded document."

5. Keep the answer natural and conversational.

Context:

{context}


User question:

{question}
"""


    response = llm.invoke(prompt)


    # -----------------------------------------
    # 7. Build sources
    # -----------------------------------------

    sources = []


    for document, score in relevant_documents:

        metadata = document.metadata


        source = {
            "filename": metadata.get(
                "filename",
                "Unknown"
            ),

            "page": metadata.get(
                "page",
                0
            )
        }


        if source not in sources:

            sources.append(source)


    return {
        "answer": response.content,
        "sources": sources
    }