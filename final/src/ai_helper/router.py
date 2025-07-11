import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ai_helper.schemas import QueryPrompt
from ai_helper.service import analise_results, execute_query, generate_query
from db import get_db

router = APIRouter(tags=["AI query generator"], prefix="/helper")


@router.post("/smart_query")
async def get_insights_with_ai(
    prompt: QueryPrompt, db: AsyncSession = Depends(get_db)
):
    """
    Say what you want and get the data without needing to chose the filters
    """
    try:
        response = await generate_query(prompt.prompt, prompt.workspace)
        response_json = json.loads(str(response))
        if response_json["query"] == "Not enough information":
            return {"error": "Not enough information to generate the query"}
    except Exception as e:
        print(f"Error while generating query : {e}")
        return {"error": "An error occurred while generating the query"}

    try:
        result = await execute_query(response_json["query"], db)
    except Exception as e:
        print(f"Error while executing query : {e}")
        return {"error": "An error occurred while executing the query"}

    try:
        if result:
            ai_insight: str = await analise_results(result[:300], prompt.prompt)
            return {
                "query": response_json["query"],
                "insights": ai_insight,
                "confidence": response_json["confidence"],
                "result": result,
            }
        return {
            "query": response_json["query"],
            "confidence": response_json["confidence"],
            "result": result,
            "insights": "No insights for this query results",
        }
    except Exception as e:
        print(f"Error while generating insights : {e}")
        return {
            "query": response_json["query"],
            "confidence": response_json["confidence"],
            "result": result,
            "insights": "No insights for this query results",
        }
