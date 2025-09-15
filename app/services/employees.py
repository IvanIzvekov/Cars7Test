from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employees import EmployeeItemCreate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.employee_repository = EmployeeRepository(session)

    async def create_employee(self, employee: EmployeeItemCreate) -> int:
        """ Сервис создания нового сотрудника """
        try:
            employee_id = await self.employee_repository.create_new_employee_in_db(employee)
            return employee_id

        except ValueError as e:
            logger.warning(f"Validation error in EmployeeService: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in EmployeeService: {e}")
            raise
