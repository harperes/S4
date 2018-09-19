import unittest
import S4

class TestSetMethods(unittest.TestCase):

    def setUp(self):
        self.S = S4.Simulation()
        self.S.create_new()

    def test_set_num_g(self):
        self.S.set_num_g(81)
        x = self.S.get_num_g()
        self.assertEqual(x, 81)

    def test_set_lattice_1D(self):
        self.S.set_lattice(0.5)

    def test_set_lattice_2D(self):
        self.S.set_lattice([[0.5, 0], [0, 0.5]])

    def test_create_material(self):
        mat_name = "test_material"
        nk = [1.1, 0.2]
        self.S.add_material(mat_name, nk)
        # need to add a get method here

    def test_set_layer_pattern_polygon(self):
        self.S.set_lattice([[2.0, 0.0], [0.0, 2.0]])
        # create dummy materials
        self.S.add_material("vacuum", [1.0, 0.0])
        mat_name = "test_material"
        nk = [1.1, 0.2]
        self.S.add_material(mat_name, nk)
        self.S.add_layer("polygon", 5.0, "vacuum")
        verts = [[0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]]
        self.S.set_layer_pattern_polygon("polygon", "test_material", [0.0, 0.0], verts, angle=0.0)
