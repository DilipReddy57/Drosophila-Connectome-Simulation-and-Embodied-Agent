import pytest

from connectome_sim.schema import NetworkSchema, Neuron, SchemaConnection, validate_network


def sample_network():
    return NetworkSchema(
        neurons=(Neuron(42, "acetylcholine"), Neuron(7, "gaba"), Neuron(99, "dopamine"), Neuron(15, "glutamate")),
        connections=(SchemaConnection(42, 7, 1.0), SchemaConnection(7, 99, -1.0)),
    )


@pytest.mark.parametrize(
    ("network", "message"),
    [
        (NetworkSchema((Neuron(1, "gaba"), Neuron(1, "gaba")), ()), "unique"),
        (NetworkSchema((Neuron(1, "unknown"),), ()), "unsupported"),
        (NetworkSchema((Neuron(1, "gaba"),), (SchemaConnection(1, 2, 1),)), "unknown"),
        (NetworkSchema((Neuron(1, "gaba"),), (SchemaConnection(1, 1, 1),)), "self"),
        (NetworkSchema((Neuron(1, "gaba"), Neuron(2, "gaba")), (SchemaConnection(1, 2, 1), SchemaConnection(1, 2, 2))), "duplicate"),
    ],
)
def test_schema_rejects_invalid_nodes_and_edges(network, message):
    with pytest.raises(ValueError, match=message):
        validate_network(network)


def test_mapping_degrees_isolates_and_transmitter_distribution():
    network = sample_network()
    validate_network(network)
    assert network.id_mapping() == {42: 0, 7: 1, 99: 2, 15: 3}
    assert network.degree_distributions() == ({42: 0, 7: 1, 99: 1, 15: 0}, {42: 1, 7: 1, 99: 0, 15: 0})
    assert network.isolated_node_ids() == {15}
    assert network.neurotransmitter_distribution() == {"acetylcholine": 1, "gaba": 1, "dopamine": 1, "glutamate": 1}
