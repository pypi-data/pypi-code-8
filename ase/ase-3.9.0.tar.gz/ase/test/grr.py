from ase.db import connect
from ase import Atoms
db = connect('test.db')
i = db.write(Atoms(), data={'a': 5})
#db.get_atoms(i, add_additional_information=True)
db.update(i, config_id=i)
db.get_atoms(i, add_additional_information=True)
