"""
BenchExec is a framework for reliable benchmarking.
This file is part of BenchExec.

Copyright (C) 2007-2015  Dirk Beyer
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import benchexec.util as util
import benchexec.tools.template
import benchexec.result as result

class Tool(benchexec.tools.template.BaseTool):
    """
    This class serves as tool adaptor for Ultimate Automizer
    """

    def executable(self):
        return util.find_executable('../UltimateAutomizer/Ultimate.py')

    def environment(self, executable):
        return {"additionalEnv" : {'HOME' :  '.', 'PATH' : ':.'}}

    def program_files(self, executable):
        executableDir = os.path.dirname(executable)
        return [
                executableDir + "/artifacts.xml",
                executableDir + "/AutomizerTermination.xml",
                executableDir + "/Automizer.xml",
                executableDir + "/configuration",
                executableDir + "/features",
                executableDir + "/p2",
                executableDir + "/plugins",
                executableDir + "/svComp-32bit-memsafety-Automizer.epf",
                executableDir + "/svComp-32bit-precise-Automizer.epf",
                executableDir + "/svComp-32bit-simple-Automizer.epf",
                executableDir + "/svComp-64bit-memsafety-Automizer.epf",
                executableDir + "/svComp-64bit-precise-Automizer.epf",
                executableDir + "/svComp-64bit-simple-Automizer.epf",
                executableDir + "/svComp-64bit-termination-Automizer.epf",
                executableDir + "/Ultimate",
                executableDir + "/Ultimate.py",
                executableDir + "/Ultimate.ini",
                executableDir + "/z3",
                executableDir + "/libz3.so"]

    def working_directory(self, executable):
        executableDir = os.path.dirname(executable)
        return executableDir

    def version(self, executable):
        return 'r14553'

    def name(self):
        return 'UltimateAutomizer'


    def cmdline(self, executable, options, sourcefiles, propertyfile, rlimits):
        assert len(sourcefiles) == 1, "only one sourcefile supported"
        sourcefile = sourcefiles[0]
        workingDir = self.working_directory(executable)
        return [
            'python3',
            os.path.relpath(executable, start=workingDir),
            os.path.relpath(propertyfile, start=workingDir),
            os.path.relpath(sourcefile, start=workingDir)] + options


    def determine_result(self, returncode, returnsignal, output, isTimeout):
        for line in output:
            line = line.rstrip()
            status = result.RESULT_UNKNOWN
            if line == 'TRUE':
                status = result.RESULT_TRUE_PROP
            elif line == 'FALSE':
                status = result.RESULT_FALSE_REACH
            elif line == 'FALSE(valid-memtrack)':
                status = result.RESULT_FALSE_MEMTRACK
            elif line == 'FALSE(valid-free)':
                status = result.RESULT_FALSE_FREE
            elif line == 'FALSE(valid-deref)':
                status = result.RESULT_FALSE_DEREF
            elif line == 'UNKNOWN-SYNTAX':
                status = 'ERROR(syntax)'
            elif line == 'UNKNOWN':
                status = result.RESULT_UNKNOWN
            elif isTimeout:
                status = 'TIMEOUT'
            else:
                continue
            return status
        status = 'ERROR'
        return status


    def get_value_from_output(self, output, column):
        # search for the text in output and get its value,
        value = None # default value
        for line in output:
            if line.startswith(column + ':'):
                searchtext = column + ':'
                startPosition = line.find(searchtext) + len(searchtext)
                value = line[startPosition:].strip()
        return value


    """ helper method """
    def allInText(self, words, text):
        """
        This function checks, if all the words appear in the given order in the text.
        """
        index = 0
        for word in words:
            index = text[index:].find(word)
            if index == -1:
                return False
        return True
