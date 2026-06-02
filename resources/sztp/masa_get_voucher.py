#!/usr/bin/env python3
"""
Download an existing MASA voucher for a single serial number.

Endpoint:
  GET https://masa.cisco.com/api/download/device/{serial}
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

MASA_BASE_URL = "https://masa.cisco.com/api"


def parse_args():
    p = argparse.ArgumentParser(description="Download existing MASA voucher for a serial")
    p.add_argument("serial", help="Device serial number, e.g. FCW2146G095")
    p.add_argument("--token", help="MASA bearer token (or set MASA_API_TOKEN)")
    p.add_argument("--cert", help="Client certificate path (optional)")
    p.add_argument("--key", help="Client key path (optional)")
    p.add_argument("--url", default=MASA_BASE_URL, help=f"Base URL (default: {MASA_BASE_URL})")
    p.add_argument(
        "--output",
        help="Output .vcj file path (default: vouchers/api_generated/<SERIAL>.vcj)",
    )
    return p.parse_args()


def looks_like_html(data):
    head = data[:1024].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def extract_bytes(resp):
    body = resp.content or b""
    if not body:
        raise ValueError("Empty response body")
    if looks_like_html(body):
        raise ValueError("Received HTML instead of voucher content")

    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" in ctype or body.lstrip().startswith((b"{", b"[")):
        try:
            payload = resp.json()
        except ValueError as exc:
            raise ValueError(f"Response looked like JSON but failed to parse: {exc}") from exc

        # Some APIs may wrap the voucher as a field in JSON.
        if isinstance(payload, dict):
            for key in ("voucher-cms", "voucher_cms", "voucherCms", "vcj", "voucher"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    return value.encode("utf-8")

        raise ValueError("JSON response did not include recognizable voucher payload")

    return body


def main():
    args = parse_args()

    token = (args.token or os.getenv("MASA_API_TOKEN") or "").strip()
    cert_path = (args.cert or os.getenv("MASA_CLIENT_CERT") or "").strip()
    key_path = (args.key or os.getenv("MASA_CLIENT_KEY") or "").strip()

    if not token and not (cert_path and key_path):
        print("Authentication is required.")
        print("Provide --token, or both --cert and --key.")
        print("Environment variables also supported: MASA_API_TOKEN, MASA_CLIENT_CERT, MASA_CLIENT_KEY")
        sys.exit(1)

    if (cert_path and not key_path) or (key_path and not cert_path):
        print("For certificate auth, both --cert and --key are required.")
        sys.exit(1)

    if cert_path and not Path(cert_path).exists():
        print(f"Certificate file not found: {cert_path}")
        sys.exit(1)

    if key_path and not Path(key_path).exists():
        print(f"Key file not found: {key_path}")
        sys.exit(1)

    serial = args.serial.strip().upper()
    out = Path(args.output) if args.output else Path("vouchers") / "api_generated" / f"{serial}.vcj"
    if out.suffix.lower() != ".vcj":
        out = out.with_suffix(".vcj")

    url = f"{args.url.rstrip('/')}/download/device/{serial}"
    headers = {"Accept": "application/voucher-cms+json,application/octet-stream,*/*"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    print("=" * 60)
    print("MASA Existing Voucher Download")
    print("=" * 60)
    print(f"Serial: {serial}")
    print(f"URL: {url}")

    try:
        if cert_path and key_path:
            resp = requests.get(url, headers=headers, cert=(cert_path, key_path), timeout=30)
        else:
            resp = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(2)

    print(f"Status Code: {resp.status_code}")
    print(f"Response Headers: {dict(resp.headers)}")

    if resp.status_code not in (200, 201):
        print("Download failed")
        text = (resp.text or "").strip()
        if text:
            print(f"Response: {text[:600]}")
        try:
            err = resp.json()
            if isinstance(err, dict):
                error_obj = err.get("error", {}) if isinstance(err.get("error"), dict) else {}
                msg = error_obj.get("msg")
                info = msg.get("info") if isinstance(msg, dict) else msg
                if info:
                    print(f"API error info: {info}")
        except ValueError:
            pass
        sys.exit(3)

    try:
        voucher_bytes = extract_bytes(resp)
    except ValueError as exc:
        print(f"Could not save usable voucher content: {exc}")
        sys.exit(4)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(voucher_bytes)
    print(f"Saved VCJ voucher to: {out}")


if __name__ == "__main__":
    main()
