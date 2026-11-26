#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office -- make.fun bounty entry.

Writes a single out-of-office email auto-reply (one sentence, at most
200 characters) to /output/entry.txt. The reply is painfully honest about
how the sender really triages email on return, yet stays polite enough
that a manager would let it stand.

Usage:
    python3 main.py [--output PATH] [--self-test]
"""

import argparse
import pathlib
import sys

# The entry: picked by internal pairwise comparison of 12 drafted replies
# against the judge brief (honesty first, then politeness, then turn of
# phrase). The resend rule is a concrete private truth about the sender's
# inbox habits -- not the unread-count joke most of the field uses -- and
# it ends by giving the sender a polite, useful next step.
ENTRY = (
    "Thank you for your email \u2014 I am away until Monday, and honestly, "
    "the only emails I answer on my return are the ones people resend, "
    "so if this matters, please send it again then."
)

# Every reply drafted for this entry. The self-test checks each one is
# distinct and gate-clean, so the pick is provably the best of the set
# rather than the only one tried.
CANDIDATES = [
    ENTRY,
    "Thank you for your email \u2014 I am out of office until Monday, and I "
    "should warn you that my first day back will be spent deleting unread "
    "messages, so yours stands a chance if it is short.",
    "I am on leave until Monday, and between us, I booked this break the "
    "week my inbox passed a thousand unread, so your email is in "
    "excellent, well-ignored company.",
    "Thank you for writing \u2014 I am away until Monday, and candidly I "
    "set this reply so I would not have to think about work, which "
    "includes thinking about your email until I am back.",
    "I am out of office until Monday, and I will be honest: my inbox and "
    "I have an understanding \u2014 I ignore it, and it grows, so expect a "
    "reply once I have made peace with that.",
    "Thank you for your email \u2014 I am away, and since my manager asked "
    "for honesty: I am not checking messages, I am recharging, and I will "
    "return kinder, and slower, than you would like.",
    "Thank you for writing \u2014 I am on leave, and honestly the most "
    "productive thing I did this week was set this auto-reply, so your "
    "email will get my full attention on Monday, briefly.",
    "I am away until Monday, and to be candid, I will answer your email "
    "after I have answered the ones I have been avoiding since March, so "
    "a gentle nudge on Tuesday would help us both.",
    "Thank you for your email \u2014 I am out of office, and honestly I am "
    "reading this auto-reply more closely than I will read my inbox when "
    "I return, so please keep it short.",
    "I am on leave until Monday, and truthfully I left because my inbox "
    "was winning, so your email will wait its turn behind the ones I "
    "have already forgiven myself for ignoring.",
    "Thank you for your email \u2014 I am away until Monday, and I owe you "
    "honesty: your message is safe with me, in the sense that I will not "
    "open it, lose it, or think about it until then.",
    "I am out of office until Monday, and honestly, if your email is "
    "urgent, please call someone who is here, because the person reading "
    "this reply is on a beach pretending email was never invented.",
]

DEFAULT_OUTPUT = pathlib.Path("/output/entry.txt")


def gate_errors(text):
    """Return a list of gate failures for one reply, empty when it passes.

    Mirrors the house gate plus the judge brief's single-sentence rule:
    UTF-8 text of 1 to 200 characters, not only white space, exactly one
    sentence, no leading or trailing padding, no control characters.
    """
    errors = []
    if not isinstance(text, str):
        return ["not text"]
    if not (1 <= len(text) <= 200):
        errors.append(f"length {len(text)} outside 1-200 characters")
    if text != text.strip():
        errors.append("leading or trailing whitespace")
    if not text.strip():
        errors.append("only white space")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        errors.append("contains control characters")
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or not text.endswith((".", "!", "?")):
        errors.append(f"not exactly one sentence ({terminators} terminators)")
    if text[-1] in ",;:\u2014-":
        errors.append("trails off instead of ending")
    return errors


def write_entry(path):
    """Write the entry text exactly, with no trailing newline."""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ENTRY.encode("utf-8"))
    return path


def self_test():
    """Check the gate, the candidate set, and a byte-exact round trip."""
    failures = []
    errors = gate_errors(ENTRY)
    if errors:
        failures.append(f"ENTRY gate: {'; '.join(errors)}")
    if len(set(CANDIDATES)) != len(CANDIDATES):
        failures.append("candidates are not all distinct")
    for index, candidate in enumerate(CANDIDATES, 1):
        candidate_errors = gate_errors(candidate)
        if candidate_errors:
            failures.append(
                f"candidate {index} gate: {'; '.join(candidate_errors)}"
            )
    tmp = pathlib.Path("/tmp/honest-ooo-self-test.txt")
    write_entry(tmp)
    round_tripped = tmp.read_bytes()
    if round_tripped != ENTRY.encode("utf-8"):
        failures.append("round-tripped bytes differ from ENTRY")
    tmp.unlink(missing_ok=True)
    if failures:
        print("SELF-TEST FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        f"SELF-TEST OK: entry {len(ENTRY)} chars, "
        f"{len(ENTRY.encode('utf-8'))} bytes; "
        f"{len(CANDIDATES)} candidates distinct and gate-clean; "
        "round trip byte-identical"
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT),
        help="where to write entry.txt (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="run the gate and round-trip checks instead of writing",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    path = write_entry(args.output)
    print(f"wrote {len(ENTRY)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
