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


def ratio_test(number_of_agents, a_amount, l_parameters):
    ilm = Ilm(l_parameters, number_of_agents, 100)

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


def dominance_graphs(number_of_agents, sample_size):
    a_amounts = []
    avg_a_dominances = []
    avg_b_dominances = []
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)

    for i in range(number_of_agents+1):
        a_amount = i
        a_dominances = []
        b_dominances = []
        for j in range(sample_size):
            a_b_dom = ratio_test(number_of_agents, a_amount, l_parameters)
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
    plt.savefig("graphs/dominance.svg", format="svg")


def average_time_to_converge(number_of_agents, exposure):
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    total_time = 0
    total_size = 0
    for i in range(10):
        ilm = Ilm(l_parameters, number_of_agents, exposure)
        for j in range(500):
            ilm.run_single_generation()
            if ilm.populations["BASE"].has_converged():
                print(ilm.gen)
                total_time += (ilm.gen - 5)
                total_size += ilm.populations["BASE"].average_grammar_size()
                break
        if ilm.gen >= 400:
            total_time += ilm.gen
    print(total_time/10)
    print(total_size/10)
    return total_time/10, total_size/10


def population_graph():
    convergence_times = []
    pop_size = []
    for i in range(1, 6):
        pop_size.append(i)
        convergence_times.append(average_time_to_converge(i, 50))
    plt.figure(0)
    plt.plot(pop_size, convergence_times)
    plt.xlabel('Population Size')
    plt.ylabel('Avg. time taken to converge')
    plt.title('Change in convergence time with respect to exposure')
    plt.savefig("graphs/convergence_times.svg", format="svg")
    print(pop_size)
    print(convergence_times)
    return


def exposure_graph(number_of_agents):
    exposures = []
    convergence_times = []
    average_sizes = []

    for i in range(16, 101):
        exposures.append(i)
        time, size = average_time_to_converge(number_of_agents, i)
        convergence_times.append(time)
        average_sizes.append(size)

    print(exposures)
    print(convergence_times)
    print(average_sizes)

    plt.figure(0)
    plt.plot(exposures, convergence_times)
    plt.xlabel('Exposure')
    plt.ylabel('Avg. time taken to converge')
    plt.title('Change in convergence time with respect to exposure')
    plt.savefig("graphs/convergence_times.svg", format="svg")

    plt.figure(1)
    plt.plot(exposures, average_sizes)
    plt.xlabel('Exposure')
    plt.ylabel('Avg. grammar size after convergence')
    plt.title('Change in grammar size with respect to exposure')
    plt.savefig("graphs/grammar_sizes.svg", format="svg")


def single_ilm(number_of_agents, number_of_generations, exposure):
    # a_freq = {"a1": 100, "a2": 20, "a3": 15, "a4": 10, "a5": 1}
    # b_freq = {"b1": 100, "b2": 20, "b3": 15, "b4": 10, "b5": 1}
    l_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    ilm = Ilm(l_parameters, number_of_agents, exposure)
    generations = []
    sizes = []
    regularities = []
    coherences = []
    for i in range(number_of_generations):
        ilm.run_single_generation()
        generations.append(ilm.gen)
        sizes.append(ilm.populations["BASE"].average_grammar_size())
        regularities.append(ilm.populations["BASE"].regularity())
        coherences.append(ilm.populations["BASE"].coherence())

    print(regularities)
    print(sizes)

    plt.figure(0)
    plt.plot(generations, regularities)
    plt.xlabel('Generation')
    plt.ylabel('Regularity')
    plt.title('Language regularity at each generation of the ILM')
    plt.savefig("graphs/regularities.svg", format="svg")

    plt.figure(1)
    plt.plot(generations, sizes)
    plt.xlabel('Generation')
    plt.ylabel('Size')
    plt.title('Average grammar size at each generation of the ILM')
    plt.savefig("graphs/sizes.svg", format="svg")

    plt.figure(2)
    plt.plot(generations, coherences)
    plt.xlabel('Generation')
    plt.ylabel('Coherence')
    plt.title('Population Coherence at each generation of the ILM')
    plt.savefig("graphs/coherences.svg", format="svg")


def meaning_freq_graph(number_of_agents, sample_size):
    freq_dists = [
        {"a1": 20, "a2": 15, "a3": 10, "a4": 5, "a5": 0},
        {"a1": 15, "a2": 13, "a3": 10, "a4": 7, "a5": 5},
        {"a1": 10, "a2": 10, "a3": 10, "a4": 10, "a5": 10},
        {"a1": 5, "a2": 7, "a3": 10, "a4": 13, "a5": 15},
        {"a1": 0, "a2": 5, "a3": 10, "a4": 15, "a5": 20}
    ]

    a_dist = freq_dists[4]
    b_dist = freq_dists[0]
    dist_indexes = []
    a_doms = []
    b_doms = []
    for i in range(5):
        dist_indexes.append(i)
        final_dist = freq_dists[i]
        total_a_dom = 0
        total_b_dom = 0
        for j in range(sample_size):
            a_dom, b_dom = meaning_freq_test(number_of_agents, a_dist, b_dist, final_dist)
            total_a_dom += a_dom
            total_b_dom += b_dom
        a_doms.append(total_a_dom/sample_size)
        b_doms.append(total_b_dom/sample_size)

    print(a_doms)
    print(b_doms)

    plt.figure(0)
    plt.plot(dist_indexes, a_doms)
    plt.plot(dist_indexes, b_doms)
    plt.xlabel('Frequency Distribution Index')
    plt.ylabel('Language Dominance')
    plt.title('Dominance of languages based on meaning frequencies')
    plt.savefig("graphs/freqs.svg", format="svg")


def meaning_freq_test(number_of_agents, aa_freqs, ab_freqs, merge_freqs):
    base = LanguageParameters(ALPHABET, A_COMP, B_COMP)
    a_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP, aa_freqs)
    b_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP, ab_freqs)
    end_parameters = LanguageParameters(ALPHABET, A_COMP, B_COMP, merge_freqs)

    ilm = Ilm(base, number_of_agents, 50)
    ilm.split_population("BASE")
    ilm.populations["BASE-A"].set_parameters(a_parameters)
    ilm.populations["BASE-B"].set_parameters(b_parameters)

    ilm.run_generations(50)

    a_language = ilm.populations["BASE-A"].current_e_language()
    b_language = ilm.populations["BASE-B"].current_e_language()

    ilm.merge_populations("BASE-A", "BASE-B", "MERGED", int(number_of_agents/2))
    ilm.populations["MERGED"].set_parameters(end_parameters)

    ilm.run_generations(50)

    final_language = ilm.populations["MERGED"].current_e_language()

    a_dominance = ilm.multi_language_conformity(a_language, final_language)
    b_dominance = ilm.multi_language_conformity(b_language, final_language)

    print(ilm.multi_language_conformity(a_language, final_language))
    print(ilm.multi_language_conformity(b_language, final_language))

    return a_dominance, b_dominance


def setup():
    for filename in os.listdir(os.path.join(DIRNAME, "graphs")):
        os.remove(os.path.join(DIRNAME, "graphs/" + filename))


def plot_graph(x_values, y_values):
    plt.figure(1)
    plt.plot(x_values, y_values)
    plt.xlabel('Exposure')
    plt.ylabel('Avg number of generations to converge')
    plt.title('Avg. time taken to converge vs exposure')
    plt.savefig("graphs/generated", format="svg")


def plot_double_graph(x_values, other_y_values, y_values):
    plt.figure(1)
    plt.plot(x_values, y_values)
    plt.plot(x_values, other_y_values)
    plt.xlabel('Frequency Distribution')
    plt.ylabel('Language Dominance')
    plt.title('Dominance of Language for meaning frequencies')
    plt.savefig("graphs/freqs.svg", format="svg")

# y = [65.7, 71.2, 52.9, 69.6, 44.1, 108.6, 55.9, 49.5, 50.2, 24.7, 46.8, 25.4, 24.3, 34.7, 18.3, 32.0, 24.0, 30.1, 29.6, 33.1, 48.8, 40.9, 20.6, 60.5, 42.4, 36.4, 45.6, 40.3, 21.4, 28.9, 34.9, 33.4, 33.4, 30.0, 25.7, 23.0, 32.0, 21.9, 31.1, 33.7, 26.4, 32.5, 21.7, 26.7, 29.2, 17.0, 25.7, 24.6, 9.8, 22.2, 12.7, 21.9, 15.0, 18.7, 17.7, 7.8, 18.1, 9.6, 15.4, 10.8, 5.3, 7.1, 4.2, 4.7, 10.6, 8.1, 5.1, 7.6, 4.1, 2.1, 2.8, 2.9, 3.2, 1.8, 2.5, 1.6, 1.4, 2.3, 0.7, 1.2, 0.4, 2.2, 0.6, 0.7]
# x = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]


# aa_freq = {"a1": 20, "a2": 15, "a3": 10, "a4": 5, "a5": 0}
# ba_freq = {"a1": 0, "a2": 5, "a3": 10, "a4": 15, "a5": 20}
#
# x = [0,1,2,3,4]
# a_dom = [0.9040000000000001, 0.27999999999999997, 0.196, 0.44799999999999995, 0.304]
# b_dom = [0.144, 0.42399999999999993, 0.34800000000000003, 0.33199999999999996, 0.7000000000000001]

setup()
# plot_double_graph(x, a_dom, b_dom)
# meaning_freq_test(2, aa_freq, ba_freq, aa_freq)
# meaning_freq_graph(2)
# dominance_graphs(2, 1)
single_ilm(1, 100, 50)
# population_graph()
# plot_graph(x, y)
# exposure_graph(1)
