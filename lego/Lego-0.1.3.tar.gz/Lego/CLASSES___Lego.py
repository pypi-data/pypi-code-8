from copy import deepcopy
import itertools
from numpy import allclose, ndarray, ones
from MBALearnsToCode.Functions.FUNCTIONS___zzzUtility import approx_gradients


class Piece:
    def __init__(self, forwards={}, backwards={}):
        forwards = deepcopy(forwards)   # just to be careful #
        backwards = deepcopy(backwards)   # just to be careful #
        self.forwards = forwards
        self.forward_from_keys = set()
        self.forward_to_keys = set(forwards)
        self.forwards_to_from = {}
        self.backwards = backwards
        self.backward_from_keys = set()
        self.backward_to_keys = set(backwards)
        self.backwards_to_from = {}
        if forwards:
            for forward_to_key, lambda_and_arg_keys_and_forward_from_keys in forwards.items():
                forward_from_keys = set(lambda_and_arg_keys_and_forward_from_keys[1].values())
                self.forward_from_keys.update(forward_from_keys)
                self.forwards_to_from[forward_to_key] = forward_from_keys
        if backwards:
            for backward_to_key, lambda_and_arg_keys_and_backward_from_keys in backwards.items():
                backward_from_keys = set(lambda_and_arg_keys_and_backward_from_keys[1].values())
                self.backward_from_keys.update(backward_from_keys)
                self.backwards_to_from[backward_to_key] = backward_from_keys

    def install(self, change_keys={}, change_vars={}):
        forwards = {}
        for forward_to_key, forward_lambda_and_arg_keys_and_from_keys in self.forwards.items():
            new_forward_to_key = change_piece_key_or_var_in_piece_key(forward_to_key, change_keys, change_vars)
            forward_lambda, forward_arg_keys_and_from_keys =\
                deepcopy(forward_lambda_and_arg_keys_and_from_keys)   # just to be careful #
            for forward_arg_key, forward_from_key in forward_arg_keys_and_from_keys.items():
                forward_arg_keys_and_from_keys[forward_arg_key] =\
                    change_piece_key_or_var_in_piece_key(forward_from_key, change_keys, change_vars)
            forwards[new_forward_to_key] = [forward_lambda, forward_arg_keys_and_from_keys]
        backwards = {}
        for backward_to_key, backward_lambda_and_arg_keys_and_from_keys in self.backwards.items():
            new_backward_to_key = change_piece_key_or_var_in_piece_key(backward_to_key, change_keys, change_vars)
            backward_lambda, backward_arg_keys_and_from_keys =\
                deepcopy(backward_lambda_and_arg_keys_and_from_keys)   # just to be careful #
            for backward_arg_key, backward_from_key in backward_arg_keys_and_from_keys.items():
                backward_arg_keys_and_from_keys[backward_arg_key] =\
                    change_piece_key_or_var_in_piece_key(backward_from_key, change_keys, change_vars)
            backwards[new_backward_to_key] = [backward_lambda, backward_arg_keys_and_from_keys]
        return Piece(forwards, backwards)

    def run(self, dict_object, forwards='all', backwards=None):
        dict_object = deepcopy(dict_object)   # just to be careful #
        forwards = deepcopy(forwards)   # just to be careful #
        backwards = deepcopy(backwards)   # just to be careful #
        if forwards:
            if forwards == 'all':
                forward_to_keys = self.forward_to_keys
            else:
                forward_to_keys = forwards.intersection(self.forward_to_keys)
            for forward_to_key in forward_to_keys:
                forward_lambda, forward_arg_keys_and_from_keys = self.forwards[forward_to_key]
                forward_args = {}
                for forward_arg_key, forward_from_key in forward_arg_keys_and_from_keys.items():
                    if isinstance(forward_from_key, tuple):
                        var, index = forward_from_key
                        if var in dict_object:
                            forward_args[forward_arg_key] = dict_object[var][index]
                    elif forward_from_key in dict_object:
                        forward_args[forward_arg_key] = dict_object[forward_from_key]
                value = forward_lambda(**forward_args)
                if isinstance(forward_to_key, tuple):
                    var, index = forward_to_key
                    if var in dict_object:
                        dict_object[var][index] = value
                    else:
                        dict_object[var] = {index: value}
                else:
                    dict_object[forward_to_key] = value
        if backwards:
            d_key, backward_to_keys = backwards
            if backward_to_keys:
                list1 = list(map(lambda k: ('DOVERD', k), backward_to_keys))
                list2 = list(map(lambda k: ('DOVERD', d_key, k), backward_to_keys))
                backward_to_keys = set(list1 + list2).intersection(self.backward_to_keys)
            else:
                backward_to_keys = self.backward_to_keys
            for backward_to_key in backward_to_keys:
                backward_lambda, backward_arg_keys_and_from_keys = self.backwards[backward_to_key]
                backward_args = {}
                for backward_arg_key, backward_from_key in backward_arg_keys_and_from_keys.items():
                    if is_doverd(backward_from_key):
                        over_d_key = backward_from_key[2]
                        if isinstance(over_d_key, tuple):
                            var, index = over_d_key
                            if var in dict_object:
                                backward_args[backward_arg_key] = dict_object[('DOVERD', d_key, var)][index]
                        elif over_d_key in dict_object:
                            backward_args[backward_arg_key] = dict_object[('DOVERD', d_key, over_d_key)]
                    elif is_overd(backward_from_key):
                        over_d_key = backward_from_key[1]
                        if isinstance(over_d_key, tuple):
                            var, index = over_d_key
                            if var in dict_object:
                                backward_args[backward_arg_key] = dict_object[('DOVERD', d_key, var)][index]
                        elif over_d_key in dict_object:
                            backward_args[backward_arg_key] = dict_object[('DOVERD', d_key, over_d_key)]
                    elif isinstance(backward_from_key, tuple):
                        var, index = backward_from_key
                        if var in dict_object:
                            backward_args[backward_arg_key] = dict_object[var][index]
                    elif backward_from_key in dict_object:
                        backward_args[backward_arg_key] = dict_object[backward_from_key]
                value = backward_lambda(**backward_args)
                if is_doverd(backward_to_key):
                    over_d_key = backward_to_key[2]
                elif is_overd(backward_to_key):
                    over_d_key = backward_to_key[1]
                if isinstance(over_d_key, tuple):
                    var, index = over_d_key
                    t = ('DOVERD', d_key, var)
                    if t in dict_object:
                        dict_object[t][index] = value
                    else:
                        dict_object[t] = {index: value}
                else:
                    dict_object[('DOVERD', d_key, over_d_key)] = value

        return dict_object

    def check_gradients(self, ins___dict):

        def sum_out(in___dict, to_key):
            d = deepcopy(ins___dict)   # just to be careful #
            for in_key, in_value in in___dict.items():
                d[in_key] = in_value
            out = self.run(d)[to_key]
            if isinstance(out, ndarray):
                return out.sum()
            else:
                return out

        outs = self.run(ins___dict)
        d_keys = set()
        d_sum_keys = set()
        for d_key in self.forward_to_keys:
            if isinstance(outs[d_key], float):
                for backward_to_key in self.backward_to_keys:
                    if is_doverd(backward_to_key) and (backward_to_key[1] == d_key):
                        d_keys.add(d_key)
            elif isinstance(outs[d_key], ndarray):
                outs[('DOVERD', 'SUM___' + d_key, d_key)] = ones(outs[d_key].shape)
                d_sum_keys.add(d_key)

        over_d_keys = set()
        for backward_to_key in self.backward_to_keys:
            if is_doverd(backward_to_key):
                over_d_keys.add(backward_to_key[2])
            elif is_overd(backward_to_key):
                over_d_keys.add(backward_to_key[1])

        for d_key in d_keys:
            outs = self.run(outs, forwards='', backwards=[d_key, over_d_keys])
        for d_sum_key in d_sum_keys:
            outs = self.run(outs, forwards='', backwards=['SUM___' + d_sum_key, over_d_keys])

        check = True
        for over_d_key, d_key in itertools.product(over_d_keys, d_keys):
            numerical_gradients = approx_gradients(lambda v: sum_out({over_d_key: v}, d_key),
                                                   ins___dict[over_d_key])
            check = check and allclose(numerical_gradients,
                                       outs[('DOVERD', d_key, over_d_key)],
                                       rtol=1.e-3, atol=1.e-6)
        for over_d_key, d_sum_key in itertools.product(over_d_keys, d_sum_keys):
            numerical_gradients = approx_gradients(lambda v: sum_out({over_d_key: v}, d_sum_key),
                                                   ins___dict[over_d_key])
            check = check and allclose(numerical_gradients,
                                       outs[('DOVERD', 'SUM___' + d_sum_key, over_d_key)],
                                       rtol=1.e-3, atol=1.e-6)

        return check


class Process:
    def __init__(self, *steps):
        self.vars = set()
        self.steps = []
        for step in steps:
            s = process_step_with_complete_specifications(step)
            piece = s[0]
            for forward_key in piece.forward_from_keys.union(piece.forward_to_keys):
                self.vars.add(var_from_forward_piece_key(forward_key))
            self.steps += [s]

    def add_steps(self, *steps):
        for step in steps:
            s = process_step_with_complete_specifications(step)
            piece = s[0]
            for forward_key in piece.forward_from_keys.union(piece.forward_to_keys):
                self.vars.add(var_from_forward_piece_key(forward_key))
            self.steps += [s]

    def install(self, change_vars={}):
        process = deepcopy(self)   # just to be careful #
        from_old_vars_to_new_vars___dict = deepcopy(change_vars)   # just to be careful #
        for old_var, new_var in change_vars.items():
            if old_var == new_var:
                del from_old_vars_to_new_vars___dict[old_var]
        if from_old_vars_to_new_vars___dict:
            steps = []
            for step in process.steps:
                old_piece, old_forward_to_keys, old_d_key_and_over_d_keys = step
                new_piece = old_piece.install(change_vars=from_old_vars_to_new_vars___dict)
                if old_forward_to_keys == 'all':
                    new_forward_to_keys = 'all'
                elif old_forward_to_keys:
                    new_forward_to_keys = set()
                    for old_forward_to_key in old_forward_to_keys:
                        new_forward_to_keys.add(change_var_in_piece_key(old_forward_to_key,
                                                                        from_old_vars_to_new_vars___dict))
                else:
                    new_forward_to_keys = None
                if old_d_key_and_over_d_keys:
                    old_d_key, old_over_d_keys = old_d_key_and_over_d_keys
                    new_d_key = change_var_in_piece_key(old_d_key, from_old_vars_to_new_vars___dict)
                    new_over_d_keys = set()
                    for old_over_d_key in old_over_d_keys:
                        new_over_d_keys.add(change_var_in_piece_key(old_over_d_key, from_old_vars_to_new_vars___dict))
                    new_d_key_and_over_d_keys = [new_d_key, new_over_d_keys]
                else:
                    new_d_key_and_over_d_keys = None
                steps += [new_piece, new_forward_to_keys, new_d_key_and_over_d_keys],
            process = Process(*steps)
        return process

    def run(self, dict_object, num_times=1):
        dict_object = deepcopy(dict_object)   # just to be careful #
        for t in range(num_times):
            for step in self.steps:
                piece, forward_to_keys, d_key_and_over_d_keys = step
                dict_object = piece.play(dict_object, forward_to_keys, d_key_and_over_d_keys)
        return dict_object


def connect_processes(*processes):
    process = deepcopy(processes[0])   # just to be careful #
    for p in processes[1:]:
        process.vars.update(p.vars)
        process.steps += p.steps
    return process


class Program:
    def __init__(self, pieces={}, processes={}):
        self.vars = set()
        self.pieces = pieces
        self.processes = processes
        for piece in pieces.values():
            for piece_key in piece.forward_from_keys.union(piece.forward_to_keys):
                self.vars.add(var_from_forward_piece_key(piece_key))

    def install(self, from_old_vars_to_new_vars___dict):
        pieces = {}
        for piece_name, piece in self.pieces.items():
            pieces[piece_name] = piece.install(change_vars=from_old_vars_to_new_vars___dict)
        processes = {}
        for process_name, process in self.processes.items():
            processes[process_name] = process.install(change_vars=from_old_vars_to_new_vars___dict)
        return Program(pieces, processes)

    def run(self, dict_object, *process_names_or_piece_names, **kwargs):
        dict_object = deepcopy(dict_object)   # just to be careful #
        for process_name_or_piece_name in process_names_or_piece_names:
            if process_name_or_piece_name in self.processes:
                process = self.processes[process_name_or_piece_name]
                dict_object = process.play(dict_object, **kwargs)
            elif process_name_or_piece_name in self.pieces:
                piece = self.pieces[process_name_or_piece_name]
                dict_object = piece.play(dict_object, **kwargs)
        return dict_object


class Project:
    def __init__(self):
        self.vars = {}
        self.pieces = {}
        self.processes = {}
        self.programs = {}

    def run(self, *process_names_or_piece_names, **kwargs):
        for process_name_or_piece_name in process_names_or_piece_names:
            if isinstance(process_name_or_piece_name, tuple) and (process_name_or_piece_name[0] in self.programs):
                program_name = process_name_or_piece_name[0]
                process_or_piece_name = process_name_or_piece_name[1]
                if process_or_piece_name in self.programs[program_name].processes:
                    process = self.programs[program_name].processes[process_or_piece_name]
                    self.vars = process.play(self.vars, **kwargs)
                elif process_or_piece_name in self.programs[program_name].pieces:
                    piece = self.programs[program_name].pieces[process_or_piece_name]
                    self.vars = piece.play(self.vars, **kwargs)
            elif process_name_or_piece_name in self.processes:
                process = self.processes[process_name_or_piece_name]
                self.vars = process.play(self.vars, **kwargs)
            elif process_name_or_piece_name in self.pieces:
                piece = self.pieces[process_name_or_piece_name]
                self.vars = piece.play(self.vars, **kwargs)


def is_doverd(piece_key):
    return isinstance(piece_key, tuple) and (piece_key[0] == 'DOVERD') and (len(piece_key) == 3)


def is_overd(piece_key):
    return isinstance(piece_key, tuple) and (piece_key[0] == 'DOVERD') and (len(piece_key) == 2)


def var_from_forward_piece_key(forward_piece_key):
    forward_piece_key = deepcopy(forward_piece_key)   # just to be careful #
    if isinstance(forward_piece_key, tuple):
        return forward_piece_key[0]
    else:
        return forward_piece_key


def change_piece_key(piece_key, from_old_keys_to_new_keys___dict):
    piece_key = deepcopy(piece_key)   # just to be careful #
    change_keys = deepcopy(from_old_keys_to_new_keys___dict)   # just to be careful #
    for old_key, new_key in from_old_keys_to_new_keys___dict.items():
        if old_key == new_key:
            del change_keys[old_key]
    if change_keys:
        if is_doverd(piece_key):
            d_key, over_d_key = piece_key[1:3]
            if d_key in change_keys:
                d_key = change_keys[d_key]
            if over_d_key in change_keys:
                over_d_key = change_keys[over_d_key]
            return 'DOVERD', d_key, over_d_key
        elif is_overd(piece_key) and (piece_key[1] in change_keys):
            return 'DOVERD', change_keys[piece_key[1]]
        elif piece_key in change_keys:
            return change_keys[piece_key]
        else:
            return piece_key
    else:
        return piece_key


def change_var_in_piece_key(piece_key, from_old_vars_to_new_vars___dict):
    piece_key = deepcopy(piece_key)   # just to be careful #
    change_vars = deepcopy(from_old_vars_to_new_vars___dict)   # just to be careful #
    for old_var, new_var in from_old_vars_to_new_vars___dict.items():
        if old_var == new_var:
            del change_vars[old_var]
    if change_vars:
        if is_doverd(piece_key):
            d_key, over_d_key = piece_key[1:3]
            if isinstance(d_key, tuple) and (d_key[0] in change_vars):
                d_key = (change_vars[d_key[0]], d_key[1])
            elif d_key in change_vars:
                d_key = change_vars[d_key]
            if isinstance(over_d_key, tuple) and (over_d_key[0] in change_vars):
                over_d_key = (change_vars[over_d_key[0]], over_d_key[1])
            elif over_d_key in change_vars:
                over_d_key = change_vars[over_d_key]
            return 'DOVERD', d_key, over_d_key
        elif is_overd(piece_key):
            key = piece_key[1]
            if isinstance(key, tuple) and (key[0] in change_vars):
                return 'DOVERD', (change_vars[key[0]], key[1])
            elif key in change_vars:
                return 'DOVERD', change_vars[key]
        elif isinstance(piece_key, tuple) and (piece_key[0] in change_vars):
            return change_vars[piece_key[0]], piece_key[1]
        elif piece_key in change_vars:
            return change_vars[piece_key]
        else:
            return piece_key
    else:
        return piece_key


def change_piece_key_or_var_in_piece_key(piece_key, change_keys={}, change_vars={}):
    piece_key = deepcopy(piece_key)   # just to be careful #
    if change_keys:
        piece_key = change_piece_key(piece_key, change_keys)
    if change_vars:
        piece_key = change_var_in_piece_key(piece_key, change_vars)
    return piece_key


def process_step_with_complete_specifications(step):
    step = deepcopy(step)   # just to be careful #
    if isinstance(step, list):
        if len(step) == 1:
            return step + ['all', None]
        elif len(step) == 2:
            return step + [None]
        else:
            return step
    else:
        return [step, 'all', None]