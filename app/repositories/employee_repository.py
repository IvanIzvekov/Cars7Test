from app.schemas.employees import EmployeeItemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
import logging

logger = logging.getLogger(__name__)


class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_operator(self, operator_id: int) -> Employee:
        """Получить сотрудника по ID"""
        operator = await self.session.get(Employee, operator_id)
        return operator

    async def create_new_employee_in_db(self, employee: EmployeeItemCreate) -> int:
        """Создать нового сотрудника и вернуть его ID"""
        new_employee = Employee(
            last_name=employee.last_name,
            first_name=employee.first_name,
            second_name=employee.second_name,
            position=employee.position,
            status=employee.status,
        )
        self.session.add(new_employee)
        await self.session.flush()
        return new_employee.id


    async def update_employee_status(self, operator_id: int, new_status: str) -> None:
        """Обновить статус сотрудника"""
        employee = await self.session.get(Employee, operator_id)
        if not employee:
            raise ValueError(f"Employee with id {operator_id} not found")

        employee.status = new_status
        await self.session.flush()
