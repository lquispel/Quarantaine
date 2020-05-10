
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

    def create_singles(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_singles"):
            logstring = "Qu Creating single: s" + str(self.node_number)
            if self.__verbose:
                print (logstring)
            self.log.append( logstring )
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_SINGLE")
            counter += 1
            self.node_number += 1

    def create_couples(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_couples"):
            logstring = "Qu Creating Couple: c" + str(self.node_number)
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="EMPLOYABLE",
                             living="LIVING_COUPLE")
            self.node_number += 1
            logstring += " s" + str(self.node_number)
            if self.__verbose:
                print(logstring)
            self.log.append(logstring + "\n" )
            self.network.add_node(self.node_number, type="person", state="SUSCEPTIBLE", age="ADULT", employable="UNEMPLOYABLE",
                             living="LIVING_COUPLE")
            self.node_number += 1
            self.network.add_edge(self.node_number - 1, self.node_number - 2, relation="LIVING_TOGETHER")
            counter += 1

    def create_families(self):
        counter = 0
        while counter < self.config["GENERAL"].getint("number_of_families"):
            logstring = "Qu: Creating family " + str(counter) + ": "
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
                            self.network.add_edge(number1, number2, relation="LIVING_TOGETHER")
            if self.__verbose:
                print(logstring)
            self.log.append(logstring + "\n")
            counter += 1

    def create_schools(self):
        school_size = 0
        school_count = 0
        for index in range(0, self.node_number - 1):
            if school_size == 0:
                if school_count:
                    if self.__verbose:
                        print(logstring)
                    self.log.append(logstring + "\n")
                self.network.add_node(self.node_number, type="school", state="OPEN")
                node = self.get_random_node("employable", "EMPLOYABLE")
                self.network.nodes[node]["employable"] = "EMPLOYED"
                self.network.add_edge(self.node_number, node, relation="EMPLOYMENT", sector="EDUCATION")
                school_count += 1
                logstring = "Qu: Creating school " + str(school_count) + ", u" + str(self.node_number) + ": teacher: " + str(node) + " pupils: "
                self.node_number += 1
                school_size = self.config["INSTITUTIONS"].getint("school_size")
            if self.network.nodes[index]["age"] == "CHILD":
                self.network.add_edge(index, self.node_number-1, relation="ATTENDING",sector="EDUCATION")
                school_size -= 1
                logstring += str(index) + ","
        if school_size != 0:
            if self.__verbose:
                print(logstring)
            self.log.append(logstring + "\n")
        return school_count

    def create_organisation(self,organisation_type,organisation_size,organisation_key,organisation_value,organisation_sector=""):
        organisation_count = 0
        size = 0
        logstring = ""
        for index in range(0, self.node_number - 1):
            if size == 0:
                if organisation_count:
                    if self.__verbose:
                        print(logstring)
                    self.log.append(logstring + "\n")
                size = organisation_size
                organisation_count += 1
                self.network.add_node(self.node_number, type=organisation_type, state="OPEN")
                logstring = "Qu: Creating " + str(organisation_type) + " organisation " + str(organisation_count) + ", o" + str(self.node_number) + " , members: "
                self.node_number += 1
            if organisation_key in self.network.nodes[index]:
                if self.network.nodes[index][organisation_key] == organisation_value:
                    self.network.add_edge(index, self.node_number, relation=organisation_type,sector=organisation_sector)
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
        if self.config["INSTITUTIONS"].getboolean("use_schools"):
            schools_created = self.create_schools()
        self.create_organisation("COMPANY",5,"employable","EMPLOYABLE")
        return self.network

