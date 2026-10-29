import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


# ---------- helper to keep tests short ----------
def manifest(tier="general", orders=None, confirmed=True, lounge=False):
    return {
        "is_confirmed": confirmed,
        "tier": tier,
        "exclusive_lounge": lounge,
        "orders": orders if orders is not None else [],
    }


# ---------- original starter test ----------
def test_single_general_order():
    manifests = [manifest("general", [{"qty": 2, "promo": ""}])]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


# ---------- process_ticket_manifest: validation (line 3) ----------
def test_invalid_manifests_type_raises():
    with pytest.raises(ValueError):
        process_ticket_manifest("not a list", 0.1)


# ---------- unconfirmed manifest skipped (line 10) ----------
def test_unconfirmed_manifest_is_skipped():
    result = process_ticket_manifest(
        [manifest("vip", [{"qty": 1, "promo": ""}], confirmed=False)], 0.1
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- tier pricing (lines 16, 18) ----------
def test_vip_tier_price():
    result = process_ticket_manifest([manifest("vip", [{"qty": 1, "promo": ""}])], 0.0)
    assert result["total_revenue"] == 150.0
    assert result["status"] == "COMPLETED"


def test_premium_tier_price():
    result = process_ticket_manifest([manifest("premium", [{"qty": 2, "promo": ""}])], 0.0)
    assert result["total_revenue"] == 180.0
    assert result["status"] == "COMPLETED"


# ---------- unknown tier rejected (lines 22-23) ----------
def test_unknown_tier_is_rejected():
    result = process_ticket_manifest([manifest("balcony", [{"qty": 1, "promo": ""}])], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- invalid quantity rejected (lines 32-33) ----------
def test_zero_quantity_order_is_rejected():
    result = process_ticket_manifest([manifest("general", [{"qty": 0, "promo": ""}])], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- fraud on VIP voids whole manifest (lines 38-41) ----------
def test_vip_fraud_risk_voids_manifest():
    orders = [
        {"qty": 1, "promo": ""},
        {"qty": 1, "promo": "FRAUD_RISK"},
        {"qty": 1, "promo": ""},  # never reached because of break
    ]
    result = process_ticket_manifest([manifest("vip", orders)], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- EARLYBIRD promo (line 43) ----------
def test_earlybird_promo_gives_20_percent_off():
    result = process_ticket_manifest([manifest("general", [{"qty": 10, "promo": "EARLYBIRD"}])], 0.0)
    assert result["total_revenue"] == pytest.approx(360.0)  # 10*45*0.8
    assert result["status"] == "COMPLETED"


# ---------- bulk discount (line 46) ----------
def test_bulk_discount_for_five_or_more():
    result = process_ticket_manifest([manifest("general", [{"qty": 5, "promo": ""}])], 0.0)
    assert result["total_revenue"] == 205.0  # 5*45 - 20


# ---------- exclusive lounge (line 51) ----------
def test_exclusive_lounge_adds_flat_fee():
    result = process_ticket_manifest(
        [manifest("general", [{"qty": 1, "promo": ""}], lounge=True)], 0.0
    )
    assert result["total_revenue"] == 120.0  # 45 + 75


# ---------- audit rejection (line 58) ----------
def test_audit_rejected_when_more_than_four_rejections():
    orders = [{"qty": 1, "promo": ""}] + [{"qty": 0, "promo": ""}] * 5
    result = process_ticket_manifest([manifest("general", orders)], 0.0)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total_revenue"] == 45.0


# ---------- monitor_gate_flow (lines 65-77) ----------
def test_gate_flow_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_overflow_on_two_consecutive_high_rates():
    assert monitor_gate_flow([[10, 60, 70]]) == "OVERFLOW"


def test_gate_flow_normal_when_streak_is_broken():
    assert monitor_gate_flow([[60, 10, 60, 10]]) == "FLOW_NORMAL"


# =====================================================================
# EXTRA TESTS FOR BRANCH COVERAGE (True AND False side of every decision)
# =====================================================================

# ---------- line 38/39: FRAUD_RISK on a NON-vip tier (branch 39 -> 48) ----------
# The order is counted as rejected, but the loop does NOT break,
# so the order is still added to the manifest total (current behaviour).
def test_non_vip_fraud_risk_is_rejected_but_not_voided():
    result = process_ticket_manifest(
        [manifest("general", [{"qty": 2, "promo": "FRAUD_RISK"}])], 0.0
    )
    assert result["total_revenue"] == 90.0
    assert result["status"] == "COMPLETED"


# ---------- VIP fraud break, lounge fee still added afterwards ----------
def test_vip_fraud_risk_still_adds_lounge_fee():
    result = process_ticket_manifest(
        [manifest("vip", [{"qty": 1, "promo": "FRAUD_RISK"}], lounge=True)], 0.0
    )
    assert result["total_revenue"] == 75.0
    assert result["status"] == "COMPLETED"


# ---------- line 2: second half of the validation condition ----------
def test_negative_tax_rate_raises():
    with pytest.raises(ValueError):
        process_ticket_manifest([manifest("general", [{"qty": 1, "promo": ""}])], -0.01)


def test_zero_tax_rate_is_allowed():
    result = process_ticket_manifest([manifest("general", [{"qty": 1, "promo": ""}])], 0.0)
    assert result["total_revenue"] == 45.0


# ---------- line 9: is_confirmed missing -> defaults to False ----------
def test_missing_is_confirmed_defaults_to_unconfirmed():
    m = {"tier": "vip", "orders": [{"qty": 1, "promo": ""}]}
    result = process_ticket_manifest([m], 0.0)
    assert result["status"] == "ZERO_SALES"


# ---------- line 12: tier missing -> defaults to general ----------
def test_missing_tier_defaults_to_general():
    m = {"is_confirmed": True, "orders": [{"qty": 1, "promo": ""}]}
    result = process_ticket_manifest([m], 0.0)
    assert result["total_revenue"] == 45.0


# ---------- line 28/31: qty missing -> 0 -> rejected; negative qty rejected ----------
def test_missing_qty_is_rejected():
    result = process_ticket_manifest([manifest("general", [{"promo": ""}])], 0.0)
    assert result["status"] == "ZERO_SALES"


def test_negative_qty_is_rejected():
    result = process_ticket_manifest([manifest("general", [{"qty": -3, "promo": ""}])], 0.0)
    assert result["status"] == "ZERO_SALES"


# ---------- line 45: bulk discount boundary (4 = no discount, 5 = discount) ----------
def test_quantity_four_gets_no_bulk_discount():
    result = process_ticket_manifest([manifest("general", [{"qty": 4, "promo": ""}])], 0.0)
    assert result["total_revenue"] == 180.0  # 4*45


# ---------- line 42/44: unknown promo code falls through to the normal path ----------
def test_unknown_promo_behaves_like_no_promo():
    result = process_ticket_manifest([manifest("general", [{"qty": 5, "promo": "RANDOM"}])], 0.0)
    assert result["total_revenue"] == 205.0


# ---------- line 57: audit boundary (exactly 4 rejections is NOT an audit failure) ----------
def test_exactly_four_rejections_is_not_audit_rejected():
    orders = [{"qty": 1, "promo": ""}] + [{"qty": 0, "promo": ""}] * 4
    result = process_ticket_manifest([manifest("general", orders)], 0.0)
    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] == 45.0


# ---------- tax is applied to the total ----------
def test_tax_applied_to_vip_order():
    result = process_ticket_manifest([manifest("vip", [{"qty": 1, "promo": ""}])], 0.1)
    assert result["total_revenue"] == 165.0


# ---------- line 59: empty list of manifests ----------
def test_empty_manifest_list_is_zero_sales():
    assert process_ticket_manifest([], 0.1) == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- multiple manifests accumulate ----------
def test_multiple_manifests_are_summed():
    ms = [
        manifest("general", [{"qty": 1, "promo": ""}]),
        manifest("premium", [{"qty": 1, "promo": ""}]),
    ]
    assert process_ticket_manifest(ms, 0.0)["total_revenue"] == 135.0


# ---------- monitor_gate_flow: extra branches ----------
def test_gate_flow_none_is_no_data():
    assert monitor_gate_flow(None) == "NO_DATA"


def test_gate_flow_rate_of_exactly_50_is_not_congested():
    assert monitor_gate_flow([[50, 50, 50]]) == "FLOW_NORMAL"


def test_gate_flow_51_twice_is_overflow():
    assert monitor_gate_flow([[51, 51]]) == "OVERFLOW"


def test_gate_flow_empty_stream_is_normal():
    assert monitor_gate_flow([[]]) == "FLOW_NORMAL"


def test_gate_flow_single_high_rate_is_normal():
    assert monitor_gate_flow([[60]]) == "FLOW_NORMAL"


def test_gate_flow_streak_resets_between_streams():
    assert monitor_gate_flow([[60], [60]]) == "FLOW_NORMAL"


def test_gate_flow_overflow_found_in_second_stream():
    assert monitor_gate_flow([[10, 20], [60, 70]]) == "OVERFLOW"
