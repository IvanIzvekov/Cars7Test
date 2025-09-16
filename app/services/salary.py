from collections import defaultdict
from datetime import datetime
from typing import List
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.statistics_repository import StatisticsRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.salary_repository import SalaryRepository
from app.schemas.statistics import StatisticsItemRead


class SalaryService:
    def __init__(self, session: AsyncSession):
        self.repo = SalaryRepository(session)
        self.stat_repo = StatisticsRepository(session)
        self.employee_repo = EmployeeRepository(session)

    async def calculate_prev_month_salary(self, operator_ids: List[int] = None):
        today = datetime.now()
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        start_at = datetime(prev_year, prev_month, 1)
        end_at = datetime(today.year, today.month, 1)
        return await self.calculate_monthly_salary(start_at, end_at, operator_ids)

    async def calculate_monthly_salary(
        self, start_at: datetime, end_at: datetime, operator_ids: List[int] = None
    ):
        # Получаем статистику и коэффициенты
        stats_model = StatisticsItemRead(
            start_date=start_at, end_date=end_at, operator_ids=operator_ids
        )
        stats = await self.stat_repo.get(stats_model)
        coeffs = await self.repo.get_coefficients()
        coeff_map = {c.id: c for c in coeffs}

        # Получаем сотрудников
        if operator_ids:
            employees = [await self.employee_repo.get_operator(op_id) for op_id in operator_ids]
        else:
            employees = await self.employee_repo.get_all_operators()
        salary_map = {e.id: Decimal(e.salary) for e in employees}

        # Агрегируем статистику по (оператор, параметр)
        grouped = defaultdict(list)
        for s in stats:
            grouped[(s.operator_id, s.parameter_id)].append(Decimal(s.value))

        # Удаляем старые записи
        if stats:
            await self.repo.delete_salary_calculation(start_at, end_at, operator_ids)

        # Рассчитываем зарплату
        for operator in employees:
            pos_sum = Decimal(0)
            neg_sum = Decimal(0)
            pos_weight = Decimal(0)
            neg_weight = Decimal(0)

            for (op_id, param_id), values in grouped.items():
                if op_id != operator.id:
                    continue
                avg_value = sum(values) / Decimal(len(values))
                coeff = coeff_map[param_id]
                weight = Decimal(coeff.weight)

                if coeff.norm != coeff.base:
                    base = Decimal(coeff.base)
                    norm = Decimal(coeff.norm)

                    if coeff.type == "positive":
                        coef = Decimal(1) if avg_value < base else Decimal(1) + (avg_value - base) / (norm - base)
                        coef = min(coef, Decimal(2))
                        pos_sum += coef * weight
                        pos_weight += weight

                    elif coeff.type == "negative":
                        coef = Decimal(1) if avg_value < base else Decimal(1) - (avg_value - base) / (norm - base)
                        coef = max(coef, Decimal(0))
                        neg_sum += coef * weight
                        neg_weight += weight

                    else:
                        coef = Decimal(1)
                else:
                    coef = Decimal(1)

                await self.repo.save_salary_calculation(
                    operator_id=operator.id,
                    parameter=str(param_id),
                    value=coef,
                    total=coef * weight,
                    salary_amount=None,
                    start_at=start_at,
                    end_at=end_at,
                )

            # Нормализуем по весу
            pos_total = pos_sum / pos_weight if pos_weight else Decimal(1)
            neg_total = neg_sum / neg_weight if neg_weight else Decimal(1)

            # Итоговый коэффициент
            total_coef = pos_total - (Decimal(1) - neg_total)
            total_coef = max(total_coef, Decimal(0))

            base_salary = salary_map.get(operator.id, Decimal(0))
            calculated_salary = base_salary * total_coef

            await self.repo.save_salary_calculation(
                operator_id=operator.id,
                parameter="TOTAL",
                value=total_coef,
                total=total_coef,
                salary_amount=calculated_salary,
                start_at=start_at,
                end_at=end_at,
            )

        return True
