"""
Adapter contracts for real automation.

The Executor intentionally does not pretend that a generator/vision model is connected.

Implement these two functions against the provider you actually use.
"""

class GeneratorAdapter:
    def generate_one(self, *, prompt: str, source_path: str, reference_paths: dict, output_path: str):
        """Must create exactly ONE image at output_path."""
        raise NotImplementedError("Connect your image-generation provider here.")

class VisionQAAdapter:
    def review_one(self, *, task: dict, source_path: str, output_path: str, reference_paths: dict) -> dict:
        """
        Return:
        {"checks": {
          "output_isolation": True,
          "presence_map": True,
          "semantic_function": True,
          "product_identity": True,
          "product_geometry": True,
          "product_fit": True,
          "hand_anatomy": True,
          "clothing_identity": True,
          "creative_delta_ge_2": True
        }}
        """
        raise NotImplementedError("Connect a vision-capable QA provider here.")
