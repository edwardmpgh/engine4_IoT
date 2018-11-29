import plotly.plotly as py
import plotly.graph_objs as go

from controller.models import SensorType

class iot_chart(object):

    def __init__(self, data):
        self.source_data = data

    def co_chart(self):

        try:
            sensor_levels = SensorType.objects.get(name='CO Detector')
        except:
            pass

        if sensor_levels:
            low = sensor_levels.alert_low
            high = sensor_levels.alert_high
        else:
            # use the default levels o=for CO
            low = 50
            high = 200

        base_chart = {
            "values": [40, 30, 30],
            "labels": ["-", low, high],
            "domain": {"x": [0, .48]},
            "marker": {
                "colors": [
                    'rgb(255, 255, 255)',
                    'rgb(255, 255, 255)',
                    'rgb(255, 255, 255)'
                ],
                "line": {
                    "width": 1
                }
            },
            "name": "Gauge",
            "hole": .4,
            "type": "pie",
            "direction": "clockwise",
            "rotation": 108,
            "showlegend": False,
            "hoverinfo": "none",
            "textinfo": "label",
            "textposition": "outside"
        }

        meter_chart = {
            "values": [50, 25, 25],
            "labels": ["Normal", "Warn", "Fatal"],
            "marker": {
                'colors': [
                    'rgb(255, 255, 255)',
                    'rgb(223,162,103)',
                    'rgb(226,126,64)'
                ]
            },
            "domain": {"x": [0, 0.48]},
            "name": "Gauge",
            "hole": .3,
            "type": "pie",
            "direction": "clockwise",
            "rotation": 90,
            "showlegend": False,
            "textinfo": "label",
            "textposition": "inside",
            "hoverinfo": "none"
        }

        layout = {
            'xaxis': {
                'showticklabels': False,
                'showgrid': False,
                'zeroline': False,
            },
            'yaxis': {
                'showticklabels': False,
                'showgrid': False,
                'zeroline': False,
            },
            'shapes': [
                {
                    'type': 'path',
                    'path': 'M 0.235 0.5 L 0.24 0.65 L 0.245 0.5 Z',
                    'fillcolor': 'rgba(44, 160, 101, 0.5)',
                    'line': {
                        'width': 0.5
                    },
                    'xref': 'paper',
                    'yref': 'paper'
                }
            ],
            'annotations': [
                {
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0.23,
                    'y': 0.45,
                    'text': '50',
                    'showarrow': False
                }
            ]
        }

        # we don't want the boundary now
        base_chart['marker']['line']['width'] = 0

        fig = {"data": [base_chart, meter_chart],
               "layout": layout}
        return py.iplot(fig, filename='gauge-meter-chart')
