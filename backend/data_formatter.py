def format_answer(question, raw_results):
    """
    Converts raw query results into a natural language sentence.
    This is a simplified example. A real-world version would be more complex.
    """
    if not raw_results:
        return "I could not find a result for your query."

    # Assumes a single result from a count or max query
    if isinstance(raw_results[0][0], int):
        result_value = raw_results[0][0]
        # Basic formatting logic based on the question
        if "total number of matches" in question.lower():
            return f"The total number of matches played is {result_value}."
        elif "largest win" in question.lower():
            return f"The largest win by wickets was {result_value}."
        else:
            return f"The answer is {result_value}."
    
    # Handle string results (e.g., venue names)
    elif isinstance(raw_results[0][0], str):
        result_value = raw_results[0][0]
        return f"The answer to your question is: {result_value}."
    
    return f"The answer is: {raw_results[0]}."