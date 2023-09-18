# Python FastAPI models using Pydantic for the "Functionality for Month and Annual Report for One Person Limited Companies"
from pydantic import BaseModel

class ReportData(BaseModel):
    report_id: int
    company_name: str
    report_type: str
    report_year: int
    report_month: int
    income_statement: IncomeStatement
    balance_sheet: BalanceSheet
    cash_flow_statement: CashFlowStatement
    tax_report: TaxReport

class IncomeStatement(BaseModel):
    revenue: float
    expenses: float
    net_income: float

class BalanceSheet(BaseModel):
    assets: float
    liabilities: float
    equity: float

class CashFlowStatement(BaseModel):
    operating_cash_flow: float
    investing_cash_flow: float
    financing_cash_flow: float
    net_cash_flow: float

class TaxReport(BaseModel):
    tax_expenses: float
    tax_liabilities: float
    tax_paid: float
