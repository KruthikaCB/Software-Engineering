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
