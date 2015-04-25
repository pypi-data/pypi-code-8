__author__ = 'kwang'

from abc import ABCMeta, abstractmethod
from course import *
from pandas import DataFrame


class Catalog:

    def __init__(self, data=None):
        """

        :param data: catalog data
        :type data: DataFrame
        :return:
        """
        if data is None:
            self.data = DataFrame()
        else:
            self.data = data.drop_duplicates()

    def display(self):
        """
        Print the courses within the current catalog
        :return: None
        """
        if self.get_catalog_length() == 0:
            print 'No courses in catalog'
        else:
            print self.data

    def to_csv(self, filename, sep='\x1A'):
        """
        Output the catalog to a csv/text file. Always uses utf-8 encoding.
        :param filename: name of the output file
        :param sep: delimiter to use in the output file, default to CTRL-Z
        :return: None
        :type filename: String
        :type sep: String
        """

        self.data.to_csv(filename, sep=sep, index=False, encoding='utf-8')

    def add_course(self, course):
        """
        Add course to the current catalog
        :type course: Course
        :return: None
        """
        course_data = DataFrame([course.get_course_data()], columns=course.get_attributes())

        if self.get_catalog_length() == 0:
            self.data = self.data.append(course_data)
        elif course.get_attributes() == self.get_schema():
            self.data = self.data.append(course_data).drop_duplicates()
        else:
            raise Exception('Course attributes does not match catalog schema')

    def get_catalog_length(self):
        """
        :return: current length of the catalog
        :rtype: int
        """
        return len(self.data)

    def append_catalog(self, catalog):
        """

        :param catalog: another catalog
        :type catalog: Catalog
        :return:
        """
        if catalog.get_catalog_length() == 0:
            pass
        elif self.get_catalog_length() == 0:
            self.data = catalog.data
        elif catalog.get_schema() != self.get_schema():
            raise Exception("Courses with different attributes cannot be added to the same catalog")
        else:
            self.data = self.data.append(catalog.data).drop_duplicates()

    def get_schema(self):
        """
        :return: the schema of the catalog
        :rtype: list
        """
        if self.get_catalog_length() == 0:
            return []
        else:
            return list(self.data.columns)

if __name__ == '__main__':
    i = dict(pid=1, school='yale', field='art', source='yale.com', course_id='art-001', title='what is art',
             instructor='tbd', desc='tbd', timestamp='2015-04-22', id='yale-art-001')
    c = PartnerCourse(info=i)

    cat = Catalog()
    print cat.get_schema()
    cat.add_course(course=c)
    print cat.get_schema()

    i = dict(pid=2, school='yale', field='art', source='yale.com', course_id='art-002', title='what is art',
             instructor='tbd', desc='tbd', timestamp='2015-04-22', id='yale-art-002')
    c = PartnerCourse(info=i)
    cat.add_course(course=c)
    cat.display()