# Reference Dataset Identity

## Shiu et al. (2024) Dataset Version
The official repository `philshiu/Drosophila_brain_model` explicitly hardcodes the dataset version to **FlyWire FAFB v630**.

### Evidence
In `example.ipynb` (Cell 2), the configuration block dictates the exact input dataset paths:
```python
config = {
    'path_res'  : './results/example',                              
    'path_comp' : './2023_03_23_completeness_630_final.csv',        
    'path_con'  : './2023_03_23_connectivity_630_final.parquet',    
    'n_proc'    : -1,                                               
}
```
The filename `630` directly corresponds to FlyWire materialization v630 (March 23, 2023 release).

## Reference Neurons
The 21 sugar-sensing neurons (`neu_sugar`) and the motor neuron (`MN9`) are defined as explicitly hardcoded integers in `example.ipynb`. 
- `neu_sugar` IDs are listed in Cell 3 of `example.ipynb`.
- MN9 is listed as `id_mn9 = 720575940660219265` in Cell 15 of `example.ipynb`.

These are verified FlyWire **Root IDs** because `model.py` and `utils.py` utilize these 64-bit integers as keys against the `completeness` and `connectivity` tables, which strictly use FlyWire Root IDs as primary keys. They are immutable for v630, but obsolete in later materializations (e.g. v783).
