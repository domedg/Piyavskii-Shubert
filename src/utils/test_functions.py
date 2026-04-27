import json
import numpy as np
from pathlib import Path

def build_test_functions():
    # Calcola il path in modo dinamico e portabile rispetto alla root del progetto
    # __file__ punta a src/utils/test_functions.py
    # .parent.parent.parent punta alla cartella root del progetto
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / "data" / "funzioni_config.json"

    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    test_functions = {}
    for func_id, func_data in config.items():
        # Pre-compila l'espressione in formato numpy per massima performance
        # includendo np per permettere a eval di trovare numpy ops.
        expr_str = func_data["formato_np"]
        compiled_expr = compile(expr_str, '<string>', 'eval')
        
        # Chiudiamo in uno scope il current_expr
        def create_eval_func(expr_code):
            return lambda x: eval(expr_code, {"np": np, "sum": sum, "range": range, "x": x})

        test_functions[func_id] = {
            "func": create_eval_func(compiled_expr),
            "a": func_data["intervallo"][0],
            "b": func_data["intervallo"][1],
            "L": func_data["L"],
            "latex": func_data.get("latex", "")
        }
    return test_functions

TEST_FUNCTIONS = build_test_functions()
