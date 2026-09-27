# Connectome Adapter Forensics

## Independent Accounting Test Results
- **C1 Neuron Count:** 139,255
- **C3 Neuron Count:** 139,255
- **C1 Canonical Connection Rows (no self-loops):** 5,342,446
- **C3 Imported Rows:** 5,342,446
- **C1 Total Synapses (no self-loops):** 50,666,648
- **C3 Total Imported Synapses:** 50,666,648

## Topological Integrity Check
1. **Self loops:** The C1 dataset has 56,231 self-loop rows. The adapter explicitly filters these out via `connections['pre_dense_index'] != connections['post_dense_index']`. Therefore, C3 imported rows perfectly match the non-self-loop count of C1.
2. **Duplicate edges:** No duplicate directed edges are created. FAFB v783 guarantees no duplicates at the regional aggregation level, and the adapter simply loads these. 
3. **Unknown endpoints:** Validated. All pre/post indices are mapped into the strict `[0, num_nodes - 1]` range, ensuring dense adjacency matrices match perfectly.
4. **Ordering changes:** The adapter enforces a deterministic sort on `[pre_dense_index, post_dense_index]` before returning arrays.

## Conclusion
The `SparseGraph` conversion from C1 to C3 is mathematically lossless (excluding intentional self-loop purges) and structurally isomorphic.

**STATUS: PASS.**
