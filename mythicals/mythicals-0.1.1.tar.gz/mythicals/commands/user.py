import sqlalchemy as sa
import sqlalchemy.orm as saorm

from mythicals import domain, db



def parsers(commands, parents):
    parser = commands.add_parser('user', parents=parents)
    commands = parser.add_subparsers()
    create_parser(commands, parents)
    delete_parser(commands, parents)


# create

def create_parser(commands, parents):
    parser = commands.add_parser('create', parents=parents)
    parser.add_argument('name')
    parser.add_argument('password')
    parser.set_defaults(command=create_command)


def create_command(args):
    name = (
        args.name.decode('utf-8')
        if isinstance(args.name, str)
        else args.name
    )
    try:
        with db.Session.begin_nested():
            company = domain.Company.create(name)
    except sa.exc.IntegrityError as ex:
        if '"ix_companies_name"' not in str(ex):
            raise
        company = domain.Company.query.filter_by(name=name).one()
    password =(
        args.password.decode('utf-8')
        if isinstance(args.password, str)
        else args.password
    )
    if not company.authenticate(password):
        company.add_password(password)
    db.Session.commit()


# delete

def delete_parser(commands, parents):
    parser = commands.add_parser('delete', parents=parents)
    parser.add_argument('name')
    parser.set_defaults(command=delete_command)


def delete_command(args):
    name = (
        args.name.decode('utf-8')
        if isinstance(args.name, str)
        else args.name
    )
    try:
        company = (
            domain.Company.query
            .filter(domain.Company.name == name)
        ).one()
    except saorm.exc.NoResultFound:
        return
    db.Session.delete(company)
    db.Session.commit()
