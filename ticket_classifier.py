import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

RULES = {
    "login": ("Authentication", "High", "Support"),
    "password": ("Authentication", "High", "Support"),
    "database": ("Database", "Critical", "Database Team"),
    "timeout": ("Performance", "High", "Backend Team"),
    "500": ("Backend", "Critical", "Backend Team"),
    "api": ("API", "High", "API Team"),
    "kubernetes": ("Infrastructure", "Critical", "DevOps"),
    "pod": ("Infrastructure", "Critical", "DevOps"),
    "ssl": ("Security", "Critical", "Security Team"),
    "certificate": ("Security", "Critical", "Security Team"),
    "slow": ("Performance", "Medium", "Performance Team"),
    "feature": ("Feature Request", "Low", "Product Team"),
    "payment": ("Payments", "Critical", "Payments Team")
}


class TicketClassifier:

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.df = None

    def load(self):
        if not self.file_path.exists():
            raise FileNotFoundError("tickets.csv not found")

        self.df = pd.read_csv(self.file_path)

    def classify(self):

        categories = []
        priorities = []
        teams = []

        for issue in self.df["Issue"]:

            issue_lower = issue.lower()

            category = "General"

            priority = "Medium"

            team = "Support"

            for keyword, values in RULES.items():

                if keyword in issue_lower:

                    category, priority, team = values

                    break

            categories.append(category)
            priorities.append(priority)
            teams.append(team)

        self.df["Category"] = categories
        self.df["Priority"] = priorities
        self.df["Assigned Team"] = teams

    def display(self):

        table = Table(title="Support Ticket Classification")

        columns = [
            "Ticket ID",
            "Category",
            "Priority",
            "Assigned Team"
        ]

        for col in columns:
            table.add_column(col)

        for _, row in self.df.iterrows():

            table.add_row(
                str(row["Ticket ID"]),
                row["Category"],
                row["Priority"],
                row["Assigned Team"]
            )

        console.print(table)

    def summary(self):

        console.print("\nCategory Summary\n")

        print(self.df["Category"].value_counts())

        console.print("\nPriority Summary\n")

        print(self.df["Priority"].value_counts())

    def export(self):

        reports = Path("reports")
        reports.mkdir(exist_ok=True)

        filename = reports / "classified_tickets.csv"

        self.df.to_csv(filename, index=False)

        console.print(f"\nReport saved -> {filename}")


def main():

    classifier = TicketClassifier("tickets.csv")

    classifier.load()

    classifier.classify()

    classifier.display()

    classifier.summary()

    classifier.export()


if __name__ == "__main__":
    main()
