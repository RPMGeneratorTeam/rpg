from support import RpgTestCase
from rpg.spec import Spec
from rpg.command import Command


class SpecTest(RpgTestCase):

    def setUp(self):
        self.spec = Spec()

    def test_spec_assignment(self):
        self.maxDiff = None
        self.assertEqual("", self.spec.Name)
        self.assertTrue(isinstance(self.spec["build"], Command))
        self.assertEqual("", str(self.spec["build"]))
        self.spec.build = ["cmake .", "make"]
        self.assertTrue(isinstance(self.spec.build, Command))
        self.spec.install = "make install"
        self.assertTrue(isinstance(self.spec["install"], Command))
        self.spec.check = Command("make test")
        self.assertTrue(isinstance(self.spec.check, Command))

        self.assertTrue(isinstance(self.spec["Requires"], list))
        self.spec.Requires.append("python3")
        self.assertTrue(isinstance(self.spec["Requires"], list))
        self.spec.Requires.append("python3-qt5")
        expected = "%Requires:\tpython3\n" \
            "%Requires:\tpython3-qt5\n" \
            "%build\ncmake .\nmake\n\n" \
            "%install\nmake install\n\n" \
            "%check\nmake test\n\n"
        self.assertEqual(expected, str(self.spec))

    def test_spec_setters_fail(self):
        self.assertRaises(AttributeError, setattr, self.spec, "bla", "a")
        self.assertRaises(TypeError, setattr, self.spec, "Name", 3)
        self.assertRaises(TypeError, setattr, self.spec, "description",
                          Command("c"))
        self.assertRaises(TypeError, setattr, self.spec, "Name", ["a", "b"])
