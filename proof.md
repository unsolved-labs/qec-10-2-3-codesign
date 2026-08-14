# Exact four-layer check minimum for direct [[10,2,3]] syndrome extraction

## Frozen claim

Consider the CSS `[[10,2,3]]` rotated-toric code on data qubits `0..9` with independent stabilizers

### Z checks

- `Z0 = {0,1,3,4}`
- `Z1 = {2,3,5,6}`
- `Z2 = {4,5,7,8}`
- `Z3 = {0,6,7,9}`

### X checks

- `X0 = {0,2,3,9}`
- `X1 = {1,2,4,5}`
- `X2 = {3,4,6,7}`
- `X3 = {5,6,8,9}`

We restrict to the following architecture.

1. Every measured check is a nonidentity pure-X or pure-Z stabilizer of this code.
2. Every measured stabilizer has its own ancilla. A Z check is measured by one data-to-ancilla CNOT for every data qubit in its support; an X check by one ancilla-to-data CNOT for every data qubit in its support.
3. All CNOTs in one syndrome round must fit in exactly four sequential conflict-free CNOT layers. A physical qubit participates in at most one CNOT per layer.
4. The measured Z checks span the rank-4 Z stabilizer space and the measured X checks span the rank-4 X stabilizer space. Repeated stabilizer measurements are allowed in the lower-bound search.
5. The same schedule is repeated for three rounds. Check ancillas are perfectly reset between rounds, and a perfect terminal data syndrome closes the detector history.
6. At first order, an arbitrary nonidentity two-qubit Pauli may occur immediately after any one CNOT. A circuit passes the CNOT-fault distinguishability criterion when the complete detector syndrome uniquely determines the resulting logical Pauli class for every such single fault. An undetected nontrivial logical fault also fails the criterion.

**Theorem.** In this frozen architecture, the minimum number of measured stabilizers—and hence dedicated check ancillas—per syndrome round that can satisfy the criterion is exactly **10**. Therefore the minimum total qubit count in this architecture is **20 = 10 data + 10 check ancillas**.

The released 10-check witness also remains unambiguous after adding a single binary preparation flip or measurement flip on any check ancilla. The theorem does not claim fault tolerance against arbitrary circuit faults outside the frozen model.

## Proof

### 1. Code parameters and available four-layer checks

Exact GF(2) elimination gives rank four for both the X and Z independent stabilizer matrices, so the code encodes

`k = 10 - 4 - 4 = 2`

logical qubits. Exhaustive normalizer enumeration gives distance three in both CSS sectors.

Each nonzero X or Z stabilizer row space has 15 elements. Their exact weight distribution is

- five weight-4 stabilizers;
- ten weight-6 stabilizers.

The fifth weight-4 stabilizer in each sector is the product of all four displayed independent generators:

- `ZR = {1,2,8,9}`;
- `XR = {0,1,7,8}`.

A direct measurement of a weight-w check needs `w` CNOTs incident on its dedicated ancilla. Since an ancilla can take part in at most one CNOT in each of four layers, every measured stabilizer in the frozen architecture has weight at most four. Hence the five weight-4 stabilizers above are the **only** available checks in each CSS sector.

Every four-element subset of the five weight-4 checks has GF(2) rank four.

### 2. Fewer than eight measured checks are impossible

The measured Z checks must span a rank-4 space and the measured X checks must span a rank-4 space. At least four checks of each type are therefore necessary. Thus at least eight checks are required before scheduling or fault propagation is considered.

### 3. Eight checks are impossible

With exactly eight measured checks there must be four X and four Z checks. Rank four forces the four checks in each sector to be distinct. Therefore there are exactly

`C(5,4) * C(5,4) = 25`

possible check architectures.

For each architecture the verifier exhaustively enumerates every four-layer schedule satisfying both:

- the per-qubit conflict constraint; and
- exact simultaneous measurement of the intended commuting stabilizers.

Across the 25 architectures there are exactly **740** ideal four-layer schedules.

For every one of the 740 schedules, `verify_release.py` exhaustively scans the single-CNOT fault mechanisms until it finds either:

- one single CNOT fault with zero detector syndrome and nonzero logical class; or
- two single CNOT faults with the same detector syndrome and different logical classes.

All 740 schedules therefore fail the first-order CNOT-fault distinguishability criterion.

### 4. Nine checks are impossible, including repeated-check architectures

With nine measured checks the type count must be `5+4`.

The lower-bound enumeration permits repeated stabilizers. Among multisets of five chosen from the five available weight-4 checks, exactly **21** have GF(2) rank four. Thus, including both X-heavy and Z-heavy orientations and all five choices of the four-check basis on the other side, there are

`21 * 5 * 2 = 210`

rank-valid nine-check architectures.

Of these, **200** contain a repeated stabilizer. Direct degree counting shows that every one of these architectures has at least one data qubit incident on five or more required CNOTs. Such an architecture cannot fit in four conflict-free CNOT layers.

The remaining **10** architectures use all five distinct weight-4 stabilizers on one side and four of five on the other. They have exactly **160** ideal four-layer schedules in total—16 per architecture.

The verifier exhaustively finds a single-fault logical ambiguity in every one of those 160 schedules. Thus no nine-check architecture passes.

### 5. Ten checks are sufficient

Measure all five weight-4 stabilizers in each CSS sector. The released witness uses four layers:

| Layer | CNOTs |
|---|---|
| 0 | `q1→Z0, q3→Z1, q5→Z2, q7→Z3, q9→ZR, X0→q0, X1→q2, X2→q4, X3→q6, XR→q8` |
| 1 | `q0→Z0, q2→Z1, q4→Z2, q6→Z3, q8→ZR, X0→q9, X1→q1, X2→q3, X3→q5, XR→q7` |
| 2 | `q4→Z0, q6→Z1, q8→Z2, q0→Z3, q2→ZR, X0→q3, X1→q5, X2→q7, X3→q9, XR→q1` |
| 3 | `q3→Z0, q5→Z1, q7→Z2, q9→Z3, q1→ZR, X0→q2, X1→q4, X2→q6, X3→q8, XR→q0` |

Every one of the 20 physical qubits participates in exactly one CNOT in every layer.

The verifier back-propagates measurement Paulis and checks exact ideal measurement of all ten intended stabilizers. It then exhaustively propagates all

`3 rounds * 40 CNOTs/round * 15 nonidentity two-qubit Paulis = 1,800`

single-CNOT fault mechanisms. No detector syndrome is shared by different logical classes, and no nontrivial logical fault is undetected.

The verifier additionally checks 60 binary check-ancilla preparation/measurement fault mechanisms; none introduces a first-order logical ambiguity.

Hence ten measured checks are sufficient. Combined with the eight- and nine-check exclusions, the exact minimum is ten. ∎

## What the theorem does not say

This is an exact optimization result inside a deliberately frozen circuit class. It does **not** prove that 20 qubits are necessary for arbitrary fault-tolerant extraction of the `[[10,2,3]]` code. In particular, it does not exclude:

- flag-qubit or flag-sharing circuits;
- cat-state or Steane/Knill extraction;
- adaptive circuits;
- more than four CNOT layers;
- subsystem/gauge measurements;
- ancilla reuse across non-simultaneous checks;
- mid-circuit feed-forward;
- alternative detector constructions;
- arbitrary routing or hardware-specific primitives.

No logical-error-rate, threshold, ASIC-like, or hardware superiority claim is part of this release.
