# The Painfully Honest Out-of-Office

[![make.fun](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![Rank](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/Akhmad045/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/rank.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![Reward](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/Akhmad045/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/reward.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)

A make.fun bounty entry: one out-of-office email auto-reply of at most
200 characters, painfully honest about the sender's inbox yet polite
enough that a manager would let it stand.

Bounty: https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b

## The entry

> Thank you for your email — I am away until Monday, and honestly, the only emails I answer on my return are the ones people resend, so if this matters, please send it again then.

177 characters, one sentence. The reply admits a private truth about how
the sender really triages email on return — the resend rule — instead of
the unread-count joke most replies lean on, and it ends by giving the
sender a polite, useful next step.

## How it works

`main.py` writes the reply to `/output/entry.txt`, exactly, with no
trailing newline. Twelve candidate replies were drafted and compared
against the judge brief (honesty first, then politeness, then turn of
phrase); the pick won the internal pairwise comparison.

```sh
python3 main.py                 # write /output/entry.txt
python3 main.py --self-test     # gate + round-trip checks
```

The self-test checks the house gate (1–200 characters, one sentence, no
padding, no control characters), that all 12 candidates are distinct and
gate-clean, and that a written copy round-trips byte for byte.

## Referral

Built with make.fun — referral code `4g7knchf`.
