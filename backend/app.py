import logging
import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import the new modules
from database import execute_query
from llm_client import get_sql_query
from data_formatter import format_answer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the SQL Query Generator Backend."}

@app.post("/generate_sql")
async def generate_sql_response(request: QueryRequest):
    logger.info(f"Received request with query: '{request.question}'")
    
    try:
        # Step 1: Get SQL from the LLM service (using a dedicated function)
        sql_query = await get_sql_query(request.question)
        if not sql_query:
            raise HTTPException(status_code=500, detail="LLM did not return a valid SQL query.")

        logger.info(f"Generated SQL: '{sql_query}'")

        # Step 2: Execute the SQL query (using a dedicated function)
        query_results = execute_query(sql_query)
        logger.info(f"Query results: {query_results}")

        # Step 3: Format the answer for the user
        final_answer = format_answer(request.question, query_results)

        return {"answer": final_answer}

    except HTTPException:
        raise  # Re-raise explicit HTTP exceptions
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)