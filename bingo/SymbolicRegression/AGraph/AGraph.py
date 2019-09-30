"""Acyclic graph representation of an equation.


This module contains most of the code necessary for the representation of an
acyclic graph (linear stack) in symbolic regression. 
Stack
-----

The stack is represented as Nx3 integer array. Where each row of the array
corresponds to a single command with form:

========  ===========  ===========
Node      Parameter 1  Parameter 2
========  ===========  ===========

Where the parameters are a reference to the result of previously executed
commands (referenced by row number in the stack). The result of the last (N'th)
command in the stack is the evaluation of the equation.

Note: Parameter values have special meaning for two of the nodes (0 and 1).

Nodes
---------

An integer to node mapping is how the command stack is parsed.
The current map is outlined below.

========  =======================================  =================
Node      Name                                     Math
========  =======================================  =================
0         load p1'th column of x                   :math:`x_{p1}`
1         load p1'th constant                      :math:`c_{p1}`
2         addition                                 :math:`p1 + p2`
3         subtraction                              :math:`p1 - p2`
4         multiplication                           :math:`p1 - p2`
5         division (not divide-by-zero protected)  :math:`p1 / p2`
6         sine                                     :math:`sin(p1)`
7         cosine                                   :math:`cos(p1)`
8         exponential                              :math:`exp(p1)`
9         logarithm                                :math:`log(|p1|)`
10        power                                    :math:`|p1|^{p2}`
11        absolute value                           :math:`|p1|`
12        square root                              :math:`sqrt(|p1|)`
========  =======================================  =================
"""
import logging
import numpy as np

from .AGraphStringFormatting import get_formatted_string
from ..Equation import Equation
from ...Base import ContinuousLocalOptimization

try:
    from bingocpp.build import bingocpp as Backend
except ImportError:
    from . import Backend

LOGGER = logging.getLogger(__name__)

COMMAND_ARRAY_DTYPE = np.int16

class AGraph(Equation, ContinuousLocalOptimization.ChromosomeInterface):
    """Acyclic graph representation of an equation.

    Agraph is initialized with with empty command array and no constants.

    Attributes
    ----------
    command_array
    constants
    num_constants
    """
    def __init__(self):
        super().__init__()
        self._command_array = np.empty([0, 3],
                                       dtype=COMMAND_ARRAY_DTYPE)
        self._short_command_array = np.empty([0, 3],
                                             dtype=COMMAND_ARRAY_DTYPE)
        self._constants = []
        self._needs_opt = False
        self._command_array_signature = self._hash_command_array()
        self._constants_signature = self._hash_constants()

    @staticmethod
    def is_cpp():
        return False

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._update_graph()
        self._fit_set = True
        self._fitness = value

    @property
    def fit_set(self):
        self._update_graph()
        return self._fit_set

    @property
    def num_constants(self):
        self._update_graph()
        return len(self._constants)

    @property
    def constants(self):
        return self._constants

    @constants.setter
    def constants(self, constants):
        self._constants = constants

    @property
    def command_array(self):
        """Nx3 array of int: acyclic graph stack.

        Notes
        -----
        Setting the command stack automatically resets fitness
        """
        return self._command_array

    @command_array.setter
    def command_array(self, command_array):
        self._command_array = command_array

    @property
    def needs_continuous_opt(self):
        """Does the individual need local optimization"""
        self._update_graph()
        return self._needs_opt

    @needs_continuous_opt.setter
    def needs_continuous_opt(self, value):
        self._update_graph()
        self._needs_opt = value

    def get_utilized_commands(self):
        """"Find which commands are utilized.

        Find the commands in the command array of the agraph upon which the
        last command relies. This is inclusive of the last command.

        Returns
        -------
        list of bool of length N
            Boolean values for whether each command is utilized.
        """
        self._update_graph()
        return Backend.get_utilized_commands(self._command_array)

    def get_number_local_optimization_params(self):
        """number of parameters for local optimization

        Returns
        -------
        int
            Number of constants that need to be optimized
        """
        return self.num_constants

    def set_local_optimization_params(self, params):
        """Set the local optimization parameters.

        Parameters
        ----------
        params : list of numeric
                 Values to set constants
        """
        self._constants = list(params)

    def evaluate_equation_at(self, x):
        """Evaluation of the AGraph equation at points x.

        Parameters
        ----------
        x : MxD array of numeric.
            Values at which to evaluate the equations. D is the number of
            dimensions in x and M is the number of data points in x.

        Returns
        -------
        Mx1 array of numeric
            :math:`f(x)`
        """
        self._update_graph()
        try:
            f_of_x = Backend.evaluate(self._short_command_array,
                                      x, self._constants)
            return f_of_x
        except (ArithmeticError, OverflowError, ValueError,
                FloatingPointError) as err:
            LOGGER.warning("%s in stack evaluation", err)
            return np.full(x.shape, np.nan)

    def evaluate_equation_with_x_gradient_at(self, x):
        """Evaluate Agraph and get its derivatives.

        Evaluate the AGraph equation at x and the gradient of x.

        Parameters
        ----------
        x : MxD array of numeric.
            Values at which to evaluate the equations. D is the number of
            dimensions in x and M is the number of data points in x.

        Returns
        -------
        tuple(Mx1 array of numeric, MxD array of numeric)
            :math:`f(x)` and :math:`df(x)/dx_i`
        """
        self._update_graph()
        try:
            f_of_x, df_dx = Backend.evaluate_with_derivative(
                self._short_command_array, x, self._constants, True)
            return f_of_x, df_dx
        except (ArithmeticError, OverflowError, ValueError,
                FloatingPointError) as err:
            LOGGER.warning("%s in stack evaluation/deriv", err)
            nan_array = np.full(x.shape, np.nan)
            return nan_array, np.array(nan_array)

    def evaluate_equation_with_local_opt_gradient_at(self, x):
        """Evaluate Agraph and get its derivatives.

        Evaluate the AGraph equation at x and get the gradient of constants.
        Constants are of length L.

        Parameters
        ----------
        x : MxD array of numeric.
            Values at which to evaluate the equations. D is the number of
            dimensions in x and M is the number of data points in x.

        Returns
        -------
        tuple(Mx1 array of numeric, MxL array of numeric)
            :math:`f(x)` and :math:`df(x)/dc_i`
        """
        self._update_graph()
        try:
            f_of_x, df_dc = Backend.evaluate_with_derivative(
                self._short_command_array, x, self._constants, False)
            return f_of_x, df_dc
        except (ArithmeticError, OverflowError, ValueError,
                FloatingPointError) as err:
            LOGGER.warning("%s in stack evaluation/const-deriv", err)
            nan_array = np.full((x.shape[0], len(self._constants)), np.nan)
            return nan_array, np.array(nan_array)

    def __str__(self):
        """Console string output of Agraph equation.

        Returns
        -------
        str
            equation in console form
        """
        self._update_graph()
        return get_formatted_string("console", self._short_command_array,
                                    self._constants)

    def get_latex_string(self):
        """Latex interpretable version of Agraph equation.

        Returns
        -------
        str
            Equation in latex form
        """
        self._update_graph()
        return get_formatted_string("latex", self._short_command_array,
                                    self._constants)

    def get_console_string(self):
        """Console version of Agraph equation.

        Returns
        -------
        str
            Equation in simple form
        """
        self._update_graph()
        return get_formatted_string("console", self._short_command_array,
                                    self._constants)

    def get_stack_string(self):
        """Stack output of Agraph equation.

        Returns
        -------
        str
            equation in stack form and simplified stack form
        """
        self._update_graph()
        print_str = "---full stack---\n"
        print_str += get_formatted_string("stack", self._command_array,
                                          self._constants)
        print_str += "---small stack---\n"
        print_str += get_formatted_string("stack", self._short_command_array,
                                          self._constants)
        return print_str

    def get_complexity(self):
        """Calculate complexity of AGraph equation.

        Returns
        -------
        int
            number of utilized commands in stack
        """
        self._update_graph()
        return self._short_command_array.shape[0]

    def distance(self, chromosome):
        """Computes the distance to another Agraph

        Distance is a measure of similarity of the two command_arrays

        Parameters
        ----------
        chromosome : Agraph
                     The individual to which distance will be calculated

        Returns
        -------
         : int
            distance from self to individual
        """
        dist = np.sum(self.command_array != chromosome.command_array)
        return dist

    def __deepcopy__(self, memodict=None):
        duplicate = AGraph()
        self._copy_agraph_values_to_new_graph(duplicate)
        return duplicate

    def _copy_agraph_values_to_new_graph(self, agraph_duplicate):
        agraph_duplicate._genetic_age = self._genetic_age
        agraph_duplicate._fitness = self._fitness
        agraph_duplicate._fit_set = self._fit_set
        agraph_duplicate._command_array = np.copy(self.command_array)
        agraph_duplicate._short_command_array = \
            np.copy(self._short_command_array)
        agraph_duplicate._constants = list(self._constants)
        agraph_duplicate._needs_opt = self._needs_opt
        agraph_duplicate._command_array_signature = \
            self._command_array_signature
        agraph_duplicate._constants_signature = self._constants_signature

    def _update_graph(self):
        command_array_signature = self._hash_command_array()
        constants_signature = self._hash_constants()
        if self._command_array_signature != command_array_signature:
            self._process_modified_command_array()
            self._fit_set = False
            self._fitness = None
            # self._needs_opt = True
            self._command_array_signature = command_array_signature
        if self._constants_signature != constants_signature:
            self._fit_set = False
            self._fitness = None
            self._needs_opt = True
            self._constants_signature = constants_signature

    def _has_command_array_been_modified(self):
        return self._command_array_signature != self._hash_command_array()

    def _has_constants_been_modified(self):
        return self._constants_signature != self._hash_constants()

    def _hash_command_array(self):
        return hash(self._command_array.data.tobytes())

    def _hash_constants(self):
        return hash(tuple(self._constants))

    def _process_modified_command_array(self):
        inserted_constants = self._renumber_constants()
        if len(inserted_constants) > 0:
            self._needs_opt = True
        self._short_command_array = Backend.simplify_stack(self._command_array)

    def _renumber_constants(self):
        util = Backend.get_utilized_commands(self._command_array)
        const_num = 0
        inserted_constants = []
        new_constants = []
        const_commands = self._command_array[:, 0] == 1
        used_const_commands = np.logical_and(const_commands, util)
        unused_const_commands = np.logical_and(const_commands,
                                               np.logical_not(util))
        self._command_array[unused_const_commands] = (1, -1, -1)
        for i, used in enumerate(used_const_commands):
            if used:
                if self._command_array[i, 1] == -1:
                    new_const = 0.
                    inserted_constants.append(const_num)
                else:
                    new_const = self._constants[self._command_array[i, 1]]
                new_constants.append(new_const)
                self._command_array[i] = (1, const_num, const_num)
                const_num += 1
        self._constants = new_constants
        return inserted_constants

    def find_inserted_constants(self):
        return self._renumber_constants()
