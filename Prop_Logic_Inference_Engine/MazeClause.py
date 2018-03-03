'''
Nicolas Le Gorrec

MazeClause.py

Specifies a Propositional Logic Clause formatted specifically
for Grid Maze Pathfinding problems. Clauses are a disjunction of
GridPropositions (2-tuples of (symbol, location)) mapped to
their negated status in the sentence.
'''
import unittest

class MazeClause:

    def __init__ (self, props):
        self.props = {}
        self.valid = False

        for prop in props:
            testProp = (prop[0], not prop[1])
            if testProp in props:
                self.valid = True
            else:
                self.props.update({prop})

    def getProp (self, prop):
        if prop in self.props:
            return self.props[prop]
        return None

    def isValid (self):
        return self.valid

    def isEmpty (self):
        return len(self.props) == 0

    def __eq__ (self, other):
        return self.props == other.props and self.valid == other.valid

    def __hash__ (self):
        # Hashes an immutable set of the stored props for ease of
        # lookup in a set
        return hash(frozenset(self.props.items()))

    # Hint: Specify a __str__ method for ease of debugging (this
    # will allow you to "print" a MazeClause directly to inspect
    # its composite literals)
    # def __str__ (self):
    #     return ""

    @staticmethod
    def resolve (c1, c2):
        results = set()

        if c1.__eq__(c2):
            return results

        if c1.isEmpty():
            results.add(c2)
            return results

        if c2.isEmpty():
            results.add(c1)
            return results

        allProps = list(c1.props.items()) + list(c2.props.items())
        count = 0
        for prop in c1.props:
            if prop in c2.props:
                if c1.props[prop] != c2.props[prop]:
                    if count == 1:
                        return results
                    allProps = [item for item in allProps if item[0] != prop]
                    count += 1

        if len(allProps) == 0:
            if len(c1.props) == 1 and len(c2.props) == 1:
                results.add(MazeClause([]))
            return results

        results.add(MazeClause(allProps))

        return results


class MazeClauseTests(unittest.TestCase):
    def test_mazeprops1(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)])
        self.assertTrue(mc.getProp(("X", (1, 1))))
        self.assertTrue(mc.getProp(("X", (2, 1))))
        self.assertFalse(mc.getProp(("Y", (1, 2))))
        self.assertTrue(mc.getProp(("X", (2, 2))) is None)
        self.assertFalse(mc.isEmpty())

    def test_mazeprops2(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (1, 1)), True)])
        self.assertTrue(mc.getProp(("X", (1, 1))))
        self.assertFalse(mc.isEmpty())

    def test_mazeprops3(self):
        mc = MazeClause([(("X", (1, 1)), True), (("Y", (2, 1)), True), (("X", (1, 1)), False)])
        self.assertTrue(mc.isValid())
        self.assertTrue(mc.getProp(("X", (1, 1))) is None)
        self.assertFalse(mc.isEmpty())

    def test_mazeprops4(self):
        mc = MazeClause([])
        self.assertFalse(mc.isValid())
        self.assertTrue(mc.isEmpty())

    def test_mazeprops5(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops6(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([]) in res)

    def test_mazeprops7(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), True)]) in res)

    def test_mazeprops8(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops9(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops10(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True), (("W", (1, 1)), False)]) in res)

if __name__ == "__main__":
    unittest.main()
