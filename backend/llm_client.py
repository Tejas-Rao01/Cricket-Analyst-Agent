import requests
import time
import logging

logger = logging.getLogger(__name__)

LLM_SERVER_URL = "http://localhost:8000/generate"


def get_prompt(question):

    return f"""
You have a table named 'matches' with the following schema:
- match_id TEXT PRIMARY KEY
- date TEXT
- venue TEXT
- gender TEXT
- match_type TEXT
- winner TEXT
- winner_by_wickets INTEGER

a table named 'innings' with the following schema:
- inning_id INTEGER PRIMARY KEY
- match_id TEXT
- team TEXT
- inning_number INTEGER
- FOREIGN KEY(match_id) REFERENCES matches(match_id)

and a tbale named deliveries with the following schema:
- delivery_id INTEGER PRIMARY KEY AUTOINCREMENT
- inning_id INTEGER
- over_num INTEGER
- ball_num INTEGER
- batsman TEXT
- bowler TEXT
- runs_scored INTEGER
- extras INTEGER
- is_wicket INTEGER
- FOREIGN KEY(inning_id) REFERENCES innings(inning_id)

Given the following natural language query:
"{question}"



Return only the SQL query that answers the question. Do not include any additional text, markdown, or explanations. delimit your response with ````
"""
    
    

def get_sql_query(question):
    """Sends a prompt to the LLM service and returns a cleaned SQL query."""
    llm_prompt = get_prompt(question)
    
    logger.info("Sending SQL generation request to the LLM")
    query_start = time.time()
    
    try:
        llm_response = requests.post(
            LLM_SERVER_URL, 
            json={"prompt": llm_prompt, "max_new_tokens": 100}
        )
        llm_response.raise_for_status()
        
        generated_text = llm_response.json().get("generated_text", "")
        # Clean the generated text to extract just the SQL
        sql_query = generated_text.strip().replace("```sql", "").replace("```", "").strip()
        
        query_end = time.time()
        logger.info(f"LLM request elapsed time: {query_end - query_start:.2f}s")
        
        return sql_query

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to LLM server: {e}", exc_info=True)
        return None