from typing import Protocol


class SupportsComputeResults(Protocol):
    def compute_results(self, data):
        ...
