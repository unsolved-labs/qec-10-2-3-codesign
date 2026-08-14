# Novelty boundary and prior-art audit

Audit date: **2026-08-14**.

## What is not claimed as new

The `[[10,2,3]]` rotated-toric code is known. Burton, Durso-Sabina, and Brown discuss and experimentally use a `[[10,2,3]]` code in *Genons, Double Covers and Fault-tolerant Clifford Gates* (arXiv:2406.09951).

Redundant stabilizer measurements are also established prior art. Kuo and Lai develop generalized quantum data-syndrome codes and redundant stabilizer checks for syndrome-error robustness (arXiv:2310.12682).

Automated syndrome-extraction schedule optimization is established prior art, including:

- *PropHunt: Automated Optimization of Quantum Syndrome Measurement Circuits* (arXiv:2601.17580);
- *AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling Problem for QEC Codes* (arXiv:2601.12509);
- *Optimal Compilation of Syndrome Extraction Circuits for General Quantum LDPC Codes* (arXiv:2603.21499).

These works establish the broader ideas of schedule optimization, hook-error-aware extraction, exact/heuristic compilation, and redundant syndrome information. This release does not claim those ideas.

## Scoped claim audited here

The release establishes a finite exact optimization result for one frozen class:

> For the specified direct one-ancilla-per-stabilizer extraction of the known `[[10,2,3]]` CSS code, constrained to exactly four conflict-free CNOT layers and the stated three-round single-CNOT-Pauli detector model, ten measured stabilizers are necessary and sufficient for the detector syndrome to determine the logical class of every single CNOT fault.

The audit searched current primary literature for the `[[10,2,3]]` code combined with direct/bare-ancilla syndrome extraction, redundant stabilizer measurement, four-layer scheduling, and exact schedule optimization. No audited source was found that states or proves this exact minimum or exhaustively classifies the corresponding 8/9-check circuit class.

That absence claim is intentionally scoped to the sources and search terms audited. It is not a claim that every publication, thesis, code repository, or unpublished result has been examined. External specialist review remains pending.

## Primary sources checked

- Simon Burton, Elijah Durso-Sabina, Natalie C. Brown, *Genons, Double Covers and Fault-tolerant Clifford Gates*, arXiv:2406.09951.
- Kao-Yueh Kuo, Ching-Yi Lai, *Generalized quantum data-syndrome codes and belief propagation decoding for phenomenological noise*, arXiv:2310.12682.
- Joshua Viszlai et al., *PropHunt: Automated Optimization of Quantum Syndrome Measurement Circuits*, arXiv:2601.17580.
- Yuhao Liu et al., *AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling Problem for QEC Codes*, arXiv:2601.12509.
- Kai Zhang et al., *Optimal Compilation of Syndrome Extraction Circuits for General Quantum LDPC Codes*, arXiv:2603.21499.
