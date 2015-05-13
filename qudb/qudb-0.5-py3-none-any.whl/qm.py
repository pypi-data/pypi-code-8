#! /usr/bin/env python3

import os
import sys
import configparser
import subprocess

import jinja2

from qudb import models
from qudb import commands


class UnreadableFile(Exception):
    pass


def check_readable_file(file, path='.'):
    fullpath = os.path.join(path, file)
    if not (os.path.isfile(fullpath) and os.access(fullpath, os.R_OK)):
        raise UnreadableFile


def preprocess_question(question, path):
    check_readable_file(question, path)
    question = os.path.normpath(question)

    # extract info
    mcq = '{0}mcq{0}'.format(os.sep) in question
    # TODO: chapter
    return mcq


def do_list(session, what, term=None, atype=None, mcq=False):
    # TODO: show more data when possible, e.g. assessment-questions
    if what == 'questions':
        # TODO: filter by chapter
        if term is not None and atype is not None:
            # return AssessmentQuestions
            result = models.AssessmentQuestion.by_assessment(
                session, mcq, term, atype)
        # else: return Questions
        elif term is None and atype is None:
            result = models.Question.all(session, mcq).all()
        elif term is not None:
            result = models.Question.by_term(session, mcq, term).all()
        else:  # atype is not None
            result = models.Question.by_atype(session, mcq, atype).all()
    elif what == 'assessments':
        if term is not None and atype is not None:
            result = models.Assessment.get(session, term, atype)
        elif term is not None:
            result = models.Assessment.by_term(session, term)
        elif atype is not None:
            result = models.Assessment.by_atype(session, atype)
        else:
            result = session.query(models.Assessment).all()
    else:
        table_name = ''.join(w.capitalize()
                             for w in what.rstrip('s').split('-'))
        table = getattr(models, table_name)
        result = session.query(table).all()
    return result


def do_add(session, term, atype, question, questions_directory='.',
           bonus=False, points=None, order=None, date=None):
    mcq = preprocess_question(question, questions_directory)
    models.Assessment.add_question(session, term, atype, question,
                                   mcq, bonus, points, order, date)


def do_update(session, term, atype, question=None, questions_directory='.',
              bonus=False, points=None, order=None, date=None):
    if question is None:
        models.Assessment.update_assessment(session, term, atype,
                                            date)
    else:
        mcq = preprocess_question(question, questions_directory)
        models.Assessment.update_question(session, term, atype,
            question, mcq, bonus, points, order, date)


def do_remove(session, term, atype, question):
    models.Assessment.remove_question(session, term, atype, question)


def parse_config_file(config_file):
    if not config_file:
        return {}
    config = configparser.ConfigParser()
    check_readable_file(config_file)
    config.read(config_file)
    return dict(config['default'])


def _atype_to_title(atype):
    title = atype[:-1].title() + ' ' + atype[-1:]
    if title.startswith('Major'):
        title = 'Major Exam' + title[5:]
    return title


def do_render(session, term, atype, template, solution, questions_directory, out_dir, config):
    a = models.Assessment.get(session, term, atype)

    values = parse_config_file(config)
    values['term'] = term
    values['title'] = _atype_to_title(atype)
    values['solution'] = solution
    values['date'] = a.date.strftime('{%d}{%m}{%Y}')
    values['qs'] = a.aqs
    values['mcqs'] = a.amcqs
    values['questions_relpath'] = os.path.relpath(questions_directory, out_dir)

    loader = jinja2.FileSystemLoader(os.path.dirname(template))
    env = jinja2.Environment(
        block_start_string='<%'   , block_end_string='%>',
        variable_start_string='<<', variable_end_string='>>',
        comment_start_string='<#' , comment_end_string='#>',
        loader=loader)
    template = env.get_template(os.path.basename(template))
    return template.render(values)


def create_db(db='qu.db'):
    return models.init(db)


def connect(db='qu.db'):
    '''connect to an existing db only, unless it's in-memory'''
    if db is not None:  # None creates an in-memory db
        check_readable_file(db)
    return models.init(db)


def pdflatex(filenames, outdir):
    for filename in filenames:
        print('Running pdflatex', filename, end=' ', flush=True)
        for i in range(4):
            subprocess.call(['pdflatex', os.path.basename(filename)],
                            cwd=outdir, stdout=subprocess.DEVNULL)
            print('.', end='', flush=True)
        for ext in ['.aux', '.log', '.out']:
            os.remove(os.path.splitext(filename)[0] + ext)
        print()


def main(cmd_args=None):
    cmd_args = cmd_args or sys.argv[1:]
    args = commands.parse_command(cmd_args)
    if args.subcmd is None:
        return

    if args.subcmd == 'init':
        create_db(args.database)
    else:
        try:
            session = connect(args.database)
        except UnreadableFile:
            print('Error: database file \'{}\' is unreadable.'.format(args.database))
            print('\nYou may want to do one of the following:')
            print(' 1. Use the -D (or --database) option to specify the path of an existing database')
            print('    By default, qm looks for ./qu.db')
            print(' 2. Use the \'init\' command, optionally with the -D option, to create a new database')
            print(' 3. Make sure the database file is readable, e.g. you have sufficient privileges')
            return

    if args.subcmd == 'list':
        try:
            result = do_list(session, args.what, args.term,
                             args.assessment_type, args.mcq)
        except models.AssessmentDoesNotExist:
            print('Error: Assessment does not exist')
        else:
            print('Listing {} ({} found):'.format(
                args.what.replace('-', ' '), len(result)))
            for i in result:
                print('- {}'.format(i))

    elif args.subcmd == 'add':
        try:
            do_add(session, args.term, args.assessment_type, args.question,
                   args.bonus, args.points, args.order, args.date)
        except models.AssessmentQuestionExists:
            print('Error: This question already exists in the specified assessment. '
                  'Cannot add. Try update!')
            print('    >> {}-{}: {}'.format(
                args.term, args.assessment_type, args.question))

    elif args.subcmd == 'update':
        try:
            do_update(session, args.term, args.assessment_type, args.question,
                      args.bonus, args.points, args.order, args.date)
        except models.AssessmentQuestionDoesNotExist:
            print('Error: This question does not exist in the specified assessment. '
                  'Cannot update. Try add!')

    elif args.subcmd == 'render':
        base_filename = os.path.join(args.output_directory,
            '{}-{}'.format(args.term, args.assessment_type))
        filenames = [
            base_filename + '.tex',
            base_filename + '-solution.tex'
        ]
        for filename, solution in zip(filenames, (False, True)):
            try:
                print('Rendering {}..'.format(filename))
                output = do_render(session, args.term,
                    args.assessment_type, args.template, solution=solution,
                    questions_directory=args.questions_directory,
                    out_dir=args.output_directory, config=args.config)
            except UnreadableFile:
                print('Error: Configuration file \'{}\' is unreadable'.format(args.config))
                return
            except models.AssessmentDoesNotExist:
                print('Error: Assessment does not exist')
                return
            except jinja2.exceptions.TemplateNotFound as e:
                print('Error: Template file \'{}\' not found'.format(args.template))
                return
            else:
                os.makedirs(args.output_directory, exist_ok=True)
                with open(filename, 'w') as outfile:
                    outfile.write(output)

        if args.pdflatex:
            pdflatex(filenames, args.output_directory)


if __name__ == '__main__':
    main()
