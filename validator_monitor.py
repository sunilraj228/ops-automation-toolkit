import json
import time
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table

console = Console()


class ValidatorMonitor:

    def __init__(self, config_file):
        self.config = config_file
        self.validators = []

    def load(self):

        if not Path(self.config).exists():
            raise FileNotFoundError(self.config)

        with open(self.config, "r") as f:
            self.validators = json.load(f)

    def rpc_call(self, url):

        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }

        start = time.time()

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=5
            )

            latency = round((time.time() - start) * 1000)

            response.raise_for_status()

            block = int(
                response.json()["result"],
                16
            )

            return {
                "status": "Healthy",
                "block": block,
                "latency": latency
            }

        except Exception:

            return {
                "status": "Offline",
                "block": "-",
                "latency": "-"
            }

    def check_all(self):

        table = Table(
            title="Blockchain Validator Monitor"
        )

        table.add_column("Validator")
        table.add_column("Status")
        table.add_column("Latest Block")
        table.add_column("Latency (ms)")

        report = []

        for validator in self.validators:

            result = self.rpc_call(
                validator["rpc"]
            )

            table.add_row(
                validator["name"],
                result["status"],
                str(result["block"]),
                str(result["latency"])
            )

            report.append({
                "validator": validator["name"],
                **result
            })

        console.print(table)

        self.save(report)

    def save(self, report):

        Path("reports").mkdir(
            exist_ok=True
        )

        filename = (
            Path("reports") /
            "validator_report.json"
        )

        with open(filename, "w") as f:
            json.dump(
                report,
                f,
                indent=4
            )

        console.print(
            f"\nReport saved to {filename}"
        )


def main():

    monitor = ValidatorMonitor(
        "validators.json"
    )

    monitor.load()

    monitor.check_all()


if __name__ == "__main__":
    main()
