import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
# import ndlib.models.compartments.NodeStochastic as ns
# import ndlib.models.compartments.CountDown as cd
import ndlib.models.compartments.EdgeStochastic as es

def generate_model(network):

    # model parameters
    infect_probability = 0.025
    incubation_time = 14
    incubation_probability = 0.5

    # Composite Model instantiation
    model = gc.CompositeModel(network)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Contagious")
    model.add_status("Ill")
    model.add_status("Hospitalized")
    model.add_status("Dead")
    model.add_status("Recovered")

    # edge conditions
    infect_condition = es.EdgeStochastic(infect_probability,"Contagious")
    # time conditions
    # incubation_time_condition = cd.CountDown("incubation", iterations=incubation_time)
    # incubation_probability =  ns.NodeStochastic(incubation_probability, composed=incubation_time_condition)
    # incubation_probability = ns.NodeStochastic(incubation_probability,triggering)

     # Rule definition
    model.add_rule("Susceptible", "Infected", infect_condition)
   # model.add_rule("Infected", "Contagious", incubation_probability)

    # model.add_rule("Contagious", "Ill", c2)
    # model.add_rule("Ill", "Hospitalized", c2)
    # model.add_rule("Hospitalized", "Dead", c2)
    # model.add_rule("Dead", "Recovered" c2)

    return model