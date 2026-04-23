from app.cli import parse_args, positive_int
import argparse
import pytest


def test_defaults():
    args = parse_args([])

    assert args.transphobia is False
    assert args.threads == 4
    assert args.verify is False
    assert args.retry_errors is False
    assert args.clear_errors is False

def test_positive_int_rejects_zero():
    with pytest.raises(argparse.ArgumentTypeError):
        positive_int("0")

def test_transphobia_flag():
    args = parse_args(["--transphobia"])
    assert args.transphobia is True


def test_verify_flag():
    args = parse_args(["--verify"])
    assert args.verify is True


def test_retry_errors_flag():
    args = parse_args(["--retry-errors"])
    assert args.retry_errors is True


def test_clear_errors_flag():
    args = parse_args(["--clear-errors"])
    assert args.clear_errors is True


def test_threads_custom_value():
    args = parse_args(["--threads", "8"])
    assert args.threads == 8


def test_threads_accepts_one():
    args = parse_args(["--threads", "1"])
    assert args.threads == 1


def test_multiple_flags_together():
    args = parse_args([
        "--verify",
        "--retry-errors",
        "--threads", "6"
    ])

    assert args.verify is True
    assert args.retry_errors is True
    assert args.threads == 6

def test_positive_int_accepts_valid_value():
    assert positive_int("3") == 3


def test_parse_args_uses_sys_argv_when_none(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["prog", "--threads", "7", "--verify"]
    )

    args = parse_args()

    assert args.threads == 7
    assert args.verify is True

def test_invalid_threads_non_integer():
    with pytest.raises(SystemExit):
        parse_args(["--threads", "abc"])


def test_unknown_argument():
    with pytest.raises(SystemExit):
        parse_args(["--banana"])