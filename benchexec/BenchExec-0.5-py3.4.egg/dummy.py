#!/usr/bin/env python3
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

# prepare for Python 3
from __future__ import absolute_import, division, print_function, unicode_literals

from . import BenchExec, main
from .systeminfo import SystemInfo

class DummyExecutor:
    @staticmethod
    def init(config, benchmark):
        benchmark.executable = "dummy"
        benchmark.tool_version = ''

    @staticmethod
    def get_system_info():
        return SystemInfo()
    
    @staticmethod
    def execute_benchmark(benchmark, output_handler):
        for runSet in benchmark.run_sets:
            if not runSet.should_be_executed():
                output_handler.output_for_skipping_run_set(runSet)
                continue
    
            output_handler.output_before_run_set(runSet)
    
            for run in runSet.runs:
                run.cputime = 1.0
                run.walltime = 1.0
                run.values.update({})
    
                output_handler.output_before_run(run)
                run.after_execution(returnvalue=0)
                output_handler.output_after_run(run)
    
            output_handler.output_after_run_set(runSet)
    
        output_handler.output_after_benchmark(False)

class DummyBenchmark(BenchExec):
    def load_executor(self):
        return DummyExecutor

if __name__ == "__main__":
    main(DummyBenchmark())
