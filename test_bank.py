import pytest
from bank import transfer_funds


@pytest.fixture
def accounts():
    return (
        {"id": 1, "balance": 500.00, "owner": "Alice"},
        {"id": 2, "balance": 100.00, "owner": "Bob"},
    )


def test_successful_transfer_decreases_source_balance(accounts):
    src, dst = accounts
    transfer_funds(src, dst, 200)
    assert src["balance"] == 300.00


def test_successful_transfer_increases_destination_balance(accounts):
    src, dst = accounts
    transfer_funds(src, dst, 200)
    assert dst["balance"] == 300.00


def test_returns_transaction_record(accounts):
    src, dst = accounts
    result = transfer_funds(src, dst, 200)
    assert result["from_id"] == 1
    assert result["to_id"] == 2
    assert result["amount"] == 200
    assert result["from_balance_after"] == 300.00
    assert result["to_balance_after"] == 300.00


def test_zero_amount_raises_value_error(accounts):
    src, dst = accounts
    with pytest.raises(ValueError):
        transfer_funds(src, dst, 0)


def test_negative_amount_raises_value_error(accounts):
    src, dst = accounts
    with pytest.raises(ValueError):
        transfer_funds(src, dst, -50)


def test_insufficient_funds_raises_value_error(accounts):
    src, dst = accounts
    with pytest.raises(ValueError):
        transfer_funds(src, dst, 600)


def test_same_account_raises_value_error():
    account = {"id": 1, "balance": 500.00, "owner": "Alice"}
    with pytest.raises(ValueError):
        transfer_funds(account, account, 100)


def test_exact_balance_transfer_leaves_zero(accounts):
    src, dst = accounts
    transfer_funds(src, dst, 500)
    assert src["balance"] == 0.00

