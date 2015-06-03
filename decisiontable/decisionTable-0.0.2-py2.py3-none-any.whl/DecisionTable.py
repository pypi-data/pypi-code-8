"""
decisionTable.DecisionTable
---------------------------

Main package class with all the logic.
If main package will need additional code, this class should get
fragmented first!

To use main class:

>>> from decisionTable import DecisionTable
>>> table = DecisionTable(tableString)
"""
from __future__ import absolute_import

from . import view

class DecisionTable(object):
    """

    Attributes:
        tableString (str): Main table representer of headers and decisions.
        wildcardSymbol (str,optional): Is any value on decision table.
        parentSymbol (str,optional): Is parent value (one level up on decision table).
        
    Args:
        header (array of str): header strings from tableString.
        decisions (array of (array of str)): Decisions rows from tableString.
        __wildcardSymbol (str) : Wild card symbol
        __parentSymbol (str) : Parent symbol
    """
    
    def __init__(self,tableString,wildcardSymbol='*',parentSymbol='.'):
        
        self.header = [] 
        self.decisions = []
        self.__wildcardSymbol = None
        self.__parentSymbol = None

        self.__setWildcardSymbol(wildcardSymbol)
        self.__setParentSymbol(parentSymbol)
        
        self.header, self.decisions = self.__tableStringParser(tableString)
        self.decisions = self.__replaceSpecialValues(self.decisions)
    
    def __setWildcardSymbol(self,value):
        """self.__wildcardSymbol variable setter"""
        
        errors = []
        if not value is str and not value.split():
            errors.append('wildcardSymbol_ERROR : Symbol : must be char or string!')
        else:
            self.__wildcardSymbol = value
        
        if errors:
            view.Tli.showErrors('SymbolError', errors)
            
    def __setParentSymbol(self,value):
        """self.__parentSymbol variable setter"""
        
        errors = []
        if not value is str and not value.split():
            errors.append('parentSymbol_ERROR : Symbol : must be char or string!')
        else:
            self.__parentSymbol = value
        
        if errors:
            view.Tli.showErrors('SymbolError', errors)
            
    def __tableStringParser(self,tableString):
        """
        Will parse and check tableString parameter for any invalid strings.
        
        Args:
            tableString (str): Standard table string with header and decisions.
        
        Raises:
            ValueError: tableString is empty.
            ValueError: One of the header element is not unique.
            ValueError: Missing data value.
            ValueError: Missing parent data.

        Returns: 
            Array of header and decisions::
            
                print(return)
                [
                    ['headerVar1', ... ,'headerVarN'],
                    [
                        ['decisionValue1', ... ,'decisionValueN'],
                        [<row2 strings>],
                        ...
                        [<rowN strings>]
                    ]
                ]
        """
        
        error = []
        header = []
        decisions = []

        if tableString.split() == []:
            error.append('Table variable is empty!')
        else:
            tableString = tableString.split('\n')
            newData = []
            for element in tableString:
                if element.strip():
                    newData.append(element)
            
            for element in newData[0].split():
                if not element in header:
                    header.append(element)
                else:
                    error.append('Header element: '+element+' is not unique!')
    
            for i, tableString in enumerate(newData[2:]):
                split = tableString.split()
                if len(split) == len(header):
                    decisions.append(split)
                else:
                    error.append('Row: {}==> missing: {} data'.format(
                        str(i).ljust(4),
                        str(len(header)-len(split)).ljust(2))
                    )
        
        if error:
            view.Tli.showErrors('TableStringError',error)
        else:
            return [header,decisions]
            
    def __replaceSpecialValues(self,decisions):
        """
        Will replace special values in decisions array.
        
        Args:
            decisions (array of array of str): Standard decision array format.

        Raises:
            ValueError: Row element don't have parent value.
            
        Returns: 
            New decision array with updated values.
        """
        error = []
        for row, line in enumerate(decisions):
            if '.' in line:
                for i, element in enumerate(line):
                    if row == 0:
                        error.append("Row: {}colume: {}==> don't have parent value".format(str(row).ljust(4),str(i).ljust(4)))
                    if element==self.__parentSymbol:
                        if decisions[row-1][i] == '.':
                            error.append("Row: {}Colume: {}==> don't have parent value".format(str(row).ljust(4),str(i).ljust(4)))
                        
                        decisions[row][i]=decisions[row-1][i]
        
        if error:
            view.Tli.showErrors('ReplaceSpecialValuesError',error)
        else:
            return decisions

    def __toString(self,values):
        """
        Will replace dict values with string values
        
        Args:
            values (dict): Dictionary of values
        
        Returns:
            Updated values dict
        """
        for key in values:
            if not values[key] is str:
                values[key] = str(values[key])
        return values
    
    def __valueKeyWithHeaderIndex(self,values):
        """
        This is hellper function, so that we can mach decision values with row index
        as represented in header index.
        
        Args:
            values (dict): Normaly this will have dict of header values and values from decision
        
        Return:
            >>> return()
            {
                values[headerName] : int(headerName index in header array),
                ...
            }

        """
        machingIndexes = {}
        for index, name in enumerate(self.header):
            if name in values:
                machingIndexes[values[name]] = index
        return machingIndexes
    
    def __checkDecisionParameters(self,result,**values):
        """
        Checker of decision parameters, it will raise ValueError if finds something wrong.
        
        Args:
            result (array of str): See public decision methods
            **values (array of str): See public decision methods
        
        Raise:
            ValueError: Result array none.
            ValueError: Values dict none.
            ValueError: Not find result key in header.
            ValueError: Result value is empty.
        
        Returns:
            Error array values
            
        """
        error = []
        
        if not result:
            error.append('Function parameter (result array) should contain one or more header string!')
        
        if not values:
            error.append('Function parameter (values variables) should contain one or more variable')
        
        for header in result:
            if not header in self.header:
                error.append('String ('+header+') in result is not in header!')
        
        for header in values:
            if not header in self.header:
                error.append('Variable ('+header+') in values is not in header!')
            elif not values[header].split():
                error.append('Variable ('+header+') in values is empty string')
        
        if error:
            return error
                
    def __getDecision(self,result,multiple=False,**values):
        """
        The main method for decision picking.
        
        Args:
            result (array of str): What values you want to get in return array.
            multiple (bolean, optional): Do you want multiple result if it finds many maching decisions.
            **values (dict): What should finder look for, (headerString : value).
        
        Returns: Maped result values with finded elements in row/row.
        """
        
        values = self.__toString(values)
        __valueKeyWithHeaderIndex = self.__valueKeyWithHeaderIndex(values)
        
        errors = self.__checkDecisionParameters(result,**values)
        if errors:
            view.Tli.showErrors('ParametersError', errors)

        machingData = {}
        for line in self.decisions:

            match = True 

            for valueKey in __valueKeyWithHeaderIndex:
                if line[__valueKeyWithHeaderIndex[valueKey]] != valueKey:
                    if line[__valueKeyWithHeaderIndex[valueKey]] != self.__wildcardSymbol:
                        match = False
                        break
            
            if match:
                if multiple:
                    for header in result:
                        if header not in machingData:
                            machingData[header] = [line[self.header.index(header)]]
                        else:
                            machingData[header].append(line[self.header.index(header)])
                else:
                    for header in result:
                        machingData[header] = line[self.header.index(header)]
                    return machingData
        
        if multiple:
            if machingData:
                return machingData

        #Return none if not found (not string so
        #not found value can be recognized
        return dict((key, None) for key in result)

    def decisionCall(self,callback,result,**values):
        """
        The decision method with callback option. This method will find matching row, construct
        a dictionary and call callback with dictionary.

        Args:
            callback (function): Callback function will be called when decision will be finded.
            result (array of str): Array of header string
            **values (dict): What should finder look for, (headerString : value).

        Example:
            >>> def call(header1,header2):
            >>>     print(header1,header2)
            >>>
            >>> table = DecisionTable('''
            >>>     header1 header2
            >>>     ===============
            >>>     value1 value2
            >>> ''')
            >>>
            >>> header1, header2 = table.decision(
            >>>     call,
            >>>     ['header1','header2'],
            >>>     header1='value1',
            >>>     header2='value2'
            >>> )
            (value1 value2)
        """
        callback(**self.__getDecision(result,**values))
    
    def decision(self,result,**values):
        """
        The decision method with callback option. This method will find matching row, construct
        a dictionary and call callback with dictionary.
                
        Args:
            callback (function): Callback function will be called when decision will be finded.
            result (array of str): Array of header string
            **values (dict): What should finder look for, (headerString : value).
        
        Returns:
            Arrays of finded values strings


        Example:
            >>> table = DecisionTable('''
            >>>     header1 header2
            >>>     ===============
            >>>     value1 value2
            >>> ''')
            >>>
            >>> header1, header2 = table.decision(
            >>>     ['header1','header2'],
            >>>     header1='value1',
            >>>     header2='value2'
            >>> )
            >>> print(header1,header2)
            (value1 value2)

        """
        data = self.__getDecision(result,**values)
        data = [ data[value] for value in result]
        if len(data) == 1:
            return data[0]
        else:
            return data
    
    def allDecisions(self,result,**values):
        """
        Joust like self.decision but for multiple finded values.
        
        Returns:
            Arrays of arrays of finded elements or if finds only one mach, array of strings.

        """
        data = self.__getDecision(result,multiple=True,**values)
        data = [ data[value] for value in result]
        if len(data) == 1:
            return data[0]
        else:
            return data