# -*- coding: utf-8 -*-
##############################################################################
# Name: peg_peg.py
# Purpose: PEG parser definition using PEG itself.
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2009 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#
# PEG can be used to describe PEG.
# This example demonstrates building PEG parser using PEG based grammar of PEG
# grammar definition language.
##############################################################################
from arpeggio import *
from arpeggio.export import PMDOTExporter, PTDOTExporter
from arpeggio.peg import ParserPEG

# Semantic actions
from arpeggio.peg import SemGrammar, SemRule, SemOrderedChoice, SemSequence,\
    SemPrefix, SemSufix, SemExpression, SemRegEx, SemStrMatch, SemRuleCrossRef

sem_actions = {
    "peggrammar":         SemGrammar(),
    "rule":            SemRule(),
    "ordered_choice":  SemOrderedChoice(),
    "sequence":        SemSequence(),
    "prefix":          SemPrefix(),
    "sufix":           SemSufix(),
    "expression":      SemExpression(),
    "regex":           SemRegEx(),
    "str_match":       SemStrMatch(),
    "rule_crossref":   SemRuleCrossRef()
}


# PEG defined using PEG itself.
peg_grammar = r"""
 peggrammar <- rule+ EOF;
 rule <- rule_name LEFT_ARROW ordered_choice ';';
 ordered_choice <- sequence (SLASH sequence)*;
 sequence <- prefix+;
 prefix <- (AND/NOT)? sufix;
 sufix <- expression (QUESTION/STAR/PLUS)?;
 expression <- regex / rule_crossref
                / (OPEN ordered_choice CLOSE) / str_match;

 rule_name <- r'[a-zA-Z_]([a-zA-Z_]|[0-9])*';
 rule_crossref <- rule_name;
 regex <- 'r\'' r'(\\\'|[^\'])*' '\'';
 str_match <- r'\'(\\\'|[^\'])*\'|"[^"]*"';
 LEFT_ARROW <- '<-';
 SLASH <- '/';
 AND <- '&';
 NOT <- '!';
 QUESTION <- '?';
 STAR <- '*';
 PLUS <- '+';
 OPEN <- '(';
 CLOSE <- ')';
 DOT <- '.';
 comment <- '//' r'.*\n';
"""

def main(debug=False):

    # ParserPEG will use ParserPython to parse peg_grammar definition and
    # create parser_model for parsing PEG based grammars
    parser = ParserPEG(peg_grammar, 'peggrammar', debug=debug)

    # Now we will use created parser to parse the same peg_grammar used for
    # parser initialization. We can parse peg_grammar because it is specified
    # using PEG itself.
    parser.parse(peg_grammar)

    # ASG should be the same as parser.parser_model because semantic
    # actions will create PEG parser (tree of ParsingExpressions).
    asg = parser.getASG(sem_actions)

    if debug:
        # This graph should be the same as peg_peg_parser_model.dot because
        # they define the same parser.
        PMDOTExporter().exportFile(asg,
                                "peg_peg_asg.dot")

    # If we replace parser_mode with ASG constructed parser it will still
    # parse PEG grammars
    parser.parser_model = asg
    parser.parse(peg_grammar)

if __name__ == '__main__':
    main(debug=True)

