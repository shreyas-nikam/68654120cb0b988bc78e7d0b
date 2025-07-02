import pytest
from definition_dc5c050f3f594d889b594cebe9337c86 import generate_bond_cash_flows

@pytest.mark.parametrize("bond_type, face_value, issue_price, coupon_rate, maturity_years, payment_frequency", [
    ("Zero-Coupon", 1000, 950, 0.0, 5, 1),        # Standard zero-coupon bond
    ("Coupon", 1000, 1000, 0.05, 10, 2),        # Semiannual coupon bond
    ("Coupon", 500, 550, 0.03, 3, 1),           # Annual coupon, face_value lower than issue_price
    ("Zero-Coupon", 2000, 2000, 0.0, 1, 12),    # Maturity of 1 year, monthly payments (though zero coupon)
    ("Coupon", 1500, 1400, 0.04, 7, 4),        # Quarterly payments
    ("Coupon", 1000, 900, 0.07, 8, 1),         # Annual coupon, discounted issue price
])
def test_generate_bond_cash_flows(bond_type, face_value, issue_price, coupon_rate, maturity_years, payment_frequency):
    df = generate_bond_cash_flows(bond_type, face_value, issue_price, coupon_rate, maturity_years, payment_frequency)
    # Check DataFrame has correct columns
    assert "Period" in df.columns
    assert "Pre_Tax_Cash_Flow" in df.columns
    # Check total number of periods
    expected_periods = maturity_years * payment_frequency
    assert len(df) == expected_periods or len(df) == expected_periods + 1  # inclusive of last principal
    # For zero-coupon, coupons should be zero except at maturity
    if bond_type == "Zero-Coupon":
        coupons = df["Coupon_Payment"]
        # All coupons except last should be zero
        assert all(coupons[:-1] == 0)
        # Last should include face value principal
        assert abs(coupons.iloc[-1] - face_value) < 1e-6
    # For coupon bonds, coupons should match calculation
    if bond_type == "Coupon":
        # Check coupons are non-negative
        assert all(df["Coupon_Payment"] >= 0)
        # Last cash flow should include face value principal
        principal_last = df["Principal_Payment"].iloc[-1]
        assert abs(principal_last - face_value) < 1e-6
    # Check that for all periods, cash flows are positive or zero
    assert all(df["Pre_Tax_Cash_Flow"] >= 0)
    # Total cash flows should correspond to sum of coupons plus principal at last
    total_coupons = df["Coupon_Payment"].sum()
    last_principal = df["Principal_Payment"].iloc[-1]
    total_cash_flow = df["Pre_Tax_Cash_Flow"].sum()
    if bond_type == "Zero-Coupon":
        # Only last period includes face value
        assert abs(total_cash_flow - last_principal) < 1e-6
    else:
        # Sum of coupons + principal
        assert abs(total_cash_flow - (total_coupons + last_principal)) < 1e-6
