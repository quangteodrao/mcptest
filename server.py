"""
Vi du MCP server nho nhat: 2 cong cu tai chinh, khong can API key.

Chay local (stdio, dung cho Claude Code / claude_desktop_config.json):
    python3 server.py

Chay remote (HTTP, dung cho custom connector tren claude.ai):
    python3 server.py --http
"""

import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("finance-demo")


@mcp.tool()
def compound_interest(
    principal: float,
    annual_rate_percent: float,
    years: float,
    compounds_per_year: int = 12,
) -> dict:
    """Tinh gia tri tuong lai cua mot khoan tien gui theo lai kep.

    Args:
        principal: So tien goc ban dau.
        annual_rate_percent: Lai suat nam, don vi phan tram (vi du 6 nghia la 6%).
        years: So nam gui.
        compounds_per_year: So lan ghep lai moi nam (12 = hang thang, 1 = hang nam).
    """
    r = annual_rate_percent / 100
    n = compounds_per_year
    t = years
    future_value = principal * (1 + r / n) ** (n * t)
    interest_earned = future_value - principal
    return {
        "principal": round(principal, 2),
        "future_value": round(future_value, 2),
        "interest_earned": round(interest_earned, 2),
        "years": years,
        "annual_rate_percent": annual_rate_percent,
        "compounds_per_year": compounds_per_year,
    }


@mcp.tool()
def loan_monthly_payment(
    loan_amount: float,
    annual_rate_percent: float,
    term_years: float,
) -> dict:
    """Tinh so tien phai tra moi thang cho mot khoan vay tra gop deu.

    Args:
        loan_amount: So tien vay.
        annual_rate_percent: Lai suat nam, don vi phan tram (vi du 9.5 nghia la 9.5%).
        term_years: Thoi han vay, tinh bang nam.
    """
    monthly_rate = annual_rate_percent / 100 / 12
    n_payments = int(round(term_years * 12))

    if monthly_rate == 0:
        monthly_payment = loan_amount / n_payments
    else:
        monthly_payment = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** n_payments
            / ((1 + monthly_rate) ** n_payments - 1)
        )

    total_paid = monthly_payment * n_payments
    total_interest = total_paid - loan_amount

    return {
        "loan_amount": round(loan_amount, 2),
        "monthly_payment": round(monthly_payment, 2),
        "number_of_payments": n_payments,
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_interest, 2),
        "annual_rate_percent": annual_rate_percent,
        "term_years": term_years,
    }


if __name__ == "__main__":
    if "--http" in sys.argv:
        # Streamable HTTP, dung khi deploy len internet de lam remote MCP server
        mcp.settings.host = "0.0.0.0"
        mcp.settings.port = 8000
        mcp.run(transport="streamable-http")
    else:
        # stdio, dung khi chay local tren may (Claude Desktop / Claude Code)
        mcp.run(transport="stdio")
