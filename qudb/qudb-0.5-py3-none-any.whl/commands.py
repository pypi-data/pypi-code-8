import argparse
import datetime


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid date: {0}.'.format(s)
        raise argparse.ArgumentTypeError(msg)


def setup_db_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-D', '--database', default='qu.db',
                        help='SQLite database file path')
    return parser


def setup_qpath_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-Q', '--questions-directory', default='.',
        help='where to look for questions. Question paths stored in the '
                        'database are relative to this path')
    return parser


def setup_question_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('question', help='path to the question file')
    return parser


def setup_term_atype_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-t', '--term', required=True,
        help='academic semester (3 digits)')
    parser.add_argument('-y', '--assessment-type', required=True,
        help='examples: major1, assignment2, quiz3')
    return parser


def setup_add_update_parser():
    # add/update-only options
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-b', '--bonus', action='store_true',
        help='default points for question')
    parser.add_argument('-p', '--points', help='default points for question')
    parser.add_argument('-o', '--order', type=int,
        help='the order of the question in this assessment; defaults to last')
    # student_count
    # avg_score
    # max_score
    # min_score
    parser.add_argument('-d', '--date', type=valid_date,
        help='assessment date; format YYYY-MM-DD')
    return parser


def setup_init_parser(subparsers, parent_parsers):
    init_parser = subparsers.add_parser('init', parents=parent_parsers)


def setup_list_parser(subparsers, parent_parsers):
    list_parser = subparsers.add_parser('list', parents=parent_parsers)
    list_parser.add_argument('what',
        choices=('terms','assessment-types','assessments', 'questions'),
        help='what to list')
    list_parser.add_argument('-t', '--term',
        help='academic semester code, e.g. 142')
    list_parser.add_argument('-y', '--assessment-type',
        help='examples: major1, assignment2, quiz3')
    list_parser.add_argument('-m', '--mcq', action='store_true',
        help='whether to retrieve MCQs or non-MCQs. cannot retrieve both at once')
    # TODO: --question: list relates assessment_questions (question uses)


def setup_add_parser(subparsers, parent_parsers):
    add_parser = subparsers.add_parser('add', parents=parent_parsers)


def setup_update_parser(subparsers, parent_parsers):
    update_parser = subparsers.add_parser('update', parents=parent_parsers)


def setup_remove_parser(subparsers, parent_parsers):
    remove_parser = subparsers.add_parser('remove', parents=parent_parsers,
                                          aliases=['rm'])


def setup_render_parser(subparsers, parent_parsers):
    render_parser = subparsers.add_parser('render', parents=parent_parsers)
    render_parser.add_argument('template',
                               help='path to the jinja2 template file')
    render_parser.add_argument('-O', '--output-directory', default='output',
        help='the directory in which the rendered files will be saved')
    render_parser.add_argument('-C', '--config', help='ini-style configuration '
        'file defining additional template variables. (Use section [default])')
    render_parser.add_argument('-P', '--pdflatex', action='store_true',
        help='process rendered file with pdflatex (4 runs)')


def parse_command(args_str):
    parser = argparse.ArgumentParser(description='Assemble assessments out of existing questions, e.g. exams, quizzes, assignments')
    db_parser = setup_db_parser()
    qpath_parser = setup_qpath_parser()
    term_atype_parser = setup_term_atype_parser()
    add_update_parser = setup_add_update_parser()
    question_parser = setup_question_parser()

    subparsers = parser.add_subparsers(title='subcommands', dest='subcmd')

    setup_init_parser(subparsers, [db_parser])
    setup_list_parser(subparsers, [db_parser, qpath_parser])
    setup_add_parser(subparsers,
        [db_parser, qpath_parser, term_atype_parser, add_update_parser, question_parser])
    setup_update_parser(subparsers,
        [db_parser, qpath_parser, term_atype_parser, add_update_parser, question_parser])
    setup_remove_parser(subparsers, [db_parser, qpath_parser, term_atype_parser])
    # TODO: rename/mv, copy assessment
    setup_render_parser(subparsers, [db_parser, qpath_parser, term_atype_parser])

    args = parser.parse_args(args=args_str)
    if args.subcmd is None:
        parser.print_help()
    return args
