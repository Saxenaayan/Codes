import uuid
import asyncio

class GraphEngine:
    def __init__(self):
        self.graphs = {}
        self.runs = {}

    def create_graph(self, nodes, edges, start_node):
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = {
            "nodes": nodes,
            "edges": edges,
            "start_node": start_node
        }
        return graph_id

    async def run_graph(self, graph_id, state):
        run_id = str(uuid.uuid4())
        graph = self.graphs[graph_id]
        node_map = graph["nodes"]
        edges = graph["edges"]

        current_node = graph["start_node"]
        execution_log = []

        while current_node:
            node_fn = node_map[current_node]
            result = await node_fn(state)

            execution_log.append({
                "node": current_node,
                "state": state.data.copy(),
                "result": result
            })

            if result == "STOP":
                break

            if isinstance(result, dict) and "next" in result:
                current_node = result["next"]
            else:
                current_node = edges.get(current_node)

        self.runs[run_id] = {"state": state.data, "log": execution_log}
        print("RUNS DICT NOW:", self.runs.keys())

        return run_id, state.data, execution_log

    def get_state(self, run_id):
        return self.runs.get(run_id, {})
