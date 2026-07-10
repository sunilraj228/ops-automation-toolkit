import os
import random
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

SERVICES = [
    "EC2",
    "S3",
    "Lambda",
    "RDS",
    "CloudFront",
    "Azure VM",
    "Azure Storage",
    "Azure SQL",
    "Compute Engine",
    "Cloud Storage"
]


class CloudCostDashboard:

    def __init__(self):
        self.data = pd.DataFrame()

    def generate_sample_data(self):

        rows = []

        for service in SERVICES:

            rows.append(
                {
                    "Service": service,
                    "Daily Cost ($)": round(random.uniform(5, 120), 2),
                    "Monthly Cost ($)": round(random.uniform(100, 2500), 2)
                }
            )

        self.data = pd.DataFrame(rows)

    def display_summary(self):

        print("\n========== CLOUD COST SUMMARY ==========\n")

        print(self.data)

        print("\n----------------------------------------")

        print(f"Total Daily Cost : ${self.data['Daily Cost ($)'].sum():.2f}")

        print(f"Total Monthly Cost : ${self.data['Monthly Cost ($)'].sum():.2f}")

    def highest_cost_service(self):

        row = self.data.loc[
            self.data["Monthly Cost ($)"].idxmax()
        ]

        print("\nHighest Cost Service")

        print("--------------------")

        print(row)

    def save_csv(self):

        filename = f"cloud_cost_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        self.data.to_csv(filename, index=False)

        print(f"\nCSV Report Saved -> {filename}")

    def plot_chart(self):

        plt.figure(figsize=(12,6))

        plt.bar(
            self.data["Service"],
            self.data["Monthly Cost ($)"]
        )

        plt.xticks(rotation=45)

        plt.ylabel("Monthly Cost ($)")

        plt.title("Cloud Service Monthly Cost")

        plt.tight_layout()

        plt.savefig("cloud_cost_dashboard.png")

        print("Chart Saved -> cloud_cost_dashboard.png")

        plt.show()

    def recommend_optimization(self):

        average = self.data["Monthly Cost ($)"].mean()

        print("\nOptimization Recommendations")

        print("----------------------------")

        expensive = self.data[
            self.data["Monthly Cost ($)"] > average
        ]

        for _, row in expensive.iterrows():

            print(
                f"{row['Service']} is spending "
                f"${row['Monthly Cost ($)']:.2f}. "
                f"Consider Reserved Instances, Rightsizing or Auto Scaling."
            )


def main():

    dashboard = CloudCostDashboard()

    dashboard.generate_sample_data()

    dashboard.display_summary()

    dashboard.highest_cost_service()

    dashboard.recommend_optimization()

    dashboard.save_csv()

    dashboard.plot_chart()


if __name__ == "__main__":
    main()
