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

    plt.figure(0)
    plt.plot(a_amounts, avg_a_dominances)
    plt.plot(a_amounts, avg_b_dominances)
    plt.xlabel('Proportion of A')
    plt.ylabel('Dominance of each language')
    plt.title('Dominance of languages based on proportion')
    dom_filename = os.path.join(DIRNAME, "graphs/dominance")
    plt.savefig(dom_filename)


def setup():
    for filename in os.listdir(os.path.join(DIRNAME, "graphs")):
        os.remove(os.path.join(DIRNAME, "graphs/" + filename))


# setup()
# for i in range(1):
#     basic_single_language_check(i, 100, 10)

dominance_graphs(6)

# ilm = Ilm(1, 50, A_COMP, B_COMP, ALPHABET)
# ilm.split_population("BASE")
#
# a_sizes = []
# a_regularities = []
# b_sizes = []
# b_regularities = []
# generations = []
#
# for i in range(50):
#     old_a_e_language = ilm.population_e_language(ilm.populations["BASE-A"])
#     old_b_e_language = ilm.population_e_language(ilm.populations["BASE-B"])
#     ilm.run_single_generation()
#     new_a_e_language = ilm.population_e_language(ilm.populations["BASE-A"])
#     new_b_e_language = ilm.population_e_language(ilm.populations["BASE-B"])
#     generations.append(ilm.gen)
#     a_regularities.append(ilm.multi_language_conformity(old_a_e_language, new_a_e_language))
#     a_sizes.append(ilm.population_grammar_size("BASE-A"))
#     b_regularities.append(ilm.multi_language_conformity(old_b_e_language, new_b_e_language))
#     b_sizes.append(ilm.population_grammar_size("BASE-B"))
#
# final_a_e_language = ilm.population_e_language(ilm.populations["BASE-A"])
# final_b_e_language = ilm.population_e_language(ilm.populations["BASE-B"])
# ilm.merge_populations("BASE-A", "BASE-B", "MERGED", 0)
#
# more_generations = []
# merged_regularities = []
# merged_sizes = []
#
# for i in range(50):
#     old_e_language = ilm.population_e_language(ilm.populations["MERGED"])
#     ilm.run_single_generation()
#     new_e_language = ilm.population_e_language(ilm.populations["MERGED"])
#     more_generations.append(ilm.gen)
#     merged_regularities.append(ilm.multi_language_conformity(old_e_language, new_e_language))
#     merged_sizes.append(ilm.population_grammar_size("MERGED"))
#
# final_merged_e_language = ilm.population_e_language(ilm.populations["MERGED"])
#
# print("Similarity to language A - " + str(ilm.multi_language_conformity(final_a_e_language, final_merged_e_language)))
# print("Similarity to language B - " + str(ilm.multi_language_conformity(final_b_e_language, final_merged_e_language)))


# plt.figure(0)
# plt.plot(generations, a_regularities)
# plt.xlabel('Generation')
# plt.ylabel('Regularity')
# plt.title('Language A regularity at each generation of the ILM')
# plt.savefig("graphs/A-Regularities")
#
# plt.figure(1)
# plt.plot(generations, a_sizes)
# plt.xlabel('Generation')
# plt.ylabel('Size')
# plt.title('Language A Grammar size at each generation of the ILM')
# plt.savefig("graphs/A-Sizes")
#
# plt.figure(2)
# plt.plot(generations, b_regularities)
# plt.xlabel('Generation')
# plt.ylabel('Regularity')
# plt.title('Language B regularity at each generation of the ILM')
# plt.savefig("graphs/B-Regularities")
#
# plt.figure(3)
# plt.plot(generations, b_sizes)
# plt.xlabel('Generation')
# plt.ylabel('Size')
# plt.title('Language B Grammar size at each generation of the ILM')
# plt.savefig("graphs/B-Sizes")
#
# plt.figure(4)
# plt.plot(more_generations, merged_regularities)
# plt.xlabel('Generation')
# plt.ylabel('Regularity')
# plt.title('Merged Language Grammar regularities at each generation of the ILM')
# plt.savefig("graphs/M-Regularities")
#
# plt.figure(5)
# plt.plot(more_generations, merged_sizes)
# plt.xlabel('Generation')
# plt.ylabel('Size')
# plt.title('Merged Language Grammar size at each generation of the ILM')
# plt.savefig("graphs/M-Sizes")