import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
from ndlib.models.compartments.NodeStochastic import NodeStochastic
from ndlib.models.compartments.CountDown import CountDown
from ndlib.models.compartments.EdgeStochastic import EdgeStochastic

def generate_model(network):

    # model parameters
    infect_probability = 0.025
    incubation_time = 14
    incubation_probability = 0.5
    ill_probability = 0.5
    disease_time = 21
    recover_probability = 0.66

    # Composite Model instantiation
    model = gc.CompositeModel(network)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Contagious")
    model.add_status("Ill")
    #model.add_status("Hospitalized")
    model.add_status("Dead")
    model.add_status("Recovered")

    # if another node is contagious or ill, this node can get infected
    infect_condition_c = EdgeStochastic(infect_probability,"Contagious")
    model.add_rule("Susceptible", "Infected", infect_condition_c)
    infect_condition_i = EdgeStochastic(infect_probability, "Ill")
    model.add_rule("Susceptible", "Infected", infect_condition_i)
    # if infected, after incubation time there is a chance of becoming contagious
    incubation_time_condition = CountDown("incubation", iterations=incubation_time)
    incubation_probability_condition =  NodeStochastic(incubation_probability, composed=incubation_time_condition)
    model.add_rule("Infected", "Contagious", incubation_probability_condition)
    # if contagious, there is a chance of becoming ill
    ill_probability_condition = NodeStochastic(ill_probability, triggering_status="Contagious")
    model.add_rule("Infected", "Ill", ill_probability_condition)
    # if ill, after disease time there is a chance of becoming Recovered
    recover_time_condition = CountDown("incubation", iterations=disease_time)
    recover_probability_condition = NodeStochastic(recover_probability, composed=recover_time_condition)
    model.add_rule("Ill", "Recovered", recover_probability_condition)
    #  if ill, after disease time there is also chance of becoming Dead
    die_probability_condition = NodeStochastic((1 - recover_probability), composed=recover_time_condition)
    model.add_rule("Ill", "Dead", die_probability_condition)

    return model