#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry.

Copies the shipped entry.png (a 1024x1024 PNG front page summing up
Friday 20 November 2026) to the grader's output path.  Standard library
only, no network, fully deterministic: the same bytes come out every run.
"""
import hashlib
import os
import struct
import sys


def _here():
    return os.path.dirname(os.path.abspath(__file__))


def _read_png(path):
    with open(path, "rb") as fh:
        return fh.read()


def _check_png(blob):
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if blob[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError("entry.png is %dx%d, expected 1024x1024"
                         % (width, height))
    if len(blob) > 1048576:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap"
                         % len(blob))
    return width, height


def _write_out(blob, dest):
    parent = os.path.dirname(os.path.abspath(dest))
    os.makedirs(parent, exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(blob)
    with open(dest, "rb") as fh:
        back = fh.read()
    if len(back) != len(blob):
        raise ValueError("wrote %d bytes, expected %d"
                         % (len(back), len(blob)))
    if hashlib.sha256(back).hexdigest() != hashlib.sha256(blob).hexdigest():
        raise ValueError("written copy does not match the shipped bytes")
    return back


def main(argv):
    src = os.path.join(_here(), "entry.png")
    blob = _read_png(src)
    _check_png(blob)
    dest = argv[1] if len(argv) > 1 else "/output/entry.png"
    out = _write_out(blob, dest)
    digest = hashlib.sha256(out).hexdigest()
    print("entry.png: %d bytes, sha256 %s -> %s" % (len(out), digest, dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
