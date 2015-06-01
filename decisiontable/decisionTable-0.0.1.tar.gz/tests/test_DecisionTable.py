#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
test_DecisionTable
----------------------------------

Tests for `DecisionTable` module.
"""
import unittest
import decisionTable

class normal(unittest.TestCase):

    def setUp(self):
        self.instance = decisionTable.DecisionTable("""

        packageState     configState     config        action        new_packageState    new_configState

        ================== ============================  ============================ ======================
        None             None            False         install       install             install            
        ok               ok              False         purge         purge               purge

        .                .               True          purge         ok                  purge
        .                .               True          update        ok                  update
        ok               error           False         purge         purge               purge

        .                .               True          update        ok                  update
        .                .               True          install       ok                  install
        .                .               True          purge         ok                  purge
        error            install         False         purge         purge               purge
        .                .               False         install       install             install
        None             error           True          purge         None                purge
        error            purge           False         purge         purge               purge
        ok               None            True          install       ok                  install
        .                .               False         purge         purge               None
        *                *               *             *             ERROR               ERROR
        
            """)

    def test_instance_variable__header(self):
        
        headerList = [
            'packageState',
            'configState',
            'config',
            'action',
            'new_packageState',
            'new_configState'
        ]

        self.assertTrue(self.instance.header)
        self.assertEqual(self.instance.header,headerList)
            
    def test_instance_variable__decisions(self):
        self.assertTrue(self.instance.decisions)
        self.assertEqual(self.instance.decisions,
            [
                ['None', 'None', 'False', 'install', 'install', 'install'],
                ['ok', 'ok', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'ok', 'True', 'purge', 'ok', 'purge'],
                ['ok', 'ok', 'True', 'update', 'ok', 'update'],
                ['ok', 'error', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'error', 'True', 'update', 'ok', 'update'],
                ['ok', 'error', 'True', 'install', 'ok', 'install'],
                ['ok', 'error', 'True', 'purge', 'ok', 'purge'],
                ['error', 'install', 'False', 'purge', 'purge', 'purge'],
                ['error', 'install', 'False', 'install', 'install', 'install'],
                ['None', 'error', 'True', 'purge', 'None', 'purge'],
                ['error', 'purge', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'None', 'True', 'install', 'ok', 'install'],
                ['ok', 'None', 'False', 'purge', 'purge', 'None'],
                ['*', '*', '*', '*', 'ERROR', 'ERROR']
            ]
        )
    
    def test_instance_method__decisionCall(self):
        this = self
        
        def callback(new_packageState,new_configState):
            this.assertEqual(new_packageState,'ok')
            this.assertEqual(new_configState,'purge')
                    
        self.instance.decisionCall(callback,
            ['new_packageState','new_configState'],
            packageState = 'ok',
            configState = 'error',
            config = True,
            action = 'purge'
        )
    
    def test_instance_method__decision(self):
        result = self.instance.decision(
            ['new_packageState','new_configState'],
            packageState = 'error',
            configState = 'install',
            config = 'False',
            action = 'install'
        )
        
        self.assertTrue(result)
        self.assertEqual(result,['install','install'])
    
    def test_instance_method__allDecision(self):
        result = self.instance.allDecisions(
            ['new_packageState','new_configState'],
            packageState = 'error'
        )
        
        self.assertTrue(result)
        self.assertEqual(result,
            [
                ['purge','install','purge','ERROR'],
                ['purge','install','purge','ERROR']
            ]
        )
        
    #Overriden
    
    def tearDown(self):
        pass

class no_decisions(unittest.TestCase):

    def setUp(self):  
        self.instance = decisionTable.DecisionTable(""" packageState     configState     config        action        new_packageState    new_configState """)
     
    def test_instance_variable__header(self):
        
        headerList = [
            'packageState',
            'configState',
            'config',
            'action',
            'new_packageState',
            'new_configState'
        ]

        self.assertTrue(self.instance.header)
        self.assertEqual(self.instance.header,headerList)
            
    def test_instance_variable__decisions(self):
        
        self.assertEqual(self.instance.decisions,[])        
    
    def test_instance_method__decisionCall(self):
        this = self
        
        def callback(new_packageState,new_configState):
            this.assertEqual(new_packageState,None)
            this.assertEqual(new_configState,None)

        self.instance.decisionCall(callback,
            ['new_packageState','new_configState'],
            packageState = 'ok',
            configState = 'error',
            config = True,
            action = 'purge'
        )
    
    def test_instance_method__decision(self):
        
        result = self.instance.decision(
            ['new_packageState','new_configState'],
            packageState = 'ok',
            configState = 'error',
            config = True,
            action = 'purge'
        )
        self.assertTrue(result)
        self.assertEqual(result,[None,None])
    
    def test_instance_method__allDecision(self):
        result = self.instance.allDecisions(
            ['new_packageState','new_configState'],
            packageState = 'error'
        )
        
        self.assertTrue(result)
        self.assertEqual(result, [None,None])
        
    def tearDown(self):
        pass

class catchedErrors(unittest.TestCase):

    def setUp(self):
        self.instance = decisionTable.DecisionTable("test")
    
    def test_instance_variable_wildcardSymbol(self):
        notCatch = False

        try:
            decisionTable.DecisionTable("test",wildcardSymbol='')
            notCatch = True
        except: None

        if notCatch:
            raise ValueError('Not catch error: wildcardSymbol errors')
        
    def test_instance_variable_parentSymbol(self):
        notCatch = False

        try:
            decisionTable.DecisionTable("test",parentSymbol='')
            notCatch = True
        except: None 

        if notCatch:
            raise ValueError('Not catch error: parentSymbol errors')

    def test_instance_method_parseStringData(self):
        notCatch = False
        
        try:
            decisionTable.DecisionTable("")
            notCatch = True
            msg = 'data variable is empty!'
        except: None    
            
        try:
            decisionTable.DecisionTable("test test")
            notCatch = True
            msg = 'is not unique header element!'
        except: None

        try:
            decisionTable.DecisionTable("""
            test test1
            ======
            test 
            test test
            """)
            notCatch = True
            msg = 'missing data in decisions'
        except: None

        try:
            decisionTable.DecisionTable("""
            test test1
            ======
            . test
            test test
            """)
            notCatch = True
            msg = 'missing parent data at first row'
        except: None

        if notCatch:
            raise ValueError('Not catching errors: '+msg)
    
    def test_instance_method_checkDecisionParameters(self):
        notCatch = False
        
        try:
            self.instance.decision([],test = 'None')
            notCatch = True
            msg = 'result should contain one or more string elements'
        except: None

        try:
            self.instance.decision(['test'])
            notCatch = True
            msg = 'values variable should contain one or more elements'
        except: None

        try:
            self.instance.decision(['not_test'],test='None')
            notCatch = True
            msg = 'result is not in header'
        except: None

        try:
            self.instance.decision(['test'],not_test='None')
            notCatch = True
            msg = 'variable name not in header'
        except: None

        try:
            self.instance.decision(['test'],test='')
            notCatch = True
            msg = 'variable in values is empty'
        except: None

        if notCatch:
            raise ValueError('Not catching errors: '+msg)
         
    def tearDown(self):
        pass    
    
if __name__ == '__main__':
    unittest.main()
