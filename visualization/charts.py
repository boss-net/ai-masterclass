import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class Chart:
    def __init__(self, title: str, data: List[Dict[str, Any]]):
        self.title = title
        self.data = data
        self.layout = {
            "title": title,
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Value"},
            "autosize": True,
            "margin": dict(l=50, r=50, b=100, t=100, pad=4),
        }

    def to_json(self) -> Dict[str, Any]:
        """Convert chart to JSON format."""
        return {"data": self._prepare_data(), "layout": self.layout}


class LineChart(Chart):
    def __init__(self, title: str, data: List[Dict[str, Any]], interval: str = "1m"):
        super().__init__(title, data)
        self.interval = interval

    def _prepare_data(self) -> List[Dict[str, Any]]:
        """Prepare data for line chart."""
        timestamps = [d["timestamp"] for d in self.data]
        values = [d["value"] for d in self.data]

        return [
            {
                "x": timestamps,
                "y": values,
                "type": "scatter",
                "mode": "lines+markers",
                "name": self.title,
            }
        ]


class BarChart(Chart):
    def __init__(self, title: str, data: List[Dict[str, Any]], group_by: str = "category"):
        super().__init__(title, data)
        self.group_by = group_by

    def _prepare_data(self) -> List[Dict[str, Any]]:
        """Prepare data for bar chart."""
        categories = set(d[self.group_by] for d in self.data)
        traces = []

        for category in categories:
            filtered = [d for d in self.data if d[self.group_by] == category]
            values = [d["value"] for d in filtered]

            traces.append(
                {
                    "x": [d["timestamp"] for d in filtered],
                    "y": values,
                    "type": "bar",
                    "name": category,
                }
            )

        return traces


class PieChart(Chart):
    def __init__(self, title: str, data: List[Dict[str, Any]], labels: str = "category"):
        super().__init__(title, data)
        self.labels = labels

    def _prepare_data(self) -> List[Dict[str, Any]]:
        """Prepare data for pie chart."""
        categories = set(d[self.labels] for d in self.data)
        values = []
        labels = []

        for category in categories:
            filtered = [d for d in self.data if d[self.labels] == category]
            total = sum(d["value"] for d in filtered)

            values.append(total)
            labels.append(category)

        return [{"values": values, "labels": labels, "type": "pie"}]


class HeatmapChart(Chart):
    def __init__(self, title: str, data: List[Dict[str, Any]], x: str = "x", y: str = "y"):
        super().__init__(title, data)
        self.x = x
        self.y = y

    def _prepare_data(self) -> List[Dict[str, Any]]:
        """Prepare data for heatmap."""
        x_values = sorted(set(d[self.x] for d in self.data))
        y_values = sorted(set(d[self.y] for d in self.data))
        z_values = [[0] * len(x_values) for _ in range(len(y_values))]

        for d in self.data:
            x_idx = x_values.index(d[self.x])
            y_idx = y_values.index(d[self.y])
            z_values[y_idx][x_idx] = d["value"]

        return [{"z": z_values, "x": x_values, "y": y_values, "type": "heatmap"}]


class ScatterMatrix(Chart):
    def __init__(self, title: str, data: List[Dict[str, Any]], dimensions: List[str]):
        super().__init__(title, data)
        self.dimensions = dimensions

    def _prepare_data(self) -> List[Dict[str, Any]]:
        """Prepare data for scatter matrix."""
        traces = []

        for i, dim1 in enumerate(self.dimensions):
            for j, dim2 in enumerate(self.dimensions):
                if i != j:
                    x = [d[dim1] for d in self.data]
                    y = [d[dim2] for d in self.data]

                    traces.append(
                        {
                            "x": x,
                            "y": y,
                            "type": "scatter",
                            "mode": "markers",
                            "name": f"{dim1} vs {dim2}",
                        }
                    )

        return traces
