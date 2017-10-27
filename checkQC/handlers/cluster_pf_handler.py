from math import pow

from checkQC.handlers.qc_handler import QCHandler, QCErrorFatal, QCErrorWarning
from checkQC.parsers.stats_json_parser import StatsJsonParser


class ClusterPFHandler(QCHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_results = None

    def parser(self):
        return StatsJsonParser

    def collect(self, signal):
        key, value = signal
        if key == "ConversionResults":
            self.conversion_results = value

    def check_qc(self):

        for lane_dict in self.conversion_results:
            lane_nbr = lane_dict["LaneNumber"]
            lane_pf = lane_dict["TotalClustersPF"]

            if self.error() != self.UNKNOWN and lane_pf < float(self.error())*pow(10, 6):
                yield QCErrorFatal("Clusters PF was to low on lane {}, it was: {}".format(lane_nbr, lane_pf),
                                   ordering=int(lane_nbr))
            elif self.warning() != self.UNKNOWN and lane_pf < float(self.warning())*pow(10, 6):
                yield QCErrorWarning("Cluster PF was to low on lane {}, it was: {}".format(lane_nbr, lane_pf),
                                     ordering=int(lane_nbr))
            else:
                continue
