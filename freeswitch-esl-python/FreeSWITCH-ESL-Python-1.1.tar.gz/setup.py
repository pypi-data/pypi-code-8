from distutils.core import setup, Extension

setup (name = 'FreeSWITCH-ESL-Python',
       version = '1.1',
       ext_modules=[Extension('_ESL',sources=['swig/esl_wrap.cpp',
                                              'src/esl.c',
                                              'src/esl_json.c',
                                              'src/esl_event.c',
                                              'src/esl_threadmutex.c',
                                              'src/esl_config.c',
                                              'src/esl_oop.cpp',
                                              'src/esl_buffer.c',
					      'swig/esl_wrap.cpp',
                                              'include/esl.h',
                                              'include/esl_json.h',
                                              'include/esl_event.h',
                                              'include/esl_threadmutex.h',
                                              'include/esl_config.h',
                                              'include/esl_oop.h',
                                              'include/esl_buffer.h'],)],
       packages = ['freeswitchESL'],
       pymodules = ['ESL'],
       description = 'Standalone FreeSWITCH ESL Python module.',)

