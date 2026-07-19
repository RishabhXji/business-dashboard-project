from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class KPICard(BaseModel):
    total_revenue: float
    total_profit: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    profit_margin: float
    inventory_turnover: Optional[float]

class ChartPoint(BaseModel):
    date: date
    value: float

class DashboardResponse(BaseModel):
    kpis: KPICard
    monthly_sales: List[Dict[str, Any]]
    revenue_by_category: List[Dict[str, Any]]
    revenue_by_region: List[Dict[str, Any]]
    top_products: List[Dict[str, Any]]
    bottom_products: List[Dict[str, Any]]
