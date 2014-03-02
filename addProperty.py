#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys


def findQuoted(lines, registeredProperties):
    """ Find quoted strings in lines.

    Ignore all quoted strings that match to keys in registeredProperties.
    Ignore the contained values once but if found in lines more than once
    then the rest of the occurrences are included in the returned list.

    """
    pattern = r"\"([^\"]+)\""
    allQuoted = []
    values = registeredProperties.values()
    for each in lines:
        found = re.findall(pattern, each)
        for eachFound in found:
            if eachFound not in registeredProperties:
                if eachFound in values:
                    values.remove(eachFound)
                else:
                    allQuoted.append(eachFound)
    return allQuoted


def isNumber(s):
    """ Return True when string s contains a valid number. """
    try:
        float(s)
        return True
    except:
        return False


def somePatternMatches(patterns, s):
    """ Return True when any re pattern in patterns matches to s. """
    for each in patterns:
        if re.match(each, s):
            return True
    return False


def removeLegalHardcoded(quotedList, registeredProperties):
    """ Return copy of quotedList without legal hardcoded strings.

    Legal hardcoded value are such that you wouldn't create properties for.
    These include e.g. numbers, "true", and "int".

    """
    illegals = []
    specials = ["UTF-8", "denarced", "true", "false", "int", "BOOLEAN", "id"]
    legalPatterns = [
        r"http.*",
        r"\d{4}-\d{2}-\d{2}_\d{4}",
        r"^\$\{[^}]+}",
        r"char.*",
        r"varchar.*"
    ]
    for each in quotedList:
        if (isNumber(each) or
            somePatternMatches(legalPatterns, each) or
                each in specials or
                each in registeredProperties):
            continue
        illegals.append(each)
    return illegals


def parseRegisteredProperties(lines):
    """ Parse liquibase xml properties from lines (list of xml strings).

    Return dictionary where the keys and values are extracted from xml:
        <property name="dictionaryKey" value="dictionaryValue"/>

    """
    registered = {}
    for each in lines:
        nameResult = re.match(r".* name=\"([^\"]+)\".*", each)
        valueResult = re.match(r".* value=\"([^\"]+)\".*", each)
        if ("<property " in each and
            nameResult and
                valueResult):
            registered[nameResult.group(1)] = valueResult.group(1)
    return registered


def removeSingleOccurrences(quoted):
    """ Return copy of quoted where unique items have been removed. """
    d = {}
    for each in quoted:
        if each not in d:
            d[each] = 0
        d[each] += 1
    multiples = []
    for key, val in d.items():
        if val > 1:
            multiples.append(key)
    return multiples


def deriveDuplicatedStringLiterals(src):
    f = open(src)
    lines = f.readlines()
    registeredProperties = parseRegisteredProperties(lines)
    allQuoted = findQuoted(lines, registeredProperties)
    selectedQuoted = removeLegalHardcoded(allQuoted, registeredProperties)
    return removeSingleOccurrences(selectedQuoted)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Find duplicated string literals in "
               "liquibase xml changelog file.")
        print "Usage: {0} filepath".format(
            sys.argv[0])
    else:
        duplicated = deriveDuplicatedStringLiterals(sys.argv[1])
        for each in duplicated:
            print """<property name="{0}" value="{1}"/>""".format(
                each + "Name", each)
