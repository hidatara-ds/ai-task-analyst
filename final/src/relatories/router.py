import csv
from datetime import date
from io import StringIO
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from relatories.schemas import Chat, ExportRequest, Workspace
from relatories.service import get_workspace_chats, get_workspaces

router = APIRouter(tags=["relatories generation"], prefix="/relatories")


# TODO : make parameters optional and perhaps use kwargs
@router.get("/export/chats")
async def export_workspace_chats(
    workspace: Optional[str],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    only_leads: bool = False,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """
    Get chats from a specific period and workspace and export to CSV
    """
    try:
        filters = ExportRequest(
            workspace=workspace,
            start_date=start_date,
            end_date=end_date,
            only_leads=only_leads,
        )
        chats: list[Chat] = await get_workspace_chats(
            filters,
            db,
        )
    except Exception as e:
        print(f"Error while performing query : {e}")
        return StreamingResponse(
            StringIO("Error while performing query"), media_type="text/plain"
        )

    # create the csv with the content returned by service
    if chats:
        output = StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(
            [
                "session_id",
                "createdAt",
                "name",
                "email",
                "prompt",
                "response",
                "workspace_name",
                "workspace_id",
            ]
        )
        for chat in chats:
            writer.writerow(
                [
                    chat.session_id,
                    chat.created_at_local,
                    chat.name,
                    chat.email,
                    chat.prompt,
                    chat.response,
                    chat.workspace_name,
                    chat.workspace_id,
                ]
            )

        output.seek(0)
        response = StreamingResponse(output, media_type="text/csv")
        response.headers["Content-Disposition"] = (
            f"attachment; filename=workspace_chats{'_' + filters.workspace if filters.workspace else ''}_{date.today()}.csv"
        )
        return response
    else:
        return StreamingResponse(
            StringIO("No chats found for the given period and workspace"),
            media_type="text/plain",
        )


@router.get("/chats")
async def get_chats_json(
    workspace: Optional[str],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    only_leads: bool = False,
    db: AsyncSession = Depends(get_db),
) -> dict[str, list[Chat]]:
    """
    Get all chats
    """
    try:
        filters = ExportRequest(
            workspace=workspace,
            start_date=start_date,
            end_date=end_date,
            only_leads=only_leads,
        )
        chats: list[Chat] = await get_workspace_chats(
            filters,
            db,
        )
        return {"data": chats}
    except Exception as e:
        print(f"Error while performing query : {e}")
        return {"data": []}


@router.get("/workspaces")
async def get_workspaces_names(
    db: AsyncSession = Depends(get_db),
) -> list[Workspace]:
    """
    Get all workspaces names
    """
    workspaces_data = None
    try:
        workspaces_data = await get_workspaces(db)
    except Exception as e:
        print(f"Error while performing query : {e}")
    if workspaces_data:
        workspaces: list[Workspace] = [
            Workspace(**workspace) for workspace in workspaces_data
        ]
        return workspaces
    else:
        return []
