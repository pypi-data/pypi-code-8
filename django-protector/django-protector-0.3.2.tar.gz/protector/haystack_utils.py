from haystack import indexes
from haystack.query import SearchQuerySet
from protector.helpers import filter_object_list


class ProtectedIndex(indexes.Indexable):
    restriction_id = indexes.IntegerField(
        model_attr='restriction_id', indexed=False, null=True
    )
    restriction_content_type_id = indexes.IntegerField(
        model_attr='restriction_content_type_id', indexed=False, null=True
    )


class RestrictedSearchQuerySet(SearchQuerySet):

    def post_process_results(self, results):
        to_cache = super(RestrictedSearchQuerySet, self).post_process_results(results)
        check_ids = []
        for result in to_cache:
            if result.restriction_id and result.restriction_content_type_id:
                check_ids.append((result.restriction_content_type_id, result.restriction_id))
        result_ids = filter_object_list(check_ids)
        return [
            result for result in to_cache if
            (result.restriction_content_type_id, result.restriction_id) in result_ids
        ]
        
