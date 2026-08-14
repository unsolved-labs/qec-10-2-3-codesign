# Exact four-layer syndrome-extraction minimum for the [[10,2,3]] code

An exact, architecture-specific optimization result for direct CSS syndrome extraction on the known `[[10,2,3]]` rotated-toric code.

## Result

Within the frozen architecture in [`proof.md`](proof.md), the minimum number of directly measured stabilizers required for a four-CNOT-layer schedule whose detector history distinguishes every single CNOT Pauli fault by logical class is exactly:

**10 measured checks = 10 dedicated check ancillas.**

With 10 data qubits, this gives an exact minimum of **20 physical qubits inside this architecture**.

The lower bound is exhaustive:

- all 25 rank-valid 8-check architectures;
- all 740 ideal four-layer schedules across them;
- all 210 rank-valid 9-check multiset architectures, including repeated checks;
- 200 repeated-check architectures excluded by an exact per-data degree bound;
- all 160 ideal schedules in the 10 remaining nine-check architectures;
- an explicit single-fault logical collision for every one of the 900 ideal 8/9-check schedules.

The 10-check witness is exhaustively checked against all 1,800 single-CNOT nonidentity Pauli mechanisms over three rounds, plus binary check-ancilla preparation and measurement flips.

## Reproduce

Python 3.11+; standard library only.

```bash
python verify_release.py
```

The verifier rederives the code parameters and stabilizer weight spectrum, re-enumerates the complete lower-bound architecture/schedule space, independently finds a single-fault logical ambiguity in every 8/9-check schedule, and exhaustively checks the 10-check witness.

Machine-readable expected output is in [`verification-report.json`](verification-report.json).

## Files

- [`proof.md`](proof.md) — frozen theorem, proof, architecture, fault model, and limitations
- [`verify_release.py`](verify_release.py) — self-contained exact verifier
- [`verification-report.json`](verification-report.json) — machine-readable replay result
- [`witness-schedule.json`](witness-schedule.json) — machine-readable 10-check schedule
- [`NOVELTY.md`](NOVELTY.md) — scoped prior-art and novelty audit

## Status

- Exact self-contained replay: **pass**
- External specialist review: **pending**
- Hardware-performance claim: **none**
- Code novelty claim: **none** — the `[[10,2,3]]` code is known

The claim is the exact minimum for the explicitly frozen direct-measurement circuit class, not a general minimum for fault-tolerant QEC.
