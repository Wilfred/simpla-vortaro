# -*- coding: utf-8 -*-
"""Splitting a compound word into components is no good if we don't
know which one is right. This is a set of sample words that all have
multiple parses used to ensure we return the correct one(s).

"""

import unittest

from vortaro.morphology import parse_morphology

class WordSegmentationTest(unittest.TestCase):
    """Test a single word with the parser.

    """

    @staticmethod
    def get_parsed_string(compound):
        """Given a string of a compound word, return a list of strings
        of potential parses. find_roots does the main work and we just
        convert the Morpheme objects here.
        
        """
        object_parses = parse_morphology(compound)

        parses = []
        for object_parse in object_parses:
            parse = []
            for component in object_parse:
                if type(component) == str:
                    parse.append(component)
                else:
                    # component is a Morpheme object
                    parse.append(component.morpheme)
            parses.append('-'.join(parse))

        return parses

    def __init__(self, compound, expected_output):
        unittest.TestCase.__init__(self)
        self.compound = compound
        self.expected_output = expected_output

    def runTest(self):
        self.test_compound()

    def test_compound(self):
        """Check that we have the correct parses first when we parse
        this compound.

        """
        actual_output = self.get_parsed_string(self.compound)
        # check the start of actual output is the same as expected
        for i in range(len(expected_output)):
            self.assertEqual(self.expected_output[i], actual_output[i])
        
if __name__ == '__main__':
    # Format: (input, correct_parses_in_priority_order)
    correct_parses = [(u'homarano', [u'hom-ar-an-o', u'homa-ran-o']),
                      (u'hundomalfermilo', [u'hundo-mal-ferm-il-o']),
                      (u'persone', [u'person-e', u'per-son-e']),
                      (u'altabligi', [u'al-tabl-ig-i']),
                      (u'manĝilaro', [u'manĝ-il-ar-o']),
                      (u'renovigi', [u're-nov-ig-i']),
                      (u'ripozejo', [u'ripoz-ej-o']),
                      (u'neniigi', [u'neni-ig-i']),
                      (u'pintigi', [u'pint-ig-i']),
                      (u'senlaborulo', [u'sen-labor-ul-o']),
                      (u'ĉirkaŭrigardi', [u'ĉirkaŭ-rigard-i']),
                      (u'eksilentigi', [u'ek-silent-ig-i']),
                      (u'intermiksiĝi', [u'inter-miks-iĝ-i']),
                      (u'memkompreneble', [u'mem-kompren-ebl-e']),
                      (u'gastigema', [u'gast-ig-em-a']),
                      (u'malrapidigi', [u'mal-rapid-ig-i']),
                      (u'koketulino', [u'koket-ul-in-o']),
                      (u'bovinejeto', [u'bov-in-ej-et-o']),
                      (u'kielvifartulo', [u'kiel-vi-fart-ul-o']),
                      # stupid word but all we have for testing -ant, -int etc
                      (u'serĉantigis', [u'serĉ-ant-ig-is']),
                      (u'lernintulo', [u'lern-int-ul-o']),
                      # gets confused with vi-dal
                      (u'vidalvida', [u'vid-al-vid-a']),
                      (u'ĉifrita', [u'ĉifr-it-a']),
                      (u'ĉifrata', [u'ĉifr-at-a']),
                      (u'ĉifrota', [u'ĉifr-ot-a']),
                      (u'eraremulo', [u'erar-em-ul-o'])]

    suite = unittest.TestSuite()
    for (compound, expected_output) in correct_parses:
        suite.addTest(WordSegmentationTest(compound, expected_output))

    unittest.TextTestRunner(verbosity=2).run(suite)
