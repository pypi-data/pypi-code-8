__author__ = 'kwang'

from abc import ABCMeta, abstractmethod


class Course:

    def __init__(self, info):
        """

        :param info: course information
        :type info: dict
        :return:
        """
        self.data = info

    def print_course(self):
        """

        :rtype : None
        """
        for key, value in self.data.items():
            print (key, value)

    def get_course_data(self):
        return self.data

    def get_attributes(self):
        return self.data.keys()


class PartnerCourse(Course):
    # class for courses from partners
    # requires the data to follow the format as
    # pid,school,field,source,course_id,title,instructor,desc,timestamp,id

    required_keys = [
        'pid', # page_id - the id of the page where the course info is from
        'school', # school - school shortname as used in edw
        'field', # field - area of study
        'source', # source - URL for the course info
        'course_id', # Course ID - the course identifier within its own school
        'title', # title - course title
        'instructor', # instructor - course instructors
        'desc', # course description
        'timestamp', # date when the course data was acquired
        'id' # a combination of school shortname and course id; concatenated by '-'
    ]

    def __init__(self, info):
        self.data = dict()
        for each in PartnerCourse.required_keys:
            self.data.setdefault(each, info[each])


class CompetitorCourse(Course):
    required_keys = [
        'category',
        'description',
        'enroll',
        'instructor',
        'instructor_desc',
        'price',
        'slug',
        'subtitle',
        'title',
        'provider'
    ]

    def __init__(self, info):
        self.data = dict()
        for each in CompetitorCourse.required_keys:
            self.data.setdefault(each, info[each])

if __name__ == '__main__':
    i = dict(pid=1, school='yale', field='art', source='yale.com', course_id='art-001', title='what is art',
             instructor='tbd', desc='tbd', timestamp='2015-04-22', id='yale-art-001')
    c = PartnerCourse(info=i)
    c.print_course()

    u = dict(category='art', description='a class on photoshop', enroll=1000, instructor='tba', instructor_desc='tbd',
             price=0.0, slug='learn-photoshop', subtitle='learn photoshop', title='photoshop', provider='udemy')

    e = CompetitorCourse(info=u)
    e.print_course()