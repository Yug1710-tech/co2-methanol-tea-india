"""
Techno-economic analysis: factorial cost estimation and profitability metrics.

Author: Yug Soni
"""

def compute_crf(discount_rate, project_life):
    """Capital Recovery Factor."""
    i = discount_rate
    n = project_life
    return i * (1 + i)**n / ((1 + i)**n - 1)


def compute_lcom(annualised_capex, annual_opex, annual_production):
    """Levelised Cost of Methanol ($/t)."""
    return (annualised_capex + annual_opex) * 1e6 / annual_production


def compute_npv(capex, annual_revenue, annual_opex, discount_rate, project_life):
    """Net Present Value ($M)."""
    i = discount_rate
    n = project_life
    annuity = (1 - (1 + i)**-n) / i
    return -capex + (annual_revenue - annual_opex) * annuity


def compute_dscr(ebitda, annual_debt_service):
    """Debt Service Coverage Ratio."""
    return ebitda / annual_debt_service


def compute_breakeven_h2(commodity_price, annualised_capex, non_h2_opex,
                         annual_h2_demand):
    """Breakeven hydrogen price ($/kg) for commodity market."""
    revenue = commodity_price * 100000 / 1e6  # $M for 100kt/yr
    return (revenue - annualised_capex - non_h2_opex) / annual_h2_demand


class EconomicModel:
    """Full techno-economic model for green methanol plant."""

    def __init__(self, tci=55.2, opex=106.22, production=100000,
                 discount_rate=0.10, project_life=20):
        self.tci = tci  # $M
        self.opex = opex  # $M/yr
        self.production = production  # t/yr
        self.discount_rate = discount_rate
        self.project_life = project_life
        self.crf = compute_crf(discount_rate, project_life)

    def lcom(self):
        """Levelised cost of methanol ($/t)."""
        annualised = self.crf * self.tci
        return compute_lcom(annualised, self.opex, self.production)

    def npv(self, selling_price):
        """NPV at given selling price ($/t)."""
        revenue = selling_price * self.production / 1e6
        return compute_npv(self.tci, revenue, self.opex,
                          self.discount_rate, self.project_life)

    def breakeven_price(self):
        """Selling price for NPV=0 ($/t)."""
        annualised = self.crf * self.tci
        return (annualised + self.opex) * 1e6 / self.production


if __name__ == "__main__":
    model = EconomicModel()
    print("=== Economic Model Results ===")
    print(f"LCOM: ${model.lcom():.0f}/t")
    print(f"NPV @ $1000/t: ${model.npv(1000):.0f}M")
    print(f"NPV @ $346/t: ${model.npv(346):.0f}M")
    print(f"Breakeven price: ${model.breakeven_price():.0f}/t\n")