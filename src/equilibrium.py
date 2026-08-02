"""
Thermodynamic equilibrium model for CO2 hydrogenation to methanol.

Reactions:
    (1) CO2 + 3H2 <=> CH3OH + H2O     (methanol synthesis)
    (2) CO2 + H2 <=> CO + H2O          (reverse water-gas shift)

Uses NIST Shomate coefficients.
Author: Yug Soni
"""
import numpy as np
from scipy.optimize import fsolve

R = 8.314  # J/mol/K

# Shomate coefficients: A, B, C, D, E, dHf298 (kJ/mol)
SPECIES = {
    'CO2':   dict(A=24.997, B=55.187,  C=-33.691, D=7.948,  E=-0.137, dHf=-393.51),
    'H2':    dict(A=33.066, B=-11.363, C=11.433,  D=-2.773, E=-0.159, dHf=0.0),
    'CH3OH': dict(A=21.150, B=70.870,  C=-55.998, D=17.318, E=0.002,  dHf=-201.00),
    'H2O':   dict(A=30.092, B=6.833,   C=6.793,   D=-2.534, E=0.082,  dHf=-241.83),
    'CO':    dict(A=25.568, B=6.096,   C=4.055,   D=-2.671, E=0.131,  dHf=-110.53),
}

# Standard entropy at 298 K (J/mol/K)
S298 = {
    'CO2': 213.79, 'H2': 130.68, 'CH3OH': 239.9,
    'H2O': 188.84, 'CO': 197.66
}


def shomate_H(T, species_name):
    """Standard enthalpy H(T) in kJ/mol using Shomate integration."""
    t = T / 1000.0
    c = SPECIES[species_name]
    H = (c['A']*t + c['B']*t**2/2 + c['C']*t**3/3 +
         c['D']*t**4/4 - c['E']/t)
    H_ref = (c['A']*0.298 + c['B']*0.298**2/2 + c['C']*0.298**3/3 +
             c['D']*0.298**4/4 - c['E']/0.298)
    return c['dHf'] + (H - H_ref)  # kJ/mol


def shomate_S(T, species_name):
    """Standard entropy S(T) in J/mol/K using Shomate integration."""
    t = T / 1000.0
    c = SPECIES[species_name]
    S = (c['A']*np.log(t) + c['B']*t + c['C']*t**2/2 +
         c['D']*t**3/3 - c['E']/(2*t**2))
    S_ref = (c['A']*np.log(0.298) + c['B']*0.298 + c['C']*0.298**2/2 +
             c['D']*0.298**3/3 - c['E']/(2*0.298**2))
    return S298[species_name] + (S - S_ref)


def dG_reaction(T, reaction):
    """Gibbs free energy change for a reaction at T (K)."""
    if reaction == 1:  # CO2 + 3H2 -> CH3OH + H2O
        dH = (shomate_H(T, 'CH3OH') + shomate_H(T, 'H2O')
              - shomate_H(T, 'CO2') - 3*shomate_H(T, 'H2'))
        dS = (shomate_S(T, 'CH3OH') + shomate_S(T, 'H2O')
              - shomate_S(T, 'CO2') - 3*shomate_S(T, 'H2'))
    elif reaction == 2:  # CO2 + H2 -> CO + H2O
        dH = (shomate_H(T, 'CO') + shomate_H(T, 'H2O')
              - shomate_H(T, 'CO2') - shomate_H(T, 'H2'))
        dS = (shomate_S(T, 'CO') + shomate_S(T, 'H2O')
              - shomate_S(T, 'CO2') - shomate_S(T, 'H2'))
    else:
        raise ValueError("reaction must be 1 or 2")
    return dH - T * dS / 1000.0


def Keq(T, reaction):
    """Equilibrium constant at temperature T (K)."""
    dG = dG_reaction(T, reaction)
    return np.exp(-dG * 1000 / (R * T))


def equilibrium_solve(T, P, H2_CO2_ratio=3.0, n_CO2_0=1.0, n_N2_0=0.001):
    """Solve for equilibrium composition at fixed T and P."""
    T_K = T + 273.15
    K1 = Keq(T_K, 1)
    K2 = Keq(T_K, 2)
    n_H2_0 = H2_CO2_ratio * n_CO2_0
    P0 = 1.0

    def equations(x):
        xi1, xi2 = x
        n_CO2 = n_CO2_0 - xi1 - xi2
        n_H2 = n_H2_0 - 3*xi1 - xi2
        n_CH3OH = xi1
        n_H2O = xi1 + xi2
        n_CO = xi2
        n_tot = n_CO2 + n_H2 + n_CH3OH + n_H2O + n_CO + n_N2_0

        if n_CO2 <= 0 or n_H2 <= 0 or n_tot <= 0:
            return [1e6, 1e6]

        y_CO2 = n_CO2 / n_tot
        y_H2 = n_H2 / n_tot
        y_CH3OH = n_CH3OH / n_tot
        y_H2O = n_H2O / n_tot
        y_CO = n_CO / n_tot

        eq1 = (y_CH3OH * y_H2O) / (y_CO2 * y_H2**3) * (P/P0)**(-2) - K1
        eq2 = (y_CO * y_H2O) / (y_CO2 * y_H2) - K2
        return [eq1, eq2]

    x0 = [0.15 * n_CO2_0, 0.01 * n_CO2_0]
    sol = fsolve(equations, x0, full_output=True)
    xi1, xi2 = sol[0]
    conv = (xi1 + xi2) / n_CO2_0 * 100
    sel = xi1 / (xi1 + xi2) * 100 if (xi1 + xi2) > 0 else 0

    return {
        'xi1': xi1, 'xi2': xi2,
        'X_CO2': conv, 'S_MeOH': sel,
        'T': T, 'P': P
    }


if __name__ == "__main__":
    T_design = 250 + 273.15
    K1 = Keq(T_design, 1)
    K2 = Keq(T_design, 2)
    print("=== Thermodynamic Model Validation ===")
    print(f"Design point (250°C):")
    print(f"  Keq1 (methanol) = {K1:.3e}")
    print(f"  Keq2 (RWGS) = {K2:.3e}  ")

    res = equilibrium_solve(250, 50, 3.0)
    print(f"  Isothermal X_CO2 = {res['X_CO2']:.1f}% ")
    print(f"  Isothermal S_MeOH = {res['S_MeOH']:.1f}%\n")