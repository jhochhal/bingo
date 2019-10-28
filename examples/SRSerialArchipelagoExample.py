# Ignoring some linting rules in tests
# pylint: disable=redefined-outer-name
# pylint: disable=missing-docstring
import numpy as np

from bingo.symbolic_regression.agraph.crossover import AGraphCrossover
from bingo.symbolic_regression.agraph.mutation import AGraphMutation
from bingo.symbolic_regression.agraph.generator import AGraphGenerator
from bingo.symbolic_regression.agraph.component_generator \
    import ComponentGenerator
from bingo.symbolic_regression.explicit_regression \
    import ExplicitRegression, ExplicitTrainingData

from bingo.evolutionary_algorithms.age_fitness import AgeFitnessEA
from bingo.evolutionary_optimizers.serial_archipelago import SerialArchipelago
from bingo.evaluation.evaluation import Evaluation
from bingo.evolutionary_optimizers.island import Island
from bingo.local_optimizers.continuous_local_opt\
    import ContinuousLocalOptimization

POP_SIZE = 100
STACK_SIZE = 10


def init_x_vals(start, stop, num_points):
    return np.linspace(start, stop, num_points).reshape([-1, 1])


def equation_eval(x):
    return x**2 + 3.5*x**3


def main():
    x = init_x_vals(-10, 10, 100)
    y = equation_eval(x)
    training_data = ExplicitTrainingData(x, y)

    component_generator = ComponentGenerator(x.shape[1])
    component_generator.add_operator(2)
    component_generator.add_operator(3)
    component_generator.add_operator(4)

    crossover = AGraphCrossover(component_generator)
    mutation = AGraphMutation(component_generator)

    agraph_generator = AGraphGenerator(STACK_SIZE, component_generator)

    fitness = ExplicitRegression(training_data=training_data)
    local_opt_fitness = ContinuousLocalOptimization(fitness, algorithm='lm')
    evaluator = Evaluation(local_opt_fitness)

    ea = AgeFitnessEA(evaluator, agraph_generator, crossover,
                      mutation, 0.4, 0.4, POP_SIZE)

    island = Island(ea, agraph_generator, POP_SIZE)
    archipelago = SerialArchipelago(island, num_islands=2)

    evo_result = archipelago.evolve_until_convergence(max_generations=500,
                                                      fitness_threshold=1.0e-4)
    if evo_result.success:
        print("best_individual: ", archipelago.get_best_individual())
        print("fitness: ", archipelago.get_best_fitness())
        print("number of generations: ", evo_result.ngen)
    else:
        print("Failed.")


if __name__ == '__main__':
    main()
