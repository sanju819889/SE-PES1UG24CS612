
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow

# Example test case:
def test_single_general_order():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "exclusive_lounge": False,
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!

# Additional test cases for process_ticket_manifest()

def test_invalid_manifest_type():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_unconfirmed_manifest():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "vip"}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_vip_ticket():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 300.0


def test_premium_ticket():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "premium",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 180.0


def test_general_ticket():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_unknown_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "student",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_zero_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_negative_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": -2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0
    )
    assert result["total_revenue"] == 72.0


def test_bulk_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5}]}], 0
    )
    assert result["total_revenue"] == 205.0


def test_fraud_risk_non_vip():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["total_revenue"] == 90.0
    assert result["status"] == "COMPLETED"


def test_fraud_risk_vip():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_vip_fraud_resets_previous_total():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [
              {"qty": 2},
              {"qty": 1, "promo": "FRAUD_RISK"},
              {"qty": 3}
          ]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_exclusive_lounge():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True, "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 165.0


def test_audit_rejected():
    manifests = [
        {"is_confirmed": True, "tier": "general",
         "orders": [{"qty": 0}]}
        for _ in range(5)
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["status"] == "AUDIT_REJECTED"


def test_completed_with_tax():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


def test_missing_confirmation_defaults_false():
    result = process_ticket_manifest(
        [{"tier": "general", "orders": [{"qty": 2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_missing_tier_defaults_general():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_missing_orders_defaults_empty():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general"}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_missing_quantity_defaults_zero():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_multiple_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}, {"qty": 3}]}], 0
    )
    assert result["total_revenue"] == 225.0


# Additional test cases for monitor_gate_flow()

def test_no_gate_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_normal_gate_flow():
    assert monitor_gate_flow([[10, 20, 30]]) == "FLOW_NORMAL"


def test_single_high_rate():
    assert monitor_gate_flow([[60]]) == "FLOW_NORMAL"


def test_two_consecutive_high_rates():
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"


def test_high_rates_separated_by_normal_rate():
    assert monitor_gate_flow([[60, 20, 70]]) == "FLOW_NORMAL"


def test_overflow_in_second_stream():
    assert monitor_gate_flow([[60], [55, 65]]) == "OVERFLOW"


def test_empty_stream():
    assert monitor_gate_flow([[]]) == "FLOW_NORMAL"


def test_exact_threshold():
    assert monitor_gate_flow([[50, 50, 50]]) == "FLOW_NORMAL"


def test_non_consecutive_high_rates_across_streams():
    assert monitor_gate_flow([[60], [60]]) == "FLOW_NORMAL"
