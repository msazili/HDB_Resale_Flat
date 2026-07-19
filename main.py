import logging
import sys

from src.pipeline import HDBDataPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    print("Hello from hdb-resale-flat!")


if __name__ == "__main__":
    pipeline = HDBDataPipeline()
    results = pipeline.run()

