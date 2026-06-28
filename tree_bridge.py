import ctypes
import os
import sys

class TreeBridge:
    def __init__(self):
        if not os.path.exists("./libtree.so") and not os.path.exists("./libtree.dll"):
            if sys.platform.startswith("win"):
                os.system("gcc -shared -o libtree.dll context_bst.c")
                lib_path = "./libtree.dll"
            else:
                os.system("gcc -shared -fPIC -o libtree.so context_bst.c")
                lib_path = "./libtree.so"
        else:
            lib_path = "./libtree.dll" if sys.platform.startswith("win") else "./libtree.so"

        self.lib = ctypes.CDLL(lib_path)
        self.lib.insert_context_node.restype = ctypes.c_void_p
        self.lib.insert_context_node.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
        self.lib.gather_high_intent_context.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
        self.lib.clear_context_tree.argtypes = [ctypes.c_void_p]
        
        self.root_ptr = None

    def add_memory(self, alert_level: int, telemetry_text: str):
        self.root_ptr = self.lib.insert_context_node(self.root_ptr, alert_level, telemetry_text.encode('utf-8'))

    def compile_rag_prompt_context(self, threshold: int) -> str:
        buffer = ctypes.create_string_buffer(4096)
        self.lib.gather_high_intent_context(self.root_ptr, threshold, buffer)
        return buffer.value.decode('utf-8')

    def __del__(self):
        if hasattr(self, 'lib') and self.root_ptr:
            self.lib.clear_context_tree(self.root_ptr)
