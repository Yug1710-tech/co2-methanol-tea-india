"""
Coupled adiabatic equilibrium-energy balance reactor model.

Author: Yug Soni
"""
# Note: Keq and shomate_H are inherited from Cell 1

def adiabatic_solve(T_in, P, H2_CO2_ratio, n_CO2_0=1.0):
    """Solve coupled equilibrium + adiabatic energy balance."""
    n_H2_0 = H2_CO2_ratio * n_CO2_0
    P0 = 1.0

    def equations(x):
        xi1, xi2, T_ad = x

        K1 = Keq(T_ad, 1)
        K2 = Keq(T_ad, 2)

        n_CO2 = n_CO2_0 - xi1 - xi2
        n_H2 = n_H2_0 - 3*xi1 - xi2
        n_CH3OH = xi1
        n_H2O = xi1 + xi2
        n_CO = xi2
        n_tot = n_CO2 + n_H2 + n_CH3OH + n_H2O + n_CO

        if n_CO2 <= 1e-8 or n_H2 <= 1e-8 or n_tot <= 0:
            return [1e6, 1e6, 1e6]

        y_CO2 = n_CO2 / n_tot
        y_H2 = n_H2 / n_tot
        y_CH3OH = n_CH3OH / n_tot
        y_H2O = n_H2O / n_tot
        y_CO = n_CO / n_tot

        eq1 = (y_CH3OH * y_H2O) / (y_CO2 * y_H2**3) * (P/P0)**(-2) - K1
        eq2 = (y_CO * y_H2O) / (y_CO2 * y_H2) - K2

        # Energy balance: H_in = H_out
        H_in = (n_CO2_0 * shomate_H(T_in, 'CO2') +
                n_H2_0 * shomate_H(T_in, 'H2'))
        H_out = (n_CO2 * shomate_H(T_ad, 'CO2') +
                 n_H2 * shomate_H(T_ad, 'H2') +
                 n_CH3OH * shomate_H(T_ad, 'CH3OH') +
                 n_H2O * shomate_H(T_ad, 'H2O') +
                 n_CO * shomate_H(T_ad, 'CO'))

        eq3 = (H_in - H_out) / 10.0  # scale for solver conditioning

        return [eq1, eq2, eq3]

    T_in_K = T_in if T_in > 500 else T_in + 273.15
    x0 = [0.15, 0.02, T_in_K + 20]
    sol = fsolve(equations, x0, full_output=True, xtol=1e-10)
    xi1, xi2, T_ad = sol[0]
    ier = sol[2]

    conv = (xi1 + xi2) / n_CO2_0 * 100
    sel = xi1 / (xi1 + xi2) * 100 if (xi1 + xi2) > 0 else 0

    return {
        'xi1': xi1, 'xi2': xi2,
        'T_ad': T_ad, 'T_ad_C': T_ad - 273.15,
        'X_CO2': conv, 'S_MeOH': sel,
        'converged': ier == 1,
        'T_in_C': T_in_K - 273.15
    }


if __name__ == "__main__":
    T_in = 250 + 273.15
    P = 50
    result = adiabatic_solve(T_in, P, 3.0)
    print("=== Coupled Adiabatic Solve Results ===")
    print(f"  Converged: {result['converged']}")
    print(f"  xi1 = {result['xi1']:.5f}, xi2 = {result['xi2']:.5f}")
    print(f"  T_adiabatic = {result['T_ad_C']:.1f}°C ")
    print(f"  CO2 conversion = {result['X_CO2']:.2f}%  ")
    print(f"  MeOH selectivity = {result['S_MeOH']:.2f}% ")