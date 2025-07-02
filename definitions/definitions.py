
import pandas as pd
from typing import Union

def generate_bond_cash_flows(
    bond_type: str,
    face_value: float,
    issue_price: float,
    coupon_rate: float,
    maturity_years: int,
    payment_frequency: int
) -> pd.DataFrame:
    """
    Creates a schedule of pre-tax cash flows for a specified bond.

    Args:
        bond_type (str): 'Zero-Coupon' or 'Coupon'.
        face_value (float): Par value of the bond.
        issue_price (float): Issue price of the bond.
        coupon_rate (float): Annual coupon rate as decimal. Ignored for zero-coupon bonds.
        maturity_years (int): Number of years until maturity.
        payment_frequency (int): Number of payments per year.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - 'Period': Payment period number
            - 'Coupon_Payment': Coupon payment amount for the period
            - 'Principal_Payment': Principal repayment at period end
            - 'Pre_Tax_Cash_Flow': Total cash flow in each period
    """
    # Validate inputs
    if bond_type not in ('Zero-Coupon', 'Coupon'):
        raise ValueError(f"Invalid bond_type: {bond_type}. Must be 'Zero-Coupon' or 'Coupon'.")
    if maturity_years <= 0:
        raise ValueError("maturity_years must be positive.")
    if payment_frequency <= 0:
        raise ValueError("payment_frequency must be positive.")
    if face_value <= 0:
        raise ValueError("face_value must be positive.")
    if issue_price < 0:
        raise ValueError("issue_price cannot be negative.")

    total_periods = int(maturity_years * payment_frequency)

    # Initialize list to collect cash flows
    cash_flows = []

    if bond_type == 'Zero-Coupon':
        for period in range(1, total_periods + 1):
            if period == total_periods:
                coupon_payment = 0.0
                principal_payment = face_value
            else:
                coupon_payment = 0.0
                principal_payment = 0.0
            pre_tax_cash_flow = coupon_payment + principal_payment
            cash_flows.append({
                'Period': period,
                'Coupon_Payment': coupon_payment,
                'Principal_Payment': principal_payment,
                'Pre_Tax_Cash_Flow': pre_tax_cash_flow
            })
    else:  # Coupon bond
        periodic_coupon = face_value * coupon_rate / payment_frequency
        for period in range(1, total_periods + 1):
            coupon_payment = periodic_coupon
            principal_payment = face_value if period == total_periods else 0.0
            pre_tax_cash_flow = coupon_payment + principal_payment
            cash_flows.append({
                'Period': period,
                'Coupon_Payment': coupon_payment,
                'Principal_Payment': principal_payment,
                'Pre_Tax_Cash_Flow': pre_tax_cash_flow
            })

    df = pd.DataFrame(cash_flows)
    return df
