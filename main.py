from classes.ilm import Ilm
import matplotlib.pyplot as plt
from classes.language_parameters import LanguageParameters
import statistics
import os
DIRNAME = os.path.dirname(__file__)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a" + str(i) for i in range(1, 6)]
B_COMP = ["b" + str(i) for i in range(1, 6)]
MEANINGS = [(x, y) for x in A_COMP for y in B_COMP]


def basic_single_language_check(name, exposure, pop_size):
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)

    sizes = []
    regularities = []
    generations = []

    ilm = Ilm(l_parameters, pop_size, exposure)

    for i in range(50):
        ilm.run_single_generation()
        sizes.append(ilm.populations["BASE"].average_grammar_size())
        regularities.append(ilm.populations["BASE"].regularity())
        generations.append(ilm.gen)

    plt.figure(str(name) + "-0")
    plt.plot(generations, regularities)
    plt.xlabel('Generation')
    plt.ylabel('Regularity')
    plt.title('Language regularity at each generation of the ILM')
    reg_filename = os.path.join(DIRNAME, "graphs/Regularities-" + str(name))
    plt.savefig(reg_filename)

    plt.figure(str(name) + "-1")
    plt.plot(generations, sizes)
    plt.xlabel('Generation')
    plt.ylabel('Size')
    plt.title('Language grammar size at each generation of the ILM')
    size_filename = os.path.join(DIRNAME, "graphs/Sizes-" + str(name))
    plt.savefig(size_filename)


def ratio_test(a_amount, l_parameters):
    ilm = Ilm(l_parameters, 6, 100)

    ilm.split_population("BASE")
    ilm.run_generations(50)
    final_a_e_language = ilm.populations["BASE-A"].current_e_language()
    final_b_e_language = ilm.populations["BASE-B"].current_e_language()

    ilm.merge_populations("BASE-A", "BASE-B", "MERGED", a_amount)
    ilm.run_generations(50)
    final_merged_e_language = ilm.populations["MERGED"].current_e_language()

    results = [ilm.multi_language_conformity(final_a_e_language, final_merged_e_language),
               ilm.multi_language_conformity(final_b_e_language, final_merged_e_language)]

    return results


def exposure_test(number_of_agents):
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    exposures = []
    convergences = []
    for i in range(1, 51):
        exposures.append(i)
        convergence = 0
        for j in range(10):
            ilm = Ilm(l_parameters, number_of_agents, i)
            ilm.run_generations(50)
            if ilm.populations["BASE"].has_converged():
                convergence += 1
        convergences.append(convergence/10)

    plt.figure(0)
    plt.plot(exposures, convergences)
    plt.xlabel('Exposure')
    plt.ylabel('Proportion of languages converged after 30 generations')
    plt.title('Convergence of lanuguages relative to exposure')
    dom_filename = os.path.join(DIRNAME, "graphs/convergence")
    plt.savefig(dom_filename)


def dominance_graphs(number_of_agents):
    a_amounts = []
    avg_a_dominances = []
    avg_b_dominances = []
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)

    for i in range(number_of_agents+1):
        a_amount = i
        a_dominances = []
        b_dominances = []
        for j in range(10):
            a_b_dom = ratio_test(a_amount, l_parameters)
            a_dominances.append(a_b_dom[0])
            b_dominances.append(a_b_dom[1])
        avg_a_dominances.append(statistics.mean(a_dominances))
        avg_b_dominances.append(statistics.mean(b_dominances))
        a_amounts.append(a_amount)

    plt.figure(0)
    plt.plot(a_amounts, avg_a_dominances)
    plt.plot(a_amounts, avg_b_dominances)
    plt.xlabel('Proportion of A')
    plt.ylabel('Dominance of each language')
    plt.title('Dominance of languages based on proportion')
    dom_filename = os.path.join(DIRNAME, "graphs/dominance")
    plt.savefig(dom_filename)

def average_time_to_converge(number_of_agents, exposure):
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    total = 0
    for i in range(100):
        ilm = Ilm(l_parameters, number_of_agents, exposure)
        for j in range(500):
            ilm.run_single_generation()
            if ilm.populations["BASE"].has_converged():
                print(ilm.gen)
                total += (ilm.gen - 5)
                break
        if ilm.gen >= 199:
            total += ilm.gen
    print(total/100)
    return total/100


def exposure_graph(number_of_agents):
    exposures = []
    convergence_times = []
    for i in range(100):
        exposures.append(i)
        convergence_times.append(average_time_to_converge(number_of_agents, i))

    print(exposures)
    print(convergence_times)

    plt.figure(0)
    plt.plot(exposures, convergence_times)
    plt.xlabel('Exposure')
    plt.ylabel('Avg. time taken to converge')
    plt.title('Change in convergence time with respect to exposure')
    plt.savefig("graphs/convergence_times")


def single_ilm(number_of_agents, number_of_generations, exposure):
    # a_freq = {"a1": 100, "a2": 20, "a3": 15, "a4": 10, "a5": 1}
    # b_freq = {"b1": 100, "b2": 20, "b3": 15, "b4": 10, "b5": 1}
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    ilm = Ilm(l_parameters, number_of_agents, exposure)
    generations = []
    sizes = []
    regularities = []
    for i in range(number_of_generations):
        ilm.run_single_generation()
        generations.append(ilm.gen)
        sizes.append(ilm.populations["BASE"].average_grammar_size())
        regularities.append(ilm.populations["BASE"].regularity())

    print(regularities)
    print(sizes)

    plt.figure(0)
    plt.plot(generations, regularities)
    plt.xlabel('Generation')
    plt.ylabel('Regularity')
    plt.title('Language regularity at each generation of the ILM')
    plt.savefig("graphs/regularities")

    plt.figure(1)
    plt.plot(generations, sizes)
    plt.xlabel('Generation')
    plt.ylabel('Size')
    plt.title('Average grammar size at each generation of the ILM')
    plt.savefig("graphs/sizes")


def setup():
    for filename in os.listdir(os.path.join(DIRNAME, "graphs")):
        os.remove(os.path.join(DIRNAME, "graphs/" + filename))


setup()
exposure_graph(1)
