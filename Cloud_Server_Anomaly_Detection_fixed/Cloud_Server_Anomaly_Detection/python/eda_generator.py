import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def generate_eda_plots(data_path: str, figures_dir: Path):
    """Generates and saves analytical plots for the EDA report."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Set plot styles
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12})
    
    # 1. Metric Distributions Plot
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    metrics = ["cpu_usage", "memory_usage", "disk_usage", "network_traffic", "response_time", "request_rate"]
    titles = [
        "CPU Utilization (%)", "Memory Utilization (%)", "Disk Write Throughput (MB/s)", 
        "Network Traffic (MB/s)", "Response Time (ms)", "Request Rate (req/sec)"
    ]
    colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B", "#9013FE", "#B8E986"]
    
    for idx, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
        ax = axes[idx // 2, idx % 2]
        sns.histplot(df[metric], kde=True, ax=ax, color=color, alpha=0.7)
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        
    plt.tight_layout()
    dist_path = figures_dir / "metric_distributions.png"
    plt.savefig(dist_path, dpi=150)
    plt.close()
    print(f"Saved metric distributions plot to {dist_path}")
    
    # 2. Server Metric Comparison Plot (Boxplots)
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    for idx, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
        ax = axes[idx // 2, idx % 2]
        sns.boxplot(x="server_id", y=metric, data=df, ax=ax, hue="server_id", legend=False, palette="Set2")
        ax.set_title(f"Comparison: {title}")
        ax.set_xlabel("")
        ax.set_ylabel("")
        
    plt.tight_layout()
    comp_path = figures_dir / "server_comparison.png"
    plt.savefig(comp_path, dpi=150)
    plt.close()
    print(f"Saved server comparison plot to {comp_path}")
    
    # 3. Correlation Heatmap
    plt.figure(figsize=(8, 6))
    corr = df[metrics].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1, square=True, linewidths=0.5)
    plt.title("Metric Correlation Heatmap")
    plt.tight_layout()
    corr_path = figures_dir / "correlation_heatmap.png"
    plt.savefig(corr_path, dpi=150)
    plt.close()
    print(f"Saved correlation heatmap to {corr_path}")
    
    # 4. Time Series Workload Profiles (3-Day Sample)
    sample_df = df[df["timestamp"] <= df["timestamp"].min() + pd.Timedelta(days=3)]
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    
    sns.lineplot(data=sample_df, x="timestamp", y="cpu_usage", hue="server_id", ax=axes[0], alpha=0.85)
    axes[0].set_title("CPU Utilization Profile (%) - 3-Day Sample")
    axes[0].set_ylabel("CPU %")
    axes[0].get_legend().remove()
    
    sns.lineplot(data=sample_df, x="timestamp", y="network_traffic", hue="server_id", ax=axes[1], alpha=0.85)
    axes[1].set_title("Network Traffic Profile (MB/s) - 3-Day Sample")
    axes[1].set_ylabel("Traffic (MB/s)")
    axes[1].get_legend().remove()
    
    sns.lineplot(data=sample_df, x="timestamp", y="response_time", hue="server_id", ax=axes[2], alpha=0.85)
    axes[2].set_title("Response Time Profile (ms) - 3-Day Sample")
    axes[2].set_ylabel("RT (ms)")
    
    plt.xlabel("Time")
    plt.tight_layout()
    ts_path = figures_dir / "server_time_series.png"
    plt.savefig(ts_path, dpi=150)
    plt.close()
    print(f"Saved server time series sample plot to {ts_path}")

def generate_notebook(output_path: Path):
    """Generates the Jupyter notebook 01_data_exploration.ipynb."""
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 01 Exploratory Data Analysis (EDA)\n",
                    "**Project Title**: Intelligent Cloud Server Anomaly Detection and Real-Time Monitoring System\n",
                    "\n",
                    "This notebook performs exploratory analysis on our validated server metrics dataset. We examine distributions, temporal behaviors, server-level profiles, and correlations to establish baseline server characteristics."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from pathlib import Path\n",
                    "\n",
                    "# Set plot styles\n",
                    "sns.set_theme(style=\"whitegrid\")\n",
                    "plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12})\n",
                    "\n",
                    "# Load the validated dataset\n",
                    "data_path = \"../data/processed/validated_historical_metrics.csv\"\n",
                    "df = pd.read_csv(data_path)\n",
                    "df[\"timestamp\"] = pd.to_datetime(df[\"timestamp\"])\n",
                    "\n",
                    "print(f\"Dataset Shape: {df.shape}\")\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Summary Statistics\n",
                    "Let's inspect numerical descriptions of the server metrics."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df.describe().T"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Server-Wise Observations Counts"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df[\"server_id\"].value_counts()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Metric Distribution Profiles\n",
                    "We plot histogram distributions with Kernel Density Estimates (KDE) to inspect shapes, skewness, and extreme value patterns."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, axes = plt.subplots(3, 2, figsize=(14, 11))\n",
                    "metrics = [\"cpu_usage\", \"memory_usage\", \"disk_usage\", \"network_traffic\", \"response_time\", \"request_rate\"]\n",
                    "titles = [\n",
                    "    \"CPU Utilization (%)\", \"Memory Utilization (%)\", \"Disk Write Throughput (MB/s)\", \n",
                    "    \"Network Traffic (MB/s)\", \"Response Time (ms)\", \"Request Rate (req/sec)\"\n",
                    "]\n",
                    "colors = [\"#4A90E2\", \"#50E3C2\", \"#F5A623\", \"#D0021B\", \"#9013FE\", \"#B8E986\"]\n",
                    "\n",
                    "for idx, (metric, title, color) in enumerate(zip(metrics, titles, colors)):\n",
                    "    ax = axes[idx // 2, idx % 2]\n",
                    "    sns.histplot(df[metric], kde=True, ax=ax, color=color, alpha=0.7)\n",
                    "    ax.set_title(title)\n",
                    "    ax.set_xlabel(\"\")\n",
                    "    ax.set_ylabel(\"Count\")\n",
                    "    \n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Server Workload Comparison\n",
                    "We use boxplots to compare the load profiles across `SERVER-01`, `SERVER-02`, and `SERVER-03`."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, axes = plt.subplots(3, 2, figsize=(14, 11))\n",
                    "for idx, (metric, title) in enumerate(zip(metrics, titles)):\n",
                    "    ax = axes[idx // 2, idx % 2]\n",
                    "    sns.boxplot(x=\"server_id\", y=metric, data=df, ax=ax, hue=\"server_id\", legend=False, palette=\"Set2\")\n",
                    "    ax.set_title(f\"Comparison: {title}\")\n",
                    "    ax.set_xlabel(\"\")\n",
                    "    ax.set_ylabel(\"\")\n",
                    "    \n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. Metric Correlation Heatmap\n",
                    "Examining linear dependencies between resource metrics."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "plt.figure(figsize=(8, 6))\n",
                    "corr = df[metrics].corr()\n",
                    "mask = np.triu(np.ones_like(corr, dtype=bool))\n",
                    "sns.heatmap(corr, mask=mask, annot=True, cmap=\"coolwarm\", fmt=\".2f\", vmin=-1, vmax=1, square=True, linewidths=0.5)\n",
                    "plt.title(\"Metric Correlation Heatmap\")\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 6. Time Series Workload Profiles (3-Day Sample)\n",
                    "Let's trace resource metrics over time for a 3-day window to look for peaks, cyclical workloads, and correlations."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "sample_df = df[df[\"timestamp\"] <= df[\"timestamp\"].min() + pd.Timedelta(days=3)]\n",
                    "fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)\n",
                    "\n",
                    "sns.lineplot(data=sample_df, x=\"timestamp\", y=\"cpu_usage\", hue=\"server_id\", ax=axes[0], alpha=0.85)\n",
                    "axes[0].set_title(\"CPU Utilization Profile (%) - 3-Day Sample\")\n",
                    "axes[0].set_ylabel(\"CPU %\")\n",
                    "axes[0].get_legend().remove()\n",
                    "\n",
                    "sns.lineplot(data=sample_df, x=\"timestamp\", y=\"network_traffic\", hue=\"server_id\", ax=axes[1], alpha=0.85)\n",
                    "axes[1].set_title(\"Network Traffic Profile (MB/s) - 3-Day Sample\")\n",
                    "axes[1].set_ylabel(\"Traffic (MB/s)\")\n",
                    "axes[1].get_legend().remove()\n",
                    "\n",
                    "sns.lineplot(data=sample_df, x=\"timestamp\", y=\"response_time\", hue=\"server_id\", ax=axes[2], alpha=0.85)\n",
                    "axes[2].set_title(\"Response Time Profile (ms) - 3-Day Sample\")\n",
                    "axes[2].set_ylabel(\"RT (ms)\")\n",
                    "\n",
                    "plt.xlabel(\"Time\")\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(notebook_content, f, indent=1)
    print(f"Generated Jupyter notebook at {output_path}")

if __name__ == "__main__":
    data_file = "data/processed/validated_historical_metrics.csv"
    fig_dir = Path("results/figures")
    notebook_file = Path("notebooks/01_data_exploration.ipynb")
    
    if os.path.exists(data_file):
        generate_eda_plots(data_file, fig_dir)
        generate_notebook(notebook_file)
    else:
        print(f"Data file {data_file} not found. Ingest data first.")
