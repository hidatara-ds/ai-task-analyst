from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ai_helper.schemas import GeneratedQuery
from config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_KEY)


async def execute_query(query: str, db: AsyncSession) -> list[dict]:
    """
    Execute query in the database
    """
    sql_query = text(query)
    result = await db.execute(sql_query)
    result_rows = result.fetchall()
    # save the result in a dictionary and ask llm to coment about it
    data = {}
    data["result"] = [dict(row._mapping) for row in result_rows]

    return [dict(row._mapping) for row in result_rows]


async def analise_results(results: list[dict], prompt: str) -> str:
    """
    Analise the results and return a comment
    """
    ai_response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are a BI analyst and need to take insights based on some chunk of data and a user question.
                You should analyze the data and generate a comment that can be useful for the user based on what he asked for.
                The comment should be concise and direct.
                Your response should only have the comment, no other text.
             """,
            },
            {
                "role": "user",
                "content": f"""
                user_question: {prompt},
                data: {results}
             """,
            },
        ],
    )
    if ai_response.choices[0].message.content:
        return ai_response.choices[0].message.content
    return "No insights for this query results"


async def generate_query(
    prompt: str, workspace: str | None = None
) -> str | None:
    """
    Get answer from AI model to generate optimized SQL queries
    """
    workspace_context = (
        f" for workspace '{workspace}'"
        if workspace
        else " across all workspaces"
    )
    full_prompt = f"{prompt}{workspace_context}"

    messages = [
        {
            "role": "system",
            "content": """
You are an expert SQL developer specializing in PostgreSQL query optimization. Your task is to help retrieve the right data to answer user questions.

Follow these steps when analyzing each request:

1. First, identify what kind of data we need to answer the question:
   - Is it a direct data retrieval (e.g., "show me latest chats")?
   - Or does it require analysis of the data content (e.g., "what are common complaints")?

2. For direct data queries:
   - Generate the exact SQL query requested
   - Use proper filtering and sorting

3. For analytical questions:
   - Return the relevant base data that would help analyze the question
   - Don't try to analyze the content in SQL - that's better done later
   - Focus on getting complete, relevant records

### Database Schema:

embed_users (collected leads - user information)
- session_id (PK)
- name: user's full name
- email: user's email
- created_at: session creation timestamp

embed_chats (chat interactions)  
- id (PK)
- prompt: user's input text
- response: system response
- session_id (FK -> embed_users)
- embed_id (FK -> embed_configs) 
- "createdAt": chat timestamp

embed_configs (configuration)
- id (PK)
- workspace_id (FK -> workspaces)
- "createdAt": config timestamp

workspaces (workspace information)
- id (PK)
- name: workspace name
- slug: URL-friendly identifier
- "createdAt": creation timestamp
- "lastUpdatedAt": last modified

### SQL Style Guide:
- Use meaningful table aliases
- Quote column names with double quotes
- Include explicit JOIN conditions
- Order by timestamp DESC for freshest data
- Add LIMIT clauses for large results
- Include WHERE clauses as needed

### Response Format:
{
  "query": "<SQL query>",
  "confidence": <float 0-1>
}

If unclear requirements:
{
  "query": "Not enough information",
  "confidence": 0.0
}

### Examples:

Direct data request:
User: "Show me recent chats"
{
  "query": "SELECT c.id, u.name, c.prompt, c.response, c."createdAt" FROM embed_chats c JOIN embed_users u ON c.session_id = u.session_id ORDER BY c."createdAt" DESC LIMIT 100",
  "confidence": 0.9
}

Analytical request:
User: "What are users complaining about most?"
{
  "query": "SELECT u.name, c.prompt, c.response, c."createdAt" FROM embed_chats c JOIN embed_users u ON c.session_id = u.session_id ORDER BY c."createdAt" DESC LIMIT 300",
  "confidence": 0.8
}
""",
        },
        {"role": "user", "content": full_prompt},
    ]

    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,  # type: ignore
        response_format=GeneratedQuery,
        temperature=0.1,  # Lower temperature for more focused outputs
    )

    return response.choices[0].message.content
