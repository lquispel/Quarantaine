
import configparser
import networkx
import random

class Network_Configurator:

    def __init__(self,verbose=0):
        self.network = 0
        self.node_number = 0
        self.config = 0
        self.log = []
        if verbose == True:
            self.__verbose = True
        else:
            self.__verbose = False

    def get_random_node(self,key=0,value=0):
        if self.node_number < 2:
            return self.network.nodes[0]
        searching = True
        while searching:
            gamble = random.randint(0,self.node_number-1)
            node = self.network.nodes[gamble]
            if key != 0:
                if key in node:
                    if value == 0:
                        searching = False
                    else:
                        if node[key] == value:
                            searching = False
            else:
                searching = False
        return gamble

    def create_persons(self):
        # singles
        counter = 0
        logstring = "Qu Creating: "
        while counter < self.config["GENERAL"].getint("number_of_singles"):
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_SINGLE")
            counter += 1
            self.node_number += 1
        counter = 0
        # couples
        while counter < self.config["GENERAL"].getint("number_of_couples"):
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_COUPLE")
            self.node_number += 1
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="UNEMPLOYABLE",
                             living="LIVING_COUPLE")
            self.node_number += 1
            self.network.add_edge(self.node_number - 1, self.node_number - 2, relation="LIVING_TOGETHER")
            counter += 1
        counter = 0

    def create_families(self):
        logstring = "Creating family: "
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_families"):
            subcounter = 0
            node_numbers = []
            while subcounter < self.config["FAMILIES"].getint("number_of_fathermothers"):
                self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT",
                                 employable="EMPLOYABLE", living="LIVING_FAMILY", )
                node_numbers.append(self.node_number)
                logstring += "p" + str(self.node_number) + " "
                self.node_number += 1
                subcounter += 1
            subcounter = 0
            while subcounter < self.config["FAMILIES"].getint("family_size") - self.config["FAMILIES"].getint(
                    "number_of_fathermothers"):
                self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="CHILD",
                                 employable="UNEMPLOYABLE", living="LIVING_FAMILY", )
                node_numbers.append(self.node_number)
                logstring += "c" + str(self.node_number) + " "
                self.node_number += 1
                subcounter += 1
            for number1 in node_numbers:
                for number2 in node_numbers:
                    if number1 != number2:
                        if self.network.has_edge(number1, number2) == False:
                            print("edge from " + str(number1) + " to " + str(number2))
                            self.network.add_edge(number1, number2, relation="LIVING_TOGETHER")
            if self.__verbose:
                print(logstring)
            logstring += "\n"
            self.log.append(logstring)
            counter += 1



    def create_schools(self):
        children = self.config["CONNECTIONS"].getint("school_size")
        self.network.add_node(self.node_number, type="school", state="OPEN")
        node = self.get_random_node("employable","EMPLOYABLE")
        self.network.nodes[node]["employable"] = "EMPLOYED"
        self.network.add_edge(self.node_number,node,relation="EMPLOYMENT")
        self.node_number += 1
        for index in range(0, self.node_number - 2):
            if self.network.nodes[index]["age"] == "CHILD":
                self.network.add_edge(index, self.node_number-1, relation="ATTENDING")
                children -= 1
                if children < 0:
                    children = self.config["CONNECTIONS"].getint("school_size")
                    self.network.add_node(self.node_number, type="school", state="OPEN")
                    node = self.get_random_node("employable", "EMPLOYABLE")
                    self.network.nodes[node]["employable"] = "EMPLOYED"
                    self.network.add_edge(self.node_number, node, relation="EMPLOYMENT")
                    self.node_number += 1

    def create_companies(self):
        if self.config["CONNECTIONS"].getboolean("use_companies"):
            employees = self.config["CONNECTIONS"].getint("company_size")
            self.network.add_node(self.node_number, type="company", state="OPEN")
            self.node_number += 1
            for index in range(0, self.node_number - 2):
                if 'employable' in self.network.nodes[index]:
                    if self.network.nodes[index]["employable"] == "EMPLOYABLE":
                        self.network.nodes[index]["employable"] == "EMPLOYED"
                        self.network.add_edge(index, self.node_number - 1, relation="EMPLOYMENT")
                        employees -= 1
                        if employees < 0:
                            employees = self.config["CONNECTIONS"].getint("company_size")
                            self.network.add_node(self.node_number, type="company", state="OPEN")
                            self.node_number += 1

    def generate_from_file(self,type,nodes,connectiviy,configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.network = networkx.Graph()
        self.node_number = 0
        self.create_families()
        return self.network

