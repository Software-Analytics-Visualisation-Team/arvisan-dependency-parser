import json

node_header = (
    "id:ID",
    ":LABEL",
    "fullName",
    "simpleName",
    "color",
    "nodeProperties",
)
edge_header = (
    "id",
    ":TYPE",
    ":START_ID",
    ":END_ID",
    "references",
    "dependencyTypes",
    "nrDependencies:INT",
    "nrCalls:INT",
)

def create_node(
    node_id: str,
    label: str,
    full_name: str,
    simple_name: str,
    color: str,
    nodeProperties = {},
) -> tuple:
    return (node_id, label, full_name, simple_name, color, nodeProperties)


def create_edge(
    edge_source: str, edge_target: str, edge_label: str, properties=None
) -> tuple:
    return (
        f"{edge_source}-{edge_label}-{edge_target}",
        edge_label,
        edge_source,
        edge_target,
        "{}",
        None,
        None,
        None,
    )


def create_domain_node(simple_name, color="#666666"):
    return create_node(
        node_id="domain_node",
        label="Domain",
        full_name="domain_node",
        simple_name=simple_name,
        color=color,
    )


def create_application_node(node_id, simple_name, label="Subsystem Group", color="#065F46"):
    return create_node(
        node_id=node_id,
        label=label,
        full_name=node_id,
        simple_name=simple_name,
        color=color,
    )


def create_sublayer_node(node_id, simple_name, label="Subsystem", color="#10B981"):
    return create_node(
        node_id=node_id,
        label=label,
        full_name=node_id,
        simple_name=simple_name,
        color=color,
    )


def create_module_node(node_id, simple_name, label="Module", color="#6EE7B7", node_properties = None):
    return create_node(
        node_id=node_id,
        label=label,
        full_name=node_id,
        simple_name=simple_name,
        color=color,
        nodeProperties=json.dumps(node_properties),
    )

def update_node_color(nodes, node_id, color):
    node = nodes.get(node_id, None)
    if node:
        node = list(node)
        node[4] = color  # Update color
        nodes[node_id] = tuple(node)

    return nodes