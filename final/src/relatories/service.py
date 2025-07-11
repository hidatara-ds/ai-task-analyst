from sqlalchemy import TextClause, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from relatories.models import Workspaces
from relatories.schemas import Chat, ExportRequest


async def get_workspace_chats(
    filters: ExportRequest,
    db: AsyncSession,
) -> list[Chat]:
    """
    Get chats from a specific period and workspace
    """

    start_filter = (
        f"c.\"createdAt\" >= '{filters.start_date}'"
        if filters.start_date
        else ""
    )
    end_filter = (
        f"c.\"createdAt\" <= '{filters.end_date}'" if filters.end_date else ""
    )

    # generating the query based on the filters
    query: TextClause = text(
        f"""
        SELECT
            c.session_id,
            u.created_at at time zone 'utc' at time zone 'BRT' as created_at_local,
            u.name,
            u.email,
            c.prompt,
            (c.response::jsonb) -> 'text' AS response,
            ws.name as workspace_name,
            ws.id as workspace_id
        FROM embed_chats c
            {"inner" if filters.only_leads else "left"} join embed_users u on u.session_id = c.session_id
            left join embed_configs conf on conf.id = c.embed_id
            left join workspaces ws on ws.id = conf.workspace_id
        WHERE ws.name = '{filters.workspace}'
        {"AND " + start_filter if start_filter else ""} 
        {"AND " + end_filter if end_filter else ""}
        ORDER BY c."createdAt";
        """
    )

    print(query)

    result = await db.execute(query)
    result_rows = result.fetchall()

    chats: list[Chat] = [Chat(**row._mapping) for row in result_rows]

    return chats


# async def get_workspace_leads(db: AsyncSession, workspace: str):
#     """
#     Get leads from a specific workspace
#     """
#     query = text(f"""
#     SELECT
#         c.session_id,
#         u.created_at at time zone 'utc' at time zone 'BRT' as created_at_local,
#         u.name,
#         u.email,
#         c.prompt,
#         (c.response::jsonb) -> 'text' AS response,
#         ws.name as workspace_name
#     FROM embed_chats c
#         inner join embed_users u on u.session_id = c.session_id
#         left join embed_configs conf on conf.id = c.embed_id
#         left join workspaces ws on ws.id = conf.workspace_id
#     WHERE ws.name = '{workspace}'
#     ORDER BY u.email;""")

#     result = await db.execute(query)
#     leads = result.fetchall()
#     return leads


async def get_workspaces(db: AsyncSession) -> list[dict]:
    """
    Get all workspaces
    """
    query = select(Workspaces.id, Workspaces.name)
    result = await db.execute(query)
    workspaces = result.fetchall()
    return [row._asdict() for row in workspaces]
