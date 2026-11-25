"""Alien Field Notes: The Two Day Earth Review.

Writes one line of alien field notes reviewing Earth after a two-day
visit to /output/entry.txt: an outsider's observations, a verdict and
a rating, with the punch at the end. The rules ban the tired topics
(traffic, gravity, money, weather), so the notes stick to what the
locals actually do.

Standard library only; deterministic: the same bytes on every run.
"""

import hashlib
import os

ENTRY = (
    "Field notes, day two: the locals apologize to furniture, worship "
    "a glowing rectangle, and rate everything out of five. Verdict: "
    "charming chaos, 4.6/5 \u2014 would abduct again."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200
BANNED = ("traffic", "gravity", "money", "weather")


def validate_entry(text):
    """Check the entry against the competition gate: 1-200 UTF-8
    characters, a single non-blank line, no banned topics, and it
    must carry a verdict and a rating."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    lowered = text.lower()
    for word in BANNED:
        if word in lowered:
            raise ValueError("entry uses a banned topic: %s" % word)
    if "verdict" not in lowered:
        raise ValueError("entry must carry a verdict")
    if "/5" not in text:
        raise ValueError("entry must carry a rating out of five")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def output_path():
    """Entry destination: $MAKEFUN_OUTPUT_DIR/entry.txt, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return OUTPUT_PATH


def verify_written_bytes(written, intended):
    """Byte-exact read-back verification: same byte length (no
    trailing newline may sneak in), same bytes, same sha256 digest,
    and the decoded text still passes the gate."""
    if len(written) != len(intended):
        raise ValueError("read-back byte length mismatch")
    if written != intended:
        raise ValueError("read-back mismatch: entry.txt differs")
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise ValueError("read-back digest mismatch")
    validate_entry(written.decode("utf-8"))


def main():
    validate_entry(ENTRY)
    path = output_path()
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    with open(path, "rb") as handle:
        written = handle.read()
    verify_written_bytes(written, ENTRY.encode("utf-8"))
    print("wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()
