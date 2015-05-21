from edc.testing.factory.factories import BaseFactory

starting_seq_num = 0


class BaseUuidModelFactory(BaseFactory):
    ABSTRACT_FACTORY = True

#     @classmethod
#     def _setup_next_sequence(cls):
#         try:
#             return 1 + cls._associated_class._default_manager.count()
#         except IndexError:
#             return 1
#     @classmethod
#     def _setup_next_sequence(cls):
#         starting_seq_num += 1
#         return starting_seq_num
