import re
import os
import datetime
import numpy as np
from os.path import basename, join, splitext, isfile

from _netcdf import NetCDFFile
from femlib.constants import *
from femlib.data import Step, StepRepository
from femlib.mesh import Mesh
from femlib.numerix import aslist, asarray, asstring

__all__ = ['File']

def cat(*args):
    return ''.join(str(a).strip() for a in args)

def adjstr(string):
    return '{0:32s}'.format(string)[:32]

def stringify(a):
    try:
        return ''.join(a).strip()
    except TypeError:
        return [''.join(row).strip() for row in a]

# --- Global dimensions and variables
dim_len_string = 'len_string'
dim_len_line = 'len_line'
dim_four = 'four'
dim_num_dim = 'num_dim'
dim_num_qa = 'num_qa_rec'
dim_time_step = 'time_step'
dim_max_steps = 'max_steps'
var_time_whole = 'time_whole'
var_qa_records = 'qa_records'
var_coor_names = 'coor_names'
var_coor_name = lambda i: cat('coord', 'xyz'[i])

# --- Element dimensions and variables
dim_num_elem = 'num_elem'
dim_num_elem_var = 'num_elem_var'
dim_num_el_blk = 'num_el_blk'
var_elements = 'elements'
var_name_elem_var = 'name_elem_var'
var_eb_prop1 = 'eb_prop1'
var_eb_status = 'eb_status'
var_eb_names = 'eb_names'
var_elem_map = lambda i: cat('elem_map', i)
dim_num_el_in_blk = lambda i: cat('num_el_in_blk', i)
dim_num_nod_per_el = lambda i: cat('num_nod_per_el', i)
var_connect = lambda i: cat('connect', i)
vals_elem_var = lambda i, j: cat('vals_elem_var', i, 'eb', j)

# --- Node dimensions and variables
dim_num_nodes = 'num_nodes'
dim_num_nod_var = 'num_nod_var'
var_nodes = 'nodes'
var_name_nod_var = 'name_nod_var'
vals_nod_var = lambda i: cat('vals_nod_var', i)

# --- Node set dimensons and variables
dim_num_node_sets = 'num_node_sets'
dim_num_nod_ns = lambda i: cat('num_nod_ns', i)
var_ns_prop1 = 'ns_prop1'
var_ns_names = 'ns_names'
var_node_ns = lambda i: cat('node_ns', i)

# --- Global variable dimensions and variables
dim_num_glo_var = 'num_glo_var'
vals_glo_var = 'vals_glo_var'

# --- Side set dimensions and variables
dim_num_side_sets = 'num_side_sets'
dim_num_side_ss = lambda i: cat('num_side_ss', i)
var_ss_prop1 = 'ss_prop1'
var_ss_names = 'ss_names'
var_side_ss = lambda i: cat('side_ss', i)
var_elem_ss = lambda i: cat('elem_ss', i)

# --- Field variable dimensions and variables (femlib specific)
dim_num_field = 'num_field'
var_step_num = 'step_num'
var_step_names = 'step_names'
var_field_elem_var = 'field_elem_var'
var_field_nod_var = 'field_nod_var'
var_fo_prop1 = 'fo_prop1'
var_fo_names = 'fo_names'
var_fo_types = 'fo_types'
var_fo_valinv = 'fo_valinv'

def File(filename, mode='r'):
    if mode not in 'wr':
        raise ValueError('unknown File mode {0}'.format(mode))
    if mode == 'r':
        return EXOFileReader(filename)
    return EXOFileWriter(filename)

class _EXOFile(object):
    mode = None
    def view(self):
        from matmodlab.viewer import launch_viewer
        launch_viewer([self.filename])

    def close(self):
        self.fh.close()

class EXOFileWriter(_EXOFile):
    mode = 'w'
    def __init__(self, filename):
        '''
        Notes
        -----
        The EXOFile class is an interface to the Exodus II api. Its methods
        are named after the analogous method from the Exodus II C bindings,
        minus the prefix 'ex_'.

        '''
        self.fh = NetCDFFile(filename, mode='w')
        self.jobid = splitext(basename(filename))[0]
        self.filename = filename

        self.initialized = False
        self.viewable = False

    def update(self):
        pass

    def __lshift__(self, u):
        if not self.initialized:
            self.initialize(*u.alpha())
        for step in u.steps.values():
            self.put_step(step)
        self.close()

    def initialize(self, dimension, num_node, nodes, vertices,
                   num_elem, elements, connect, element_blocks, field_outputs,
                   node_sets=None, side_sets=None):
        '''Writes the initialization parameters to the EXODUS II file'''

        # ------------------------------------------------------------------- #
        # -------------------------------- standard ExodusII dimensioning --- #
        # ------------------------------------------------------------------- #
        self.fh.floating_point_word_size = 4
        self.fh.version = 5.0300002
        self.fh.file_size = 1
        self.fh.api_version = 5.0300002
        self.fh.title = 'finite element simulation'

        self.fh.filename = basename(self.filename)
        self.fh.jobid = self.jobid

        self.fh.createDimension(dim_len_string, 33)
        self.fh.createDimension(dim_len_line, 81)
        self.fh.createDimension(dim_four, 4)

        self.fh.createDimension(dim_num_dim, dimension)
        self.fh.createDimension(dim_num_nodes, num_node)
        self.fh.createDimension(dim_num_elem, num_elem)

        # node and element number maps
        self.fh.createVariable(var_nodes, 'i', (dim_num_nodes,))
        self.fh.variables[var_nodes][:] = nodes
        self.fh.createVariable(var_elements, 'i', (dim_num_elem,))
        self.fh.variables[var_elements][:] = elements

        # ------------------------------------------------------------------- #
        # ---------------------------------------------------- QA records --- #
        # ------------------------------------------------------------------- #
        now = datetime.datetime.now()
        day = now.strftime("%m/%d/%y")
        hour = now.strftime("%H:%M:%S")
        self.fh.createDimension(dim_num_qa, 1)
        self.fh.createVariable(var_qa_records, 'c', (dim_num_qa, dim_four,
                                                     dim_len_string))
        self.fh.variables[var_qa_records][0, 0, :] = adjstr('femlib')
        self.fh.variables[var_qa_records][0, 1, :] = adjstr(self.jobid)
        self.fh.variables[var_qa_records][0, 2, :] = adjstr(day)
        self.fh.variables[var_qa_records][0, 3, :] = adjstr(hour)

        # ------------------------------------------------------------------- #
        # ------------------------------------------------- record arrays --- #
        # ------------------------------------------------------------------- #
        self.fh.createDimension(dim_time_step, None)
        self.fh.createVariable(var_time_whole, 'f', (dim_time_step,))
        self.fh.createVariable(var_step_num, 'i', (dim_time_step,))
        self.fh.createDimension(dim_max_steps, 100) # arbitrary number
        self.fh.createVariable(var_step_names, 'c', (dim_max_steps, dim_len_string))

        self.step_count = 0

        # ------------------------------------------------------------------- #
        # ------------------------------------------------- field outputs --- #
        # ------------------------------------------------------------------- #
        fields = field_outputs.values()

        nev = sum([len(fo.keys) for fo in fields if fo.position==ELEMENT])
        self.fh.createDimension(dim_num_elem_var, nev)
        self.fh.createVariable(var_name_elem_var, 'c', (dim_num_elem_var,
                                                        dim_len_string))
        self.fh.createVariable(var_field_elem_var, 'i', (dim_num_elem_var,))

        nnv = sum([len(fo.keys) for fo in fields if fo.position==NODE])
        self.fh.createDimension(dim_num_nod_var, nnv)
        self.fh.createVariable(var_name_nod_var, 'c', (dim_num_nod_var,
                                                       dim_len_string))
        self.fh.createVariable(var_field_nod_var, 'i', (dim_num_nod_var,))

        self.fh.createDimension(dim_num_field, len(fields))
        self.fh.createVariable(var_fo_prop1, 'i', (dim_num_field,))
        self.fh.createVariable(var_fo_names, 'c', (dim_num_field, dim_len_string))
        self.fh.createVariable(var_fo_types, 'i', (dim_num_field,))
        self.fh.createVariable(var_fo_valinv, 'c', (dim_num_field, dim_len_string))
        self.fh.variables[var_fo_prop1][:] = np.arange(len(fields)) + 1

        i = j = 0
        for (n, fo) in enumerate(fields):
            self.fh.variables[var_fo_names][n, :] = adjstr(fo.name)
            self.fh.variables[var_fo_types][n] = fo.type
            string = adjstr(asstring(fo.valid_invariants, 0))
            self.fh.variables[var_fo_valinv][n] = string
            for key in fo.keys:
                key = adjstr(key)
                if fo.position == ELEMENT:
                    self.fh.variables[var_name_elem_var][i, :] = key
                    self.fh.variables[var_field_elem_var][i] = n
                    i += 1
                elif fo.position == NODE:
                    self.fh.variables[var_name_nod_var][j, :] = key
                    self.fh.variables[var_field_nod_var][j] = n
                    j += 1
                else:
                    raise ValueError('unknown field output position')

        # ------------------------------------------------------------------- #
        # -------------------------------------------- node set meta data --- #
        # ------------------------------------------------------------------- #
        nns = 0 if node_sets is None else len(node_sets)
        if nns:
            self.fh.createDimension(dim_num_node_sets, nns)
            # node set IDs - standard map
            prop1 = np.arange(nns, dtype=np.int32) + 1
            self.fh.createVariable(var_ns_prop1, 'i', (dim_num_node_sets,))
            self.fh.variables[var_ns_prop1][:] = prop1
            self.fh.variables[var_ns_prop1].name = 'ID'
            self.fh.createVariable(var_ns_names, 'c', (dim_num_node_sets,
                                                       dim_len_string))
            for (i, ns) in enumerate(node_sets, start=1):
                self.fh.variables[var_ns_names][i-1][:] = adjstr(ns.name)
                self.fh.createDimension(dim_num_nod_ns(i), len(ns.nodes))
                self.fh.createVariable(var_node_ns(i), 'i', (dim_num_nod_ns(i),))
                self.fh.variables[var_node_ns(i)][:] = ns.nodes

        # ------------------------------------------------------------------- #
        # -------------------------------------------- side set meta data --- #
        # ------------------------------------------------------------------- #
        nss = 0 if side_sets is None else len(side_sets)
        if nss:
            self.fh.createDimension(dim_num_side_sets, nss)
            # side set IDs - standard map
            prop1 = np.arange(nss, dtype=np.int32) + 1
            self.fh.createVariable(var_ss_prop1, 'i', (dim_num_side_sets,))
            self.fh.variables[var_ss_prop1][:] = prop1
            self.fh.variables[var_ss_prop1].name = 'ID'
            self.fh.createVariable(var_ss_names, 'c', (dim_num_side_sets,
                                                       dim_len_string))
            for (i, ss) in enumerate(side_sets, start=1):
                self.fh.variables[var_ss_names][i-1][:] = adjstr(ss.name)
                self.fh.createDimension(dim_num_side_ss(i), len(ss.sides))
                self.fh.createVariable(var_side_ss(i), 'i', (dim_num_side_ss(i),))
                self.fh.variables[var_side_ss(i)][:] = ss.sides
                self.fh.createVariable(var_elem_ss(i), 'i', (dim_num_elem_ss(i),))
                self.fh.variables[var_elem_ss(i)][:] = ss.elements

        # ------------------------------------------------------------------- #
        # --------------------------------------- element block meta data --- #
        # ------------------------------------------------------------------- #
        # block IDs - standard map
        num_el_blk = len(element_blocks)
        self.fh.createDimension(dim_num_el_blk, num_el_blk)

        prop1 = np.arange(num_el_blk, dtype=np.int32) + 1
        self.fh.createVariable(var_eb_prop1, 'i', (dim_num_el_blk,))
        self.fh.variables[var_eb_prop1][:] = prop1
        self.fh.variables[var_eb_prop1].name = 'ID'

        self.fh.createVariable(var_eb_status, 'i', (dim_num_el_blk,))
        self.fh.variables[var_eb_status][:] = np.ones(num_el_blk, dtype=int)

        self.fh.createVariable(var_eb_names, 'c', (dim_num_el_blk, dim_len_string))
        for (i, block) in enumerate(element_blocks, start=1):
            self.fh.variables[var_eb_names][i-1][:] = adjstr(block.name)

            # block connect
            ij = [elements.index(e) for e in block.elements]
            block_conn = np.array([[n for n in c if n >= 0] for c in connect[ij]])

            ne, nn = block_conn.shape
            d1, d2 = dim_num_el_in_blk(i), dim_num_nod_per_el(i)
            self.fh.createDimension(d1, ne)
            self.fh.createDimension(d2, nn)

            # element map
            elem_map = var_elem_map(i)
            self.fh.createVariable(elem_map, 'i', (d1,))
            self.fh.variables[elem_map][:] = block.elements

            # set up the element block connectivity
            self.fh.createVariable(var_connect(i), 'i', (d1, d2))
            self.fh.variables[var_connect(i)][:] = block_conn

            # element type
            if dimension == 1:
                elem_type = 'TRUSS'
            elif dimension == 2:
                if nn == 3:
                    elem_type = 'TRI'
                elif nn == 4:
                    elem_type = 'QUAD'
            elif dimension == 3:
                if nn in (4, 6):
                    elem_type = 'TET'
                elif nn in (8, 20):
                    elem_type = 'HEX'

            self.fh.variables[var_connect(i)].elem_type = elem_type

            for j in range(1, nev+1):
                self.fh.createVariable(vals_elem_var(j,i), 'f', (dim_time_step, d1))

        # ------------------------------------------------------------------- #
        # ------------------------------------------------ node meta data --- #
        # ------------------------------------------------------------------- #
        if len(vertices.shape) == 1:
            vertices = np.reshape(vertices, (num_node, dimension))
        self.fh.createVariable(var_coor_names, 'c', (dim_num_dim, dim_len_string))
        for i in range(dimension):
            self.fh.variables[var_coor_names][i][:] = adjstr(var_coor_name(i))
            self.fh.createVariable(var_coor_name(i), 'f', (dim_num_nodes,))
            self.fh.variables[var_coor_name(i)][:] = vertices[:, i]

        for j in range(1, nnv+1):
            self.fh.createVariable(vals_nod_var(j), 'f',
                                   (dim_time_step, dim_num_nodes))

        # ------------------------------------------------------------------- #
        # ------------------------------------ global variables meta data --- #
        # ------------------------------------------------------------------- #
        self.fh.createDimension(dim_num_glo_var, 1)
        self.fh.createVariable(vals_glo_var, 'f', (dim_time_step, ))

        self.initialized = True
        return

    def put_step(self, step):

        assert self.initialized

        self.fh.variables[var_step_names][self.step_count] = adjstr(step.name)

        for frame in step.frames:

            # write time value
            count = len(self.fh.variables[var_time_whole].data)
            self.fh.variables[var_time_whole][count] = frame.value
            self.fh.variables[var_step_num][count] = self.step_count
            self.fh.variables[vals_glo_var][count] = 0.

            # get node and element fields
            fields = frame.field_outputs.values()
            fo_n = [fo for fo in fields if fo.position==NODE]
            fo_e = [fo for fo in fields if fo.position==ELEMENT]

            # write out node fields
            a = stringify(self.fh.variables[var_name_nod_var])
            for fo in fo_n:
                data = fo.get_data()
                if len(data.shape) == 1:
                    data = data.reshape(-1, 1)
                for (k, key) in enumerate(fo.keys):
                    i = a.index(key) + 1
                    self.fh.variables[vals_nod_var(i)][count] = data[:, k]

            # write element data to the appropriate element block
            a = stringify(self.fh.variables[var_name_elem_var])
            ebs = stringify(self.fh.variables[var_eb_names])
            for fo in fo_e:
                for (j, eb) in enumerate(ebs, start=1):
                    bd = fo.get_data(block=eb)
                    if len(bd.shape) == 1:
                        bd = bd.reshape(-1, 1)
                    for (k, key) in enumerate(fo.keys):
                        i = a.index(key) + 1
                        self.fh.variables[vals_elem_var(i,j)][count] = bd[:, k]

        self.step_count += 1
        return

class EXOFileReader(_EXOFile):
    mode = 'r'
    def __init__(self, filename):
        if not isfile(filename):
            raise IOError('no such file: {0}'.format(repr(filename)))
        self.filename = filename
        self.fh = NetCDFFile(filename, mode='r')
        self.read()

    def read(self):

        # --- read in the mesh
        # nodes and vertices
        nodes = self.fh.variables[var_nodes][:].tolist()
        dimension = self.fh.dimensions[dim_num_dim]
        vertices = np.empty((len(nodes), dimension))
        for i in range(self.fh.dimensions[dim_num_dim]):
            vertices[:, i] = self.fh.variables[var_coor_name(i)][:]

        # elements, blocks, connectivity
        blocks = {}
        num_el_blk = self.fh.dimensions[dim_num_el_blk]
        elements = self.fh.variables[var_elements][:].tolist()
        emap = dict([(j, i) for (i, j) in enumerate(elements)])
        j = max(self.fh.dimensions[dim_num_nod_per_el(i+1)]
                for i in range(num_el_blk))
        connect = -np.ones((self.fh.dimensions[dim_num_elem], j))
        for i in range(num_el_blk):
            name = stringify(self.fh.variables[var_eb_names][i])
            els = self.fh.variables[var_elem_map(i+1)][:]
            j = [emap[e] for e in els]
            connect[j] = self.fh.variables[var_connect(i+1)][:]
            blocks[name] = els

        # instantiate the mesh
        self.mesh = Mesh(type='free', nodes=nodes, vertices=vertices,
                         elements=elements, connect=connect)
        for (name, elements) in blocks.items():
            self.mesh.ElementBlock(name, elements=elements)

        self._steps = None

    def get_vertices(self):
        return self.mesh.vertices

    def get_nodes(self):
        return self.mesh.nodes

    @property
    def steps(self):
        if self._steps is None:
            self._steps = self.get_steps()
        return self._steps

    def get_steps(self):
        '''Read the step from the output database.  This is essentially the
        reverse operation of put_step

        '''
        CL = 'component_labels'
        steps = StepRepository()
        times = self.fh.variables[var_time_whole][:]

        # set up step counting
        step_num = self.fh.variables[var_step_num][:].tolist()
        step_names = stringify(self.fh.variables[var_step_names])

        for count in range(times.shape[0]):

            step_name = step_names[step_num[count]]
            if step_name not in steps:
                step = Step(step_name)
                if steps:
                    step.frames.append(steps.values()[-1].frames[-1])
                steps[step.name] = step

            time = 0. if count == 0 else times[count-1]
            increment = times[count] - time
            frame = step.Frame(time, increment)

            # get field data
            fields = {}
            for i in range(self.fh.dimensions[dim_num_field]):
                a = asarray(stringify(self.fh.variables[var_fo_valinv][i]),
                            dtype=int)
                fields[i] = {'name':stringify(self.fh.variables[var_fo_names][i]),
                             'type': self.fh.variables[var_fo_types][i],
                             'valid_invariants': a}

            # element data
            for i in range(self.fh.dimensions[dim_num_el_blk]):
                block = stringify(self.fh.variables[var_eb_names][i])
                labels = self.mesh.blocks[block].elements
                for j in range(self.fh.dimensions[dim_num_elem_var]):
                    name = stringify(self.fh.variables[var_name_elem_var][j])
                    field = self.fh.variables[var_field_elem_var][j]
                    fields[field]['position'] = ELEMENT

                    data = self.fh.variables[vals_elem_var(j+1,i+1)][count, :]
                    if i == 0:
                        fields[field].setdefault('data', []).append(data)
                        fields[field]['labels'] = aslist(labels)
                        if fields[field]['type'] != SCALAR:
                            c = name.rsplit('_', 1)[1]
                            fields[field].setdefault(CL, []).append(c)
                    else:
                        if fields[field]['type'] != SCALAR:
                            c = name.rsplit('_', 1)[1]
                            k = fields[field][CL].index(c)
                        else:
                            k = 0
                        d = fields[field]['data'][k]
                        fields[field]['data'][k] = np.append(d, data)
                        fields[field]['labels'].extend(labels)

            # node data
            for i in range(self.fh.dimensions[dim_num_nod_var]):
                name = stringify(self.fh.variables[var_name_nod_var][i])
                field = self.fh.variables[var_field_nod_var][i]
                fields[field]['position'] = NODE

                if fields[field]['type'] != SCALAR:
                    c = name.rsplit('_', 1)[1]
                    fields[field].setdefault(CL, []).append(c)

                data = self.fh.variables[vals_nod_var(i+1)][count, :]
                fields[field].setdefault('data', []).append(data)
                fields[field]['labels'] = self.mesh.nodes

            for (n, info) in fields.items():
                info['data'] = np.column_stack(info['data'])
                field = frame.FieldOutput(info['name'], info['type'],
                                          info['position'], self.mesh,
                                          valid_invariants=info['valid_invariants'],
                                          component_labels=info.get(CL),
                                          mode='r')
                field.add_data(info['labels'], info['data'])

        return steps

if __name__ == '__main__':
    from femlib.mesh import Mesh
    from femlib.funspace import FunctionSpace, Function
    from femlib.element import Element
    mesh = Mesh(type='uniform', ox=0., lx=1., nx=10)
    mesh.ElementBlock(name='Block-1', elements='all')
    mesh.extend(1., 10, block='Block-2')
    V = FunctionSpace(mesh, {'Block-1': Element(type='link2'),
                             'Block-2': Element(type='link2')})
    u = Function(V)
    u += np.linspace(1., 10., len(u.vector))
    field_outputs = u.steps.values()[0].frames[-1].field_outputs
    f = File('myfile', mode='w')
    f.initialize(mesh.dimension, mesh.num_node, mesh.nodes, mesh.vertices,
                 mesh.num_elem, mesh.elements, mesh.connect, mesh.element_blocks,
                 field_outputs)
    for step in u.steps.values():
        f.put_step(step)

    f.close()

    f = File('myfile', mode='r')
    steps = f.get_steps()
    for step in steps.values():
        for frame in step.frames:
            print step.name, frame.time, frame.increment
