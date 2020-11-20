#  Copyright (C) 2018  Equinor ASA, Norway.
#
#  The file 'test_grid_equinor_coarse.py' is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.
import itertools
import math

from ecl.eclfile import EclRestartFile
from ecl.grid import EclGrid
from ecl.util.test import TestAreaContext

from tests import EclTest, equinor_test


@equinor_test()
class GridCoarceTest(EclTest):
    def lgc_grid(self):
        return EclGrid(
            self.createTestPath("Equinor/ECLIPSE/LGCcase/LGC_TESTCASE2.EGRID")
        )

    def lgc_restart(self):
        return EclRestartFile(
            self.createTestPath("Equinor/ECLIPSE/LGCcase/LGC_TESTCASE2.UNRST")
        )

    def test_save_roundtrip(self):
        with TestAreaContext("python/grid-test/testCoarse"):
            g1 = self.lgc_grid()

            g1.save_EGRID("LGC.EGRID")
            g2 = EclGrid("LGC.EGRID")
            self.assertTrue(g1.equal(g2, verbose=True))
            self.assertEqual(g1.coarse_groups(), g2.coarse_groups())

    def test_lgc_number_of_groups(self):
        with TestAreaContext("python/grid-test/testCoarse"):
            g1 = self.lgc_grid()

            self.assertTrue(g1.coarse_groups() == 3384)

    def test_create_3d_agrees_with_get_value_on_coarse_grid(self):
        with TestAreaContext("python/grid-test/testCoarse"):
            grid = self.lgc_grid()
            kw = self.lgc_restart()["SGAS"][0]
            nx = grid.getNX()
            ny = grid.getNY()
            nz = grid.getNZ()
            for k, j, i in itertools.product(range(nz), range(ny), range(nx)):
                kw[i + j * nx + nx * ny * k] = i * j * k
            numpy_3d = grid.create3D(kw)
            for k, j, i in itertools.product(range(nz), range(ny), range(nx)):
                self.assertAlmostEqual(numpy_3d[i, j, k], grid.grid_value(kw, i, j, k))
