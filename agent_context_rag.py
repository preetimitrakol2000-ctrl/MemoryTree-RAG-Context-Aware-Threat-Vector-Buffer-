from tree_bridge import TreeBridge

class AgentMemoryRAG:
    def __init__(self):
        self.memory_engine = TreeBridge()

    def load_incident_stream(self):
        # Insert security telemetry elements sorted into memory trees based on explicit critical scores
        self.memory_engine.add_memory(85, "Critical threat: Unauthorized extraction trace discovered on host DB.")
        self.memory_engine.add_memory(40, "Minor warning: Ping scan detected from peripheral router interface.")
        self.memory_engine.add_memory(95, "Immediate Alert: Superuser password mutation confirmed from unmapped external IP.")

    def run_augmented_generation_loop(self) -> str:
        # Extract and bundle high-priority system events into a single prompt context window
        retrieved_facts = self.memory_engine.compile_rag_prompt_context(threshold=70)
        
        prompt = (
            f"=== SECURITY AI CONTEXT WINDOW ===\n"
            f"RETRIEVED TREE STATE MEMORIES: {retrieved_facts}\n"
            f"-----------------------------------------------------------------\n"
            f"[SYSTEM ACTION STATEMENT]: Isolate current network interfaces and revoke all tokens immediately."
        )
        return prompt

if __name__ == "__main__":
    rag_system = AgentMemoryRAG()
    rag_system.load_incident_stream()
    print(rag_system.run_augmented_generation_loop())
