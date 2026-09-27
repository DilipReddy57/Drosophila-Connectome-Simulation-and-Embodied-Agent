import polars as pl
from pathlib import Path

neurons = pl.read_parquet('data/derived/final_v1/neurons.parquet')
connections = pl.read_parquet('data/derived/final_v1/connections.parquet')

print(f'neurons = {neurons.height}')
print(f'connection rows = {connections.height}')
print(f'synapses = {connections["synapse_count"].sum()}')
print(f'self edges = {connections.filter(pl.col("pre_neuron_id") == pl.col("post_neuron_id")).height}')

valid_pres = connections.join(neurons, left_on="pre_neuron_id", right_on="neuron_id", how="anti").height
valid_posts = connections.join(neurons, left_on="post_neuron_id", right_on="neuron_id", how="anti").height
print(f'invalid endpoints = {valid_pres + valid_posts}')
print(f'duplicate canonical groups = {connections.select(["pre_neuron_id", "post_neuron_id", "region"]).is_duplicated().sum()}')
print(f'duplicate root IDs = {neurons.select(["neuron_id"]).is_duplicated().sum()}')
print(f'duplicate dense IDs = {neurons.select(["dense_index"]).is_duplicated().sum()}')
print(f'dense ID min = {neurons["dense_index"].min()}')
print(f'dense ID max = {neurons["dense_index"].max()}')
print(f'missing dense IDs = {neurons.filter(pl.col("dense_index").is_null()).height}')

nulls = {}
for col in neurons.columns: nulls[col] = neurons.filter(pl.col(col).is_null()).height
for col in connections.columns: nulls[col] = connections.filter(pl.col(col).is_null()).height
print(f'null columns = {nulls}')

print(f'unknown regions = {connections.filter((pl.col("region") == "unknown") | (pl.col("region") == "Unknown")).height}')
print(f'unknown NT = {connections.filter((pl.col("source_nt_type") == "unknown") | (pl.col("source_nt_type") == "Unknown")).height}')

annotation_cols = ["cell_type", "super_class", "class", "subclass", "hemilineage"]
is_annotated = neurons.select(pl.any_horizontal([pl.col(c).is_not_null() & (pl.col(c) != "unknown") & (pl.col(c) != "Unknown") & (pl.col(c) != "") for c in annotation_cols])).to_series()
print(f'cell-type annotation coverage = {is_annotated.sum()}/{neurons.height}')
