#!/usr/bin/env python3
"""LoomQ submission adapter contract v1.0.

This file intentionally contains no scoring implementation. Teams may implement
the functions directly or delegate to another language/runtime with subprocess.
"""

from typing import Any, Dict, List, Tuple

try:
    from .backend.braket import run_braket
    from .emitters.braket import emit_braket
    from .parser import parse_qasm
except ImportError:
    from backend.braket import run_braket
    from emitters.braket import emit_braket
    from parser import parse_qasm

SUPPORTED_TARGETS = ("spinq", "originq", "braket")


def transpile(qasm_str: str, target: str) -> str:
    circuit = parse_qasm(qasm_str)
    if target == "spinq":
        return qasm_str
    elif target == "originq":
        return qasm_str
    elif target == "braket":
        return emit_braket(
            circuit,
            include_stdlib=True,
        )

    raise NotImplementedError(
        f"{target} is not implemented"
    )


def run(
    qasm_str: str,
    target: str,
    shots: int,
) -> Dict[str, Any]:
    if target == "braket":
        circuit = parse_qasm(qasm_str)

        qasm3 = emit_braket(
            circuit,
            include_stdlib=False,
        )

        measurement_map = {
            measurement.qubit: measurement.bit
            for measurement in circuit.measurements
        }

        return run_braket(
            qasm3,
            shots=shots,
            measurement_map=measurement_map,
            num_bits=circuit.num_bits,
        )

    raise NotImplementedError(
        f"{target} backend is not implemented"
    )


def agent_chat(prompt: str) -> str:
    """Optional L2 entry point using the documented LOOMQ_LLM_* environment."""
    raise NotImplementedError("L2 is optional; implement agent_chat(prompt) to enter")


def compile_hybrid(hybrid_qasm_str: str) -> Tuple[List[str], str]:
    """Optional L3 entry point. Return quantum operations and RISC-V assembly."""
    raise NotImplementedError(
        "L3 is optional; implement compile_hybrid(hybrid_qasm_str) to enter"
    )
