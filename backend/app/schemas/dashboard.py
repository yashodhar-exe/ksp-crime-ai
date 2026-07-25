from typing import Optional
from pydantic import BaseModel

from app.schemas.audit import AuditLogOut
from app.schemas.case import CaseOut


class DashboardSummaryOut(BaseModel):
    total_cases: int
    open_cases: int
    critical_cases: int
    total_citizens: int
    total_officers: int
    district: Optional[str]  # None = viewing all districts (admin/SP)


class BreakdownPoint(BaseModel):
    label: str
    count: int


class DashboardStatsOut(BaseModel):
    by_status: list[BreakdownPoint]
    by_crime_type: list[BreakdownPoint]


class DashboardRecentOut(BaseModel):
    cases: list[CaseOut]


class DashboardActivityOut(BaseModel):
    entries: list[AuditLogOut]
