from fseg.impl._fseg import Algorithm, SPACalculator

registered_algorithms = {
    "SPA": SPACalculator,
}

__all__ = [
    "Algorithm",
    "registered_algorithms",
]
