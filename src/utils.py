"""
Utility functions for unit conversions and helpers.

Author: Yug Soni
"""

def celsius_to_kelvin(T_C):
    return T_C + 273.15

def kelvin_to_celsius(T_K):
    return T_K - 273.15

def bar_to_pa(P_bar):
    return P_bar * 1e5

def pa_to_bar(P_pa):
    return P_pa / 1e5

def kg_to_tonnes(m_kg):
    return m_kg / 1000.0

def tonnes_to_kg(m_t):
    return m_t * 1000.0

def mw_methanol():
    return 32.04

def mw_co2():
    return 44.01

def stoichiometric_h2_co2_ratio():
    return 3.0

def co2_sequestration_credit():
    return 44.01 / 32.04

print("Utilities and helpers successfully loaded.")