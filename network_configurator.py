
import configparser
import networkx
import random

class Organisation:

    def __init__(self,org_dict):
        self.type = org_dict["type"]
        self.size = int(org_dict["size"])     # int(org_dict["size"])
        self.key = org_dict["key"]
        self.value = org_dict["value"]
        self.sector = org_dict["sector"]
        self.value_change = org_dict["type"]
        self.relation = org_dict["relation"]
        self.adminstrators = int(org_dict["administrators"])
        if self.adminstrators > 0:
            self.adminstrator_key = org_dict["administrator_key"]
            self.administrator_value = org_dict["administrator_value"]
            self.administrator_value_change = org_dict["administrator_value_change"]
            self.administrator_relation = org_dict["administrator_relation"]

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
        if self.node_number < 2:        # return first node if only two or less nodes present
            return self.network.nodes[0]
        while 1:
            gamble = random.randint(0,self.node_number-1)
            if key != 0:     # if no key argument, just return the node
                node = self.network.nodes[gamble]
                if key in node:
                    if value != 0:  # if no value argument, just return the node
                        if node[key] == value:
                            return gamble
                else:
                    return gamble
            else:
                return gamble


    def create_singles(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_singles"):
            logstring = "Qu Creating single: s" + str(self.node_number)
            if self.__verbose:
                print (logstring)
            self.log.append( logstring )
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_SINGLE",religious="Yes")
            counter += 1
            self.node_number += 1

    def create_couples(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_couples"):
            logstring = "Qu Creating Couple: c" + str(self.node_number)
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_COUPLE",religious="Yes")
            self.node_number += 1
            logstring += " s" + str(self.node_number)
            if self.__verbose:
                print(logstring)
            self.log.append(logstring + "\n" )
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="UNEMPLOYABLE",
                             living="LIVING_COUPLE",religious="Yes")
            self.node_number += 1
            self.network.add_edge(self.node_number - 1, self.node_number - 2, relation="LIVING_TOGETHER")
            counter += 1

    def create_families(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_families"):
            logstring = "Qu: Creating family " + str(counter) + ": "
            subcounter = 0
            node_numbers = []
            while subcounter < self.config["GENERAL"].getint("number_of_parents"):
                self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT",
                                 employable="EMPLOYABLE", living="LIVING_FAMILY", religious="Yes" )
                node_numbers.append(self.node_number)
                logstring += "p" + str(self.node_number) + " "
                self.node_number += 1
                subcounter += 1
            subcounter = 0
            while subcounter < self.config["GENERAL"].getint("family_size") - self.config["GENERAL"].getint(
                    "number_of_parents"):
                self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="CHILD",
                                 employable="UNEMPLOYABLE", living="LIVING_FAMILY",religious="Yes" )
                node_numbers.append(self.node_number)
                logstring += "c" + str(self.node_number) + " "
                self.node_number += 1
                subcounter += 1
            for number1 in node_numbers:
                for number2 in node_numbers:
                    if number1 != number2:
                        if self.network.has_edge(number1, number2) == False:
                            self.network.add_edge(number1, number2, relation="LIVING_TOGETHER")
            if self.__verbose:
                print(logstring)
            self.log.append(logstring + "\n")
            counter += 1

    def create_organisations(self,organisation):
        organisation_count = 0
        size = 0
        logstring = ""
        for index in range(0, self.node_number - 1):
            if size == 0:
                if self.__verbose:
                     print(logstring)
                self.log.append(logstring + "\n")
                size = organisation.size
                organisation_count += 1
                self.network.add_node(self.node_number, type=organisation.type, sector=organisation.sector, state="OPEN")
                logstring = "Qu: Creating " + str(organisation.type) + " organisation " + str(organisation_count) + ", node:o" + str(self.node_number) + ", |"
                adm_count = organisation.adminstrators
                while adm_count > 0:
                    node = self.get_random_node(organisation.adminstrator_key,organisation.administrator_value)
                    logstring += "adm:" + str(node) + ","
                    self.network.add_edge(self.node_number, node, relation=organisation.administrator_relation, sector=organisation.sector)
                    self.network.nodes[node][organisation.adminstrator_key] = organisation.administrator_value_change
                    adm_count -= 1
                logstring += " | "
                self.node_number += 1
            if organisation.key in self.network.nodes[index]:
                if self.network.nodes[index][organisation.key] == organisation.value:
                    self.network.add_edge(index, self.node_number, relation=organisation.relation,sector=organisation.sector)
                    self.network.nodes[index][organisation.key] = organisation.value_change
                    logstring += str(index) + ", "
                    size -= 1
        if size != 0:
            if self.__verbose:
                print(logstring)
            self.log.append(logstring+ "\n")

    def generate_from_file(self,type,nodes,connectiviy,configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.network = networkx.Graph()
        self.node_number = 0
        self.create_singles()
        self.create_couples()
        self.create_families()
        for key in self.config["ORGANISATIONS"]:
            if self.config["ORGANISATIONS"].getboolean(key):
                self.create_organisations(Organisation(self.config[key]))
        return self.network

