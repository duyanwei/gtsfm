"""Functions to generate a report of metrics with tables and plots.

A HTML report can be generated using the generate_metrics_report_html() function, 
if called with a list of GtsfmMetricsGroup. 
The HTML report has headers, section headings, tables generated using tabulate
and grids of box or histogram plots generated using plotly.

Authors: Akshay Krishnan
"""
from typing import Any, Dict, List, Tuple, Union

import plotly.graph_objects as go
import plotly.subplots as psubplot
from tabulate import tabulate

import gtsfm.evaluation.metrics as metrics
from gtsfm.evaluation.metrics import GtsfmMetricsGroup

SUBPLOTS_PER_ROW = 3


def get_readable_metric_name(metric_name: str) -> str:
    """Helper to convert a metric name separated by underscores to readable format.

    In readable format, each word is capitalized and are separated by spaces.
    Ex: bundle_adjustment_metrics -> Bundle Adjustment Metrics

    Args:
        metric_name: where words are separated by underscores.

    Returns:
        readable metric name where words are separated by spaces.
    """
    words = metric_name.split("_")
    words = [word.capitalize() for word in words]
    return " ".join(words)


def create_table_for_scalar_metrics(metrics_dict: Dict[str, Union[float, int]]) -> str:
    """Creates a table in HTML format for scalar metrics.

    Returns:
        Table with scalar metrics and their values in HTML format.
    """
    table = {
        "Metric name": list(metrics_dict.keys()),
        "Value": list(metrics_dict.values()),
    }
    return tabulate(table, headers="keys", tablefmt="html")


def create_table_for_scalar_metrics_and_compare(
    metrics_dicts: List[Dict[str, Union[float, int]]]
) -> str:
    """Creates a table in HTML format for scalar metrics.

    Returns:
        Table with scalar metrics and their values in HTML format.
    """
    for metrics_dict in metrics_dicts:
        for metric_key, metric_value in metrics_dict.items():
            if isinstance(metric_value, float):
                if metric_value.is_integer():
                    metrics_dict[metric_key] = int(metric_value)
                else:
                    metrics_dict[metric_key] = round(metric_value, 3)
    table = {
        "Metric name": list(metrics_dicts[0].keys()),
        "GTSfM": list(metrics_dicts[0].values()),
        "COLMAP": list(metrics_dicts[1].values()),
    }
    return tabulate(table, headers="keys", tablefmt="html")


def create_plots_for_distributions(metrics_dict: Dict[str, Any]) -> str:
    """Creates plots for 1D distribution metrics using plotly, and converts them to HTML.

    The plots are arranged in a grid, with each row having SUBPLOTS_PER_ROW (3) columns.
    For a certain metric, these can be either histogram or box according to the metric's property.

    Args:
        metrics_dict: A dict, where keys are names of metrics and values are
        the dictionary representation of the metric.
    Returns:
        Plots in a grid converted to HTML as a string.
    """
    distribution_metrics = []
    # Separate all the 1D distribution metrics.
    for metric, value in metrics_dict.items():
        if isinstance(value, dict):
            all_nan_summary = all(v != v for v in value[metrics.SUMMARY_KEY].values())
            if not all_nan_summary:
                distribution_metrics.append(metric)
    if len(distribution_metrics) == 0:
        return ""

    # Setup figure layout - number of rows and columns.
    num_rows = (len(distribution_metrics) + SUBPLOTS_PER_ROW - 1) // SUBPLOTS_PER_ROW
    fig = psubplot.make_subplots(
        rows=num_rows, cols=SUBPLOTS_PER_ROW, subplot_titles=distribution_metrics
    )
    fig.update_layout({"height": 512 * num_rows, "width": 1024, "showlegend": False})
    i = 0

    # Iterate over all metrics.
    for metric_name, metric_value in metrics_dict.items():
        # Check if this is a 1D distribution metric and has a summary.
        if (
            metric_name not in distribution_metrics
            or metrics.SUMMARY_KEY not in metric_value
        ):
            continue
        row = i // SUBPLOTS_PER_ROW + 1
        col = i % SUBPLOTS_PER_ROW + 1
        i += 1
        # Histogram metrics are plotted directly from summary.
        if "histogram" in metric_value[metrics.SUMMARY_KEY]:
            histogram = metric_value[metrics.SUMMARY_KEY]["histogram"]
            fig.add_trace(
                go.Bar(
                    x=list(histogram.keys()),
                    y=list(histogram.values()),
                    name=metric_name,
                ),
                row=row,
                col=col,
            )
        elif "quartiles" in metric_value[metrics.SUMMARY_KEY]:
            # If all values are available, use them to create box plot.
            if metrics.FULL_DATA_KEY in metric_value:
                fig.add_trace(
                    go.Box(y=metric_value[metrics.FULL_DATA_KEY], name=metric_name),
                    row=row,
                    col=col,
                )
            # Else use summary to create box plot.
            else:
                quartiles = metric_value[metrics.SUMMARY_KEY]["quartiles"]
                fig.add_trace(
                    go.Box(
                        q1=[quartiles["q1"]],
                        median=[quartiles["q2"]],
                        q3=[quartiles["q3"]],
                        lowerfence=[quartiles["q0"]],
                        upperfence=[quartiles["q4"]],
                        name=metric_name,
                    ),
                    row=row,
                    col=col,
                )

    # Return the figure converted to HTML.
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def get_figures_for_metrics(metrics_group: GtsfmMetricsGroup) -> Tuple[str, str]:
    """Gets the tables and plots for individual metrics in a metrics group.

    All scalar metrics are reported in the table.
    Metrics of 1-D distributions have an entry in the table for the mean,
    and a histogram or box plot as per their property.

    Args:
        metrics_group: A GtsfmMetricsGroup for any gtsfm module.

    Returns:
        A tuple of table and plotly figures as HTML code.
    """
    scalar_metrics = {}
    metrics_dict = metrics_group.get_metrics_as_dict()[metrics_group.name]
    # Separate the scalar metrics.
    for metric_name, value in metrics_dict.items():
        if isinstance(value, dict):
            # Metrics with a dict representation must contain a summary.
            if metrics.SUMMARY_KEY not in value:
                raise ValueError(f"Metric {metric_name} does not contain a summary.")
            # Add a scalar metric for mean of 1D distributions.
            scalar_metrics["mean_" + metric_name] = value[metrics.SUMMARY_KEY]["mean"]
            scalar_metrics["median_" + metric_name] = value[metrics.SUMMARY_KEY][
                "median"
            ]
        else:
            scalar_metrics[metric_name] = value
    table = create_table_for_scalar_metrics(scalar_metrics)
    plots_fig = create_plots_for_distributions(metrics_dict)
    return table, plots_fig


def get_figures_for_metrics_and_compare(
    metrics_group: GtsfmMetricsGroup, metric_path: str
) -> Tuple[str, str]:
    """Gets the tables and plots for individual metrics in a metrics group.

    All scalar metrics are reported in the table.
    Metrics of 1-D distributions have an entry in the table for the mean,
    and a histogram or box plot as per their property.

    Args:
        metrics_group: A GtsfmMetricsGroup for any gtsfm module.

    Returns:
        A tuple of table and plotly figures as HTML code.
    """
    all_scalar_metrics = []
    all_metrics_groups = []

    colmap_metric_path = (
        metric_path[: metric_path.rindex("/")]
        + "/colmap"
        + metric_path[metric_path.rindex("/") :]
    )
    colmap_metrics_group = GtsfmMetricsGroup.parse_from_json(colmap_metric_path)

    all_metrics_groups.append(metrics_group)
    all_metrics_groups.append(colmap_metrics_group)

    for metrics_group in all_metrics_groups:
        scalar_metrics = {}
        metrics_dict = metrics_group.get_metrics_as_dict()[metrics_group.name]
        # Separate the scalar metrics.
        for metric_name, value in metrics_dict.items():
            if isinstance(value, dict):
                # Metrics with a dict representation must contain a summary.
                if metrics.SUMMARY_KEY not in value:
                    raise ValueError(
                        f"Metric {metric_name} does not contain a summary."
                    )
                # Add a scalar metric for mean of 1D distributions.
                mean_nan = (
                    value[metrics.SUMMARY_KEY]["mean"]
                    != value[metrics.SUMMARY_KEY]["mean"]
                )
                median_nan = (
                    value[metrics.SUMMARY_KEY]["median"]
                    != value[metrics.SUMMARY_KEY]["median"]
                )
                if mean_nan or median_nan:
                    scalar_metrics["mean_" + metric_name] = ""
                    scalar_metrics["median_" + metric_name] = ""
                else:
                    scalar_metrics["mean_" + metric_name] = value[metrics.SUMMARY_KEY][
                        "mean"
                    ]
                    scalar_metrics["median_" + metric_name] = value[
                        metrics.SUMMARY_KEY
                    ]["median"]
            else:
                scalar_metrics[metric_name] = value
        all_scalar_metrics.append(scalar_metrics)
    table = create_table_for_scalar_metrics_and_compare(all_scalar_metrics)

    # TODO Add plots for COLMAP, not just GTSfM
    plots_fig = ""
    for metrics_group in all_metrics_groups:
        plots_fig += create_plots_for_distributions(
            metrics_group.get_metrics_as_dict()[metrics_group.name]
        )
    # plots_fig += create_plots_for_distributions(all_metrics_groups[0].get_metrics_as_dict()[metrics_group.name])
    return table, plots_fig


def get_html_metric_heading(metric_name: str) -> str:
    """Helper to get the HTML heading for a metric name.

    This converts a "metric_name" to "Metric Name" (for readability) and adds some style.

    Returns:
        HTML for heading as a string.
    """
    metric_name = get_readable_metric_name(metric_name)
    metric_html = f'<p style="font-size:25px;font-family:Arial">{metric_name}</p>'
    return metric_html


def get_html_header() -> str:
    """Helper to get a HTML header with some CSS styles for tables.""

    Returns:
        A HTML header as string.
    """
    return """<head>
                <style>
                  table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 768px
                  }
                  td, th {
                    border: 1px solid #999999;
                    text-align: left;
                    padding: 8px;
                  }
                  tr:nth-child(even) {
                    background-color: #dddddd;
                  }
                </style>
              </head>"""


def generate_metrics_report_html(
    metrics_groups: List[GtsfmMetricsGroup],
    html_path: str,
    colmap_files_dirpath: str,
    metric_paths: List[str],
) -> None:
    """Generates a report for metrics groups with plots and tables and saves it to HTML.

    Args:
        metrics_groups: List of metrics to be reported.
    """
    with open(html_path, mode="w") as f:
        # Write HTML headers.
        f.write("<!DOCTYPE html>" "<html>")
        f.write(get_html_header())

        # Iterate over all metrics groups
        for i, metrics_group in enumerate(metrics_groups):

            # Write name of the metric group in human readable form.
            f.write(get_html_metric_heading(metrics_group.name))

            # Write plots and tables.
            if colmap_files_dirpath == "":
                table, plots_fig = get_figures_for_metrics(metrics_group)
            else:
                table, plots_fig = get_figures_for_metrics_and_compare(
                    metrics_group, metric_paths[i]
                )
            f.write(table)
            if plots_fig is not None:
                f.write(plots_fig)

        # Close HTML tags.
        f.write("</html>")
