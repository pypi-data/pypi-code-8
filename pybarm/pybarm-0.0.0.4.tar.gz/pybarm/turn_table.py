#!/usr/bin/env python
# encoding: utf-8
"""
turn_table.py


Created by Dan MacLean (TSL) on 2015-04-16.
Copyright (c) 2015 Dan MacLean. All rights reserved.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../motors")
import stepper_motor
import time
class TurnTable:
    
    def __init__(self, sections=6, motor_pins=[17,18,21,22]):
        self.sections = sections
        self.motor = stepper_motor.StepperMotor(motor_pins)
        self.steps_between_sections = self.get_steps_between_sections(sections)
        self.steps_to_sections_from_origin = self.get_steps_to_sections(sections)
        self.current_section = 1
        self.steps_to_sections_from_origin
    
    def get_steps_between_sections(self,sections):
        '''divides the 512 steps into specified sections.
        gives an integer on purpose - we must use an integer value of 
        steps'''
        return 512 / sections
    
    def get_steps_to_sections(self,sections):
        '''gets the number of steps to each section from the origin.
        Since the number of steps to each section might be a decimal,
        the extra steps are saved and shared whole between each section.
        
        EG. 512.0 / 6 = 85.3 
        but as we must work in integers..
        512 / 6 = 85
        85 * 6 = 510
        therefore we have 2 steps left over. 
        Put the first extra step in section 1, move all sections back one, then the second in section 2 etc
        '''
        distances = [(self.steps_between_sections * i) - self.steps_between_sections for i in range(1,sections + 1)]
        
        ## now we need to add in the missing steps if any ( we should always have less remaining than there are sections)
        missing_steps = (512 - ((512/sections) * sections) )
        
        if missing_steps > 0:
            for m in range(1,missing_steps + 1):
                for j in range(m, len(distances)):
                    distances[j] += 1
        #total distance should be 512, is distance to last step + steps between sections
        total_distance = distances[-1] + self.steps_between_sections
        assert total_distance == 512, "distances do not cover 512 steps!"
        
        distance_to_section = {}
        
        for i in range(0, sections):
            distance_to_section[i + 1] = distances[i]
            
        return distance_to_section 
    
    def go_to_section(self,target_section):
        '''sends the motor to a particular section'''
        steps_to_go = TurnTable.get_steps_to(self,target_section)
        
        if steps_to_go < 0:
            self.motor.anticlockwise(abs(steps_to_go))
        else:
            self.motor.clockwise(steps_to_go)
        self.current_section = target_section
    
    def get_steps_to(self,target_section):
        '''gets the number of steps from self.current_section to target section.'''
        return self.steps_to_sections_from_origin[target_section] - self.steps_to_sections_from_origin[self.current_section]
        



#print "running!"
#table = TurnTable(6,[17,18,21,22])
#stops = [6,5,4,3,2,1]
#for s in stops:
#    print "going from:", table.current_section, "to section:", s
#    table.go_to_section(s)
#    time.sleep(1)
