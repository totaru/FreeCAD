# ***************************************************************************
# *   Copyright (c) 2021 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD

import Fem

from . import manager
from .ccx_cantilever_base_edge import setup_cantilever_base_edge
from .manager import get_meshname
from .manager import init_doc


def get_information():
    return {
        "name": "CCX cantilever seg2 beam elements",
        "meshtype": "edge",
        "meshelement": "Seg2",
        "constraints": ["fixed", "force"],
        "solvers": ["calculix"],
        "material": "solid",
        "equation": "mechanical"
    }


def get_explanation(header=""):
    return header + """

To run the example from Python console use:
from femexamples.ccx_cantilever_ele_seg2 import setup
setup()


See forum topic post (for seg3):
https://forum.freecadweb.org/viewtopic.php?f=18&t=16044

CalculiX cantilever modeled with seg2 beam elements

"""


def setup(doc=None, solvertype="ccxtools"):

    # init FreeCAD document
    if doc is None:
        doc = init_doc()

    # explanation object
    # just keep the following line and change text string in get_explanation method
    manager.add_explanation_obj(doc, get_explanation(manager.get_header(get_information())))

    # setup CalculiX cantilever
    doc = setup_cantilever_base_edge(doc, solvertype)
    femmesh_obj = doc.getObject(get_meshname())

    # load the seg2 mesh
    from .meshes.mesh_canticcx_seg2 import create_nodes, create_elements
    new_fem_mesh = Fem.FemMesh()
    control = create_nodes(new_fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating nodes.\n")
    control = create_elements(new_fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating elements.\n")

    # overwrite mesh with the seg2 mesh
    femmesh_obj.FemMesh = new_fem_mesh

    # set mesh obj parameter
    femmesh_obj.SecondOrderLinear = False
    femmesh_obj.ElementDimension = "1D"
    femmesh_obj.ElementOrder = "1st"
    femmesh_obj.CharacteristicLengthMax = "150.0 mm"
    femmesh_obj.CharacteristicLengthMin = "150.0 mm"

    doc.recompute()
    return doc
