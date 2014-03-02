#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import addProperty


class FindQuotedTest(unittest.TestCase):
    def testHappyPath(self):
        # SETUP SUT
        registeredProperties = {
            "regName": "regValue"
        }
        source = [
            """god likes "dead" men who """,
            """are "dirty".""",
            """Registered name is contained several times but """,
            """it should be irrelevant "regName" "regName".""",
            """Registered value can only appear once:""",
            """so first "regValue" is ignored but second "regValue" isn't."""]

        # EXERCISE
        found = addProperty.findQuoted(source, registeredProperties)

        # VERIFY
        self.assertEqual(
            ["dead", "dirty", "regValue"],
            found)


class RemoveLegalHardcoded(unittest.TestCase):
    def testNonRemovalOfIllegalQuoted(self):
        # SETUP SUT
        allQuoted = ["somethingThatShouldNotBeRemoved"]

        # EXERCISE
        selectedQuoted = addProperty.removeLegalHardcoded(allQuoted, [])

        # VERIFY
        self.assertEqual(allQuoted, selectedQuoted)

    def testNumbersRemoval(self):
        # SETUP SUT
        allQuoted = ["1.0"]

        # EXERCISE
        selectedQuoted = addProperty.removeLegalHardcoded(allQuoted, [])

        # VERIFY
        self.assertEqual(0, len(selectedQuoted))

    def testDateIdRemoval(self):
        # SETUP SUT
        allQuoted = ["2014-02-25_2124"]

        # EXERCISE
        selectedQuoted = addProperty.removeLegalHardcoded(allQuoted, [])

        # VERIFY
        self.assertEqual(0, len(selectedQuoted))


class ParseRegisteredPropertiesTest(unittest.TestCase):
    def testHappyPath(self):
        # SETUP SUT
        lines = [
            """<property name="idType" value="int"/>""",
            """<property name="employeeTableName" value="Employee"/>""",
            """<property name="memberTableName" value="Member"/>""",
            """<property name="companyTableName" value="Company"/>""",
            """<property name="shiftTableName" value="Shift"/>""",
            """<property name="shiftEntryTableName" value="ShiftEntry"/>""",
            """<property name="deliveryTableName" value="Delivery"/>"""
        ]

        # EXERCISE
        registered = addProperty.parseRegisteredProperties(lines)

        # VERIFY
        self.assertEqual(len(lines), len(registered))


class RemoveSingleOccurrences(unittest.TestCase):
    def testRemoval(self):
        # SETUP SUT
        l = ["god", "god", "all", "words", "that", "occur", "once", "should",
             "be", "removed"]

        # EXERCISE
        result = addProperty.removeSingleOccurrences(l)

        # VERIFY
        self.assertEqual(["god"], result)

if __name__ == '__main__':
    unittest.main()
