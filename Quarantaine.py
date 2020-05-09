
import configparser

# import ndlib modules
# model modules
import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
# visualization modules
import matplotlib.pyplot as plt
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.bokeh.MultiPlot import MultiPlot

# import Quarantaine modules
import network_configurator

class Simulator:

    def __init__(self,config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Starting Quarantaine with " + config_file)
        self._active_network = 0
        self._active_model = 0

    def plot_networks(self):
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Plotting networks ... ")
        nx.draw(self._active_network, with_labels=True)
        plt.show()

    def plot_trends(self,iterations):
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Plotting trends ... ")
        trends = self._active_model.build_trends(iterations)
        viz = DiffusionTrend(self._active_model, trends)
        p = viz.plot(width=400, height=400)
        viz2 = DiffusionPrevalence(self._active_model, trends)
        p2 = viz2.plot(width=400, height=400)
        vm = MultiPlot()
        vm.add_plot(p)
        vm.add_plot(p2)
        m = vm.plot()
        show(m)

    def create_network(self,type,nodes,connectivity,configfile=0):
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Creating network ...  ")
        # Network Definition
        if configfile != 0:
            generator = network_configurator.Network_Configurator()
            self._active_network = generator.generate_from_file(type,nodes,connectivity,configfile)
        else:
            if type == 0:
                self._active_network = nx.erdos_renyi_graph(nodes, 0.1, 1000)
            else:
                self._active_network = 0
        return self._active_network

    def create_model(self,model_type,network):
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Creating model ...  ")
        # Model Selection
        if model_type == 'SIR':
            self._active_model = ep.SIRModel(network)
        else:
            self._active_model = 0
        # Model Configuration
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.001)
        config.add_model_parameter('gamma', 0.01)
        config.add_model_parameter("fraction_infected", 0.05)
        self._active_model.set_initial_status(config)
        return self._active_model

    def run(self,nr_iterations):
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Running model on network ... ")
        if self._active_model == 0:
            if self.config["UI"].getboolean("verbose"):
                print("Qu: !!! Run aborted, no active model  ")
            return False
        if self._active_network == 0:
            if self.config["UI"].getboolean("verbose"):
                print("Qu: !!! Run aborted, no active network  ")
            return False
        iterations = self._active_model.iteration_bunch(200)
        if self.config["UI"].getboolean("verbose"):
            print("Qu: Model ran, " + str(nr_iterations) + " iterations")
        if self.config["UI"].getboolean("headless"):
            return True
        else:
            if self.config["UI"].getboolean("verbose"):
                print("Qu: Generating network plot ... ")
            self.plot_networks()
            if self.config["UI"].getboolean("verbose"):
                print("Qu: Generating trend plot ... ")
            self.plot_trends(iterations)
            return True

def main():

    config_file = "quarantaine.cfg"
    simulator = Simulator(config_file)
    simulator.create_model("SIR",simulator.create_network(0,1000,0.1,"network.cfg"))
    simulator.run(200)

if __name__ == "__main__":
        main()