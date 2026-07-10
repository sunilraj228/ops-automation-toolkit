import argparse
import logging
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

PATTERNS = {
    r"connection refused": {
        "severity": "Critical",
        "cause": "Target service is unreachable.",
        "recommendation": "Verify service status, firewall rules, and network connectivity."
    },
    r"timeout": {
        "severity": "High",
        "cause": "Operation exceeded timeout.",
        "recommendation": "Check latency and backend performance."
    },
    r"permission denied": {
        "severity": "High",
        "cause": "Insufficient permissions.",
        "recommendation": "Review filesystem permissions or IAM/RBAC roles."
    },
    r"authentication failed": {
        "severity": "Medium",
        "cause": "Invalid credentials.",
        "recommendation": "Verify username, password, API key, or token."
    },
    r"ssl": {
        "severity": "High",
        "cause": "SSL/TLS issue detected.",
        "recommendation": "Validate certificate expiry and trust chain."
    },
    r"disk full": {
        "severity": "Critical",
        "cause": "Storage capacity exhausted.",
        "recommendation": "Clean up storage or increase disk capacity."
    }
}


class LogAnalyzer:

    def __init__(self, logfile):
        self.logfile = Path(logfile)
        self.errors = []

    def load(self):

        if not self.logfile.exists():
            raise FileNotFoundError(self.logfile)

        logging.info("Loading log file...")
        return self.logfile.read_text(encoding="utf-8").splitlines()

    def extract(self, lines):

        regex = re.compile(r"(ERROR|WARNING).+", re.IGNORECASE)

        for line in lines:
            match = regex.search(line)

            if match:
                self.errors.append(match.group())

    def classify(self, message):

        lower = message.lower()

        for pattern, details in PATTERNS.items():

            if re.search(pattern, lower):
                return details

        return {
            "severity": "Unknown",
            "cause": "Pattern not recognised.",
            "recommendation": "Manual investigation required."
        }

    def display(self):

        counter = Counter(self.errors)

        table = Table(title="Log Analysis Summary")

        table.add_column("Occurrences", justify="center")
        table.add_column("Message")

        for msg, count in counter.items():
            table.add_row(str(count), msg)

        console.print(table)

    def markdown_report(self):

        report = []

        report.append("# AI Log Analysis Report\n")
        report.append(f"Generated: {datetime.now()}\n")

        counter = Counter(self.errors)

        report.append(f"Unique Issues: {len(counter)}\n")

        for message, count in counter.items():

            result = self.classify(message)

            report.append("---")

            report.append(f"## {message}")

            report.append(f"- Occurrences: **{count}**")
            report.append(f"- Severity: **{result['severity']}**")
            report.append(f"- Root Cause: {result['cause']}")
            report.append(
                f"- Recommendation: {result['recommendation']}\n"
            )

        return "\n".join(report)

    def save_report(self):

        reports = Path("reports")
        reports.mkdir(exist_ok=True)

        filename = reports / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        filename.write_text(
            self.markdown_report(),
            encoding="utf-8"
        )

        return filename


def main():

    parser = argparse.ArgumentParser(
        description="AI Log Analyzer"
    )

    parser.add_argument(
        "-f",
        "--file",
        default="application.log",
        help="Path to log file"
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer(args.file)

    try:

        lines = analyzer.load()

        analyzer.extract(lines)

        if not analyzer.errors:
            console.print("[green]No warnings or errors found.[/green]")
            return

        analyzer.display()

        report = analyzer.save_report()

        console.print(
            f"\n[bold green]Report generated:[/bold green] {report}"
        )

    except Exception as exc:

        console.print(f"[red]{exc}[/red]")


if __name__ == "__main__":
    main()
