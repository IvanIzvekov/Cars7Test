from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.employees import EmployeeItemCreate
from app.services.employees import EmployeeService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/create")
async def create_employee_router(
    request: EmployeeItemCreate,
    session: AsyncSession = Depends(get_session),
):
    service = EmployeeService(session)

    try:
        async with session.begin():
            employee_id = await service.create_employee(request)
        return {"status": "ok", "id": employee_id}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error creating employee")
        raise HTTPException(status_code=500, detail="Internal Server Error")
