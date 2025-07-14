def format_doc(document):
    formatted = []
    for doc in document:
        formatted.append(doc.page_content)
    return "\n\n".join(formatted)