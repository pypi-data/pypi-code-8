from unittest.case import TestCase

from trendy.services import ServiceBase, SecurityProfilesService
from mock import MagicMock


class ServicesBaseTestCases(TestCase):
    def setUp(self):
        self.trend = MagicMock()

    def test_all_calls_retrieveAll(self):
        self.trend.testRetrieveAll = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        sut.all()

        self.trend.testRetrieveAll.assert_called_once

    def test_by_id_calls_retrieve(self):
        self.trend.testRetrieve = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        sut.by_id(1)

        self.trend.testRetrieve.assert_called_once_with(1)

    def test_by_ids_calls_retrieve_many_times(self):
        self.trend.testRetrieve = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        result = sut.by_ids([1, 2, 3])

        assert self.trend.testRetrieve.call_count == 3
        self.assertEqual(result, [{}, {}, {}])

    def test_by_name_calls_retrieveByName(self):
        self.trend.testRetrieveByName = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        sut.by_name('name')

        self.trend.testRetrieveByName.assert_called_once_with('name')

    def test_by_names_calls_retrieveByName_many_times(self):
        self.trend.testRetrieveByName = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        sut.by_names(['a', 'b', 'c'])

        assert self.trend.testRetrieveByName.call_count == 3

    def test_update_calls_save(self):
        self.trend.testSave = MagicMock(return_value={})
        sut = ServiceBase(self.trend, 'test')

        sut.update('test')

        self.trend.testSave.assert_called_once_with('test')

    def test_delete_calls_delete_with_id(self):
        self.trend.testDelete = MagicMock(return_value=True)
        sut = ServiceBase(self.trend, 'test')

        sut.delete(1)

        self.trend.testDelete.assert_called_once_with([1])

    def test_delete_calls_delete_with_object(self):
        self.trend.testDelete = MagicMock(return_value=True)
        sut = ServiceBase(self.trend, 'test')
        obj = MagicMock()
        obj.ID = 1

        sut.delete(obj)

        self.trend.testDelete.assert_called_once_with([1])

    def test_default_is_unimplemented(self):
        with self.assertRaises(NotImplementedError):
            sut = ServiceBase(self.trend, 'test')
            sut.default()


class SecurityProfileTestsCases(TestCase):
    def setUp(self):
        self.trend = MagicMock()

    def test_default_has_reasonable_defaults(self):
        sut = SecurityProfilesService(self.trend)
        default = sut.default()

        self.assertEqual(default.description, '')
        self.assertEqual(default.name, '')
        self.assertEqual(default.parentSecurityProfileID, 0)
        self.assertEqual(default.DPIRuleIDs, None)
        self.assertEqual(default.DPIState, "INHERITED")
        self.assertEqual(default.antiMalwareManualID, None)
        self.assertEqual(default.antiMalwareManualInherit, True)
        self.assertEqual(default.antiMalwareRealTimeID, None)
        self.assertEqual(default.antiMalwareRealTimeInherit, True)
        self.assertEqual(default.antiMalwareRealTimeScheduleID, None)
        self.assertEqual(default.antiMalwareScheduledID, None)
        self.assertEqual(default.antiMalwareScheduledInherit, True)
        self.assertEqual(default.antiMalwareState, "INHERITED")
        self.assertEqual(default.applicationTypeIDs, None)
        self.assertEqual(default.firewallRuleIDs, None)
        self.assertEqual(default.firewallState, "INHERITED")
        self.assertEqual(default.integrityRuleIDs, None)
        self.assertEqual(default.integrityState, "INHERITED")
        self.assertEqual(default.logInspectionRuleIDs, None)
        self.assertEqual(default.logInspectionState, "INHERITED")
        self.assertEqual(default.recommendationState, None)
        self.assertEqual(default.scheduleID, None)
        self.assertEqual(default.statefulConfigurationID, None)