"""
Monte Carlo uncertainty quantification for techno-economic analysis.

Author: Yug Soni
"""
from scipy.stats import spearmanr


def lognormal_params(mean, std):
    """Convert mean/std to lognormal mu/sigma."""
    sigma2 = np.log(1 + (std/mean)**2)
    mu = np.log(mean) - sigma2/2
    sigma = np.sqrt(sigma2)
    return mu, sigma


def run_monte_carlo(N=10000, seed=42):
    """Run Monte Carlo simulation for NPV uncertainty."""
    np.random.seed(seed)

    # --- Input distributions ---
    mu_h2, sigma_h2 = lognormal_params(3.50, 0.70)
    H2_price = np.random.lognormal(mu_h2, sigma_h2, N)
    H2_price = np.clip(H2_price, 2.0, 6.0)

    MeOH_price = np.random.normal(1000, 150, N)
    MeOH_price = np.clip(MeOH_price, 500, 1500)

    CO2_cost = np.random.triangular(25, 45, 75, N)
    Elec = np.random.normal(0.07, 0.0105, N)
    Elec = np.clip(Elec, 0.04, 0.10)

    CAPEX = np.random.triangular(44.2, 55.2, 69.0, N)
    OPEX_mult = np.random.uniform(0.90, 1.10, N)
    CF = np.random.normal(0.90, 0.045, N)
    CF = np.clip(CF, 0.75, 1.00)

    # --- Economic model ---
    H2_consumption = 87.44 / 3.50  # M kg/yr
    CO2_consumption = 16.85 / 45.0  # M tonnes/yr
    production = 100000 * (CF / 0.90)  # t/yr

    OPEX = ((H2_consumption * H2_price * 1e6 +
             CO2_consumption * 1e6 * CO2_cost +
             Elec / 0.07 * 0.82e6 +
             0.14e6 + 0.43e6 + 0.54e6) * OPEX_mult / 1e6)

    CRF = 0.1175
    Annualised_CAPEX = CRF * CAPEX
    LCOM = (Annualised_CAPEX + OPEX) * 1e6 / production

    Revenue_marine = MeOH_price * production / 1e6
    i, n = 0.10, 20
    annuity_factor = (1 - (1 + i)**-n) / i
    annual_net_cf = Revenue_marine - OPEX
    NPV = -CAPEX + annual_net_cf * annuity_factor

    # Spearman correlations
    rho_meoh, _ = spearmanr(MeOH_price, NPV)
    rho_h2, _ = spearmanr(H2_price, NPV)
    rho_capex, _ = spearmanr(CAPEX, NPV)

    return {
        'NPV': NPV,
        'LCOM': LCOM,
        'H2_price': H2_price,
        'MeOH_price': MeOH_price,
        'CAPEX': CAPEX,
        'CF': CF,
        'statistics': {
            'mean_NPV': NPV.mean(),
            'median_NPV': np.median(NPV),
            'std_NPV': NPV.std(),
            'p_positive': (NPV > 0).mean() * 100,
            'var5': np.percentile(NPV, 5),
            'mean_LCOM': LCOM.mean(),
            'lcom_5pct': np.percentile(LCOM, 5),
            'lcom_95pct': np.percentile(LCOM, 95),
            'rho_MeOH': rho_meoh,
            'rho_H2': rho_h2,
            'rho_CAPEX': rho_capex,
        }
    }


if __name__ == "__main__":
    results = run_monte_carlo(N=10000, seed=42)
    stats = results['statistics']
    print("=== Monte Carlo Results (10,000 iterations, seed=42) ===")
    print(f"Mean NPV: ${stats['mean_NPV']:.1f}M")
    print(f"Median NPV: ${stats['median_NPV']:.1f}M")
    print(f"Std dev NPV: ${stats['std_NPV']:.1f}M")
    print(f"P(NPV>0): {stats['p_positive']:.1f}%")
    print(f"5% VaR: ${stats['var5']:.1f}M")
    print(f"Mean LCOM: ${stats['mean_LCOM']:.0f}/t")
    print(f"Spearman rho (MeOH price): {stats['rho_MeOH']:.2f}")
    print(f"Spearman rho (H2 price): {stats['rho_H2']:.2f}")
    print(f"Spearman rho (CAPEX): {stats['rho_CAPEX']:.2f}\n")