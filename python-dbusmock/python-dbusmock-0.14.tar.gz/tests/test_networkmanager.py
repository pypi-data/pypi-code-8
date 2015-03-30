#!/usr/bin/python3

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.  See http://www.gnu.org/copyleft/lgpl.html for the full text
# of the license.

__author__ = 'Iftikhar Ahmad'
__email__ = 'iftikhar.ahmad@canonical.com'
__copyright__ = '(c) 2012 Canonical Ltd.'
__license__ = 'LGPL 3+'

import unittest
import sys
import subprocess
import dbus
import dbusmock
import os
import re

from dbusmock.templates.networkmanager import DeviceState
from dbusmock.templates.networkmanager import NM80211ApSecurityFlags
from dbusmock.templates.networkmanager import InfrastructureMode
from dbusmock.templates.networkmanager import NMActiveConnectionState
from dbusmock.templates.networkmanager import NMState
from dbusmock.templates.networkmanager import NMConnectivityState


p = subprocess.Popen(['which', 'nmcli'], stdout=subprocess.PIPE)
p.communicate()
have_nmcli = (p.returncode == 0)


@unittest.skipUnless(have_nmcli, 'nmcli not installed')
class TestNetworkManager(dbusmock.DBusTestCase):
    '''Test mocking NetworkManager'''

    @classmethod
    def setUpClass(klass):
        klass.start_system_bus()
        klass.dbus_con = klass.get_dbus(True)

        # prepare environment which avoids translations
        klass.lang_env = os.environ.copy()
        try:
            del klass.lang_env['LANG']
        except KeyError:
            pass
        try:
            del klass.lang_env['LANGUAGE']
        except KeyError:
            pass
        klass.lang_env['LC_MESSAGES'] = 'C'

    def setUp(self):
        (self.p_mock, self.obj_networkmanager) = self.spawn_server_template(
            'networkmanager',
            {'NetworkingEnabled': True, 'WwanEnabled': False},
            stdout=subprocess.PIPE)
        self.dbusmock = dbus.Interface(self.obj_networkmanager,
                                       dbusmock.MOCK_IFACE)

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()

    def read_general(self):
        return subprocess.check_output(['nmcli', '--nocheck', 'general'],
                                       env=self.lang_env,
                                       universal_newlines=True)

    def read_connection(self):
        return subprocess.check_output(['nmcli', '--nocheck', 'connection'],
                                       env=self.lang_env,
                                       universal_newlines=True)

    def read_active_connection(self):
        return subprocess.check_output(['nmcli', '--nocheck', 'connection',
                                        'show', '--active'],
                                       env=self.lang_env,
                                       universal_newlines=True)

    def read_device(self):
        return subprocess.check_output(['nmcli', '--nocheck', 'dev'],
                                       env=self.lang_env,
                                       universal_newlines=True)

    def read_device_wifi(self):
        return subprocess.check_output(['nmcli', '--nocheck', 'dev', 'wifi'],
                                       env=self.lang_env,
                                       universal_newlines=True)

    def test_one_eth_disconnected(self):
        self.dbusmock.AddEthernetDevice('mock_Ethernet1', 'eth0',
                                        DeviceState.DISCONNECTED)
        out = self.read_device()
        self.assertRegex(out, 'eth0.*\sdisconnected')

    def test_one_eth_connected(self):
        self.dbusmock.AddEthernetDevice('mock_Ethernet1', 'eth0',
                                        DeviceState.ACTIVATED)
        out = self.read_device()
        self.assertRegex(out, 'eth0.*\sconnected')

    def test_two_eth(self):
        # test with numeric state value
        self.dbusmock.AddEthernetDevice('mock_Ethernet1', 'eth0', 30)
        self.dbusmock.AddEthernetDevice('mock_Ethernet2', 'eth1',
                                        DeviceState.ACTIVATED)
        out = self.read_device()
        self.assertRegex(out, 'eth0.*\sdisconnected')
        self.assertRegex(out, 'eth1.*\sconnected')

    def test_wifi_without_access_points(self):
        self.dbusmock.AddWiFiDevice('mock_WiFi1', 'wlan0',
                                    DeviceState.ACTIVATED)
        out = self.read_device()
        self.assertRegex(out, 'wlan0.*\sconnected')

    def test_eth_and_wifi(self):
        self.dbusmock.AddEthernetDevice('mock_Ethernet1', 'eth0',
                                        DeviceState.DISCONNECTED)
        self.dbusmock.AddWiFiDevice('mock_WiFi1', 'wlan0',
                                    DeviceState.ACTIVATED)
        out = self.read_device()
        self.assertRegex(out, 'eth0.*\sdisconnected')
        self.assertRegex(out, 'wlan0.*\sconnected')

    def test_one_wifi_with_accesspoints(self):
        wifi = self.dbusmock.AddWiFiDevice('mock_WiFi2', 'wlan0',
                                           DeviceState.ACTIVATED)
        self.dbusmock.AddAccessPoint(wifi, 'Mock_AP1', 'AP_1',
                                     '00:23:F8:7E:12:BB',
                                     InfrastructureMode.NM_802_11_MODE_ADHOC,
                                     2425, 5400, 82,
                                     NM80211ApSecurityFlags.NM_802_11_AP_SEC_KEY_MGMT_PSK)
        self.dbusmock.AddAccessPoint(wifi, 'Mock_AP3', 'AP_3',
                                     '00:23:F8:7E:12:BC',
                                     InfrastructureMode.NM_802_11_MODE_INFRA,
                                     2425, 5400, 82, 0x400)
        out = self.read_device()
        aps = self.read_device_wifi()
        self.assertRegex(out, 'wlan0.*\sconnected')
        self.assertRegex(aps, 'AP_1.*\sAd-Hoc')
        self.assertRegex(aps, 'AP_3.*\sInfra')

    def test_two_wifi_with_accesspoints(self):
        wifi1 = self.dbusmock.AddWiFiDevice('mock_WiFi1', 'wlan0',
                                            DeviceState.ACTIVATED)
        wifi2 = self.dbusmock.AddWiFiDevice('mock_WiFi2', 'wlan1',
                                            DeviceState.UNAVAILABLE)
        self.dbusmock.AddAccessPoint(wifi1, 'Mock_AP0',
                                     'AP_0', '00:23:F8:7E:12:BA',
                                     InfrastructureMode.NM_802_11_MODE_UNKNOWN,
                                     2425, 5400, 82, 0x400)
        self.dbusmock.AddAccessPoint(wifi2, 'Mock_AP1', 'AP_1',
                                     '00:23:F8:7E:12:BB',
                                     InfrastructureMode.NM_802_11_MODE_ADHOC,
                                     2425, 5400, 82,
                                     NM80211ApSecurityFlags.NM_802_11_AP_SEC_KEY_MGMT_PSK)
        self.dbusmock.AddAccessPoint(wifi2, 'Mock_AP3', 'AP_2',
                                     '00:23:F8:7E:12:BC',
                                     InfrastructureMode.NM_802_11_MODE_INFRA,
                                     2425, 5400, 82, 0x400)
        out = self.read_device()
        aps = self.read_device_wifi()
        self.assertRegex(out, 'wlan0.*\sconnected')
        self.assertRegex(out, 'wlan1.*\sunavailable')
        self.assertRegex(aps, 'AP_0.*\s(Unknown|N/A)')
        self.assertRegex(aps, 'AP_1.*\sAd-Hoc')
        self.assertRegex(aps, 'AP_2.*\sInfra')

    def test_wifi_with_connection(self):
        wifi1 = self.dbusmock.AddWiFiDevice('mock_WiFi1', 'wlan0',
                                            DeviceState.ACTIVATED)
        ap1 = self.dbusmock.AddAccessPoint(
            wifi1, 'Mock_AP1', 'The_SSID', '00:23:F8:7E:12:BB',
            InfrastructureMode.NM_802_11_MODE_ADHOC, 2425, 5400, 82,
            NM80211ApSecurityFlags.NM_802_11_AP_SEC_KEY_MGMT_PSK)
        con1 = self.dbusmock.AddWiFiConnection(wifi1, 'Mock_Con1', 'The_SSID',
                                               'wpa-psk')

        self.assertRegex(self.read_connection(), 'The_SSID.*\s802-11-wireless')
        self.assertEqual(ap1, '/org/freedesktop/NetworkManager/AccessPoint/Mock_AP1')
        self.assertEqual(con1, '/org/freedesktop/NetworkManager/Settings/Mock_Con1')

    def test_global_state(self):
        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_CONNECTED_GLOBAL)
        self.assertRegex(self.read_general(), 'connected.*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_CONNECTED_SITE)
        self.assertRegex(self.read_general(), 'connected \(site only\).*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_CONNECTED_LOCAL)
        self.assertRegex(self.read_general(), 'connected \(local only\).*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_CONNECTING)
        self.assertRegex(self.read_general(), 'connecting.*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_DISCONNECTING)
        self.assertRegex(self.read_general(), 'disconnecting.*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_DISCONNECTED)
        self.assertRegex(self.read_general(), 'disconnected.*\sfull')

        self.dbusmock.SetGlobalConnectionState(NMState.NM_STATE_ASLEEP)
        self.assertRegex(self.read_general(), 'asleep.*\sfull')

    def test_connectivity_state(self):
        self.dbusmock.SetConnectivity(NMConnectivityState.NM_CONNECTIVITY_FULL)
        self.assertRegex(self.read_general(), 'connected.*\sfull')

        self.dbusmock.SetConnectivity(NMConnectivityState.NM_CONNECTIVITY_LIMITED)
        self.assertRegex(self.read_general(), 'connected.*\slimited')

        self.dbusmock.SetConnectivity(NMConnectivityState.NM_CONNECTIVITY_PORTAL)
        self.assertRegex(self.read_general(), 'connected.*\sportal')

        self.dbusmock.SetConnectivity(NMConnectivityState.NM_CONNECTIVITY_NONE)
        self.assertRegex(self.read_general(), 'connected.*\snone')

    def test_wifi_with_active_connection(self):
        wifi1 = self.dbusmock.AddWiFiDevice('mock_WiFi1', 'wlan0',
                                            DeviceState.ACTIVATED)
        ap1 = self.dbusmock.AddAccessPoint(
            wifi1, 'Mock_AP1', 'The_SSID', '00:23:F8:7E:12:BB',
            InfrastructureMode.NM_802_11_MODE_INFRA, 2425, 5400, 82,
            NM80211ApSecurityFlags.NM_802_11_AP_SEC_KEY_MGMT_PSK)
        con1 = self.dbusmock.AddWiFiConnection(wifi1, 'Mock_Con1', 'The_SSID', '')
        active_con1 = self.dbusmock.AddActiveConnection(
            [wifi1], con1, ap1, 'Mock_Active1',
            NMActiveConnectionState.NM_ACTIVE_CONNECTION_STATE_ACTIVATED)

        self.assertEqual(ap1, '/org/freedesktop/NetworkManager/AccessPoint/Mock_AP1')
        self.assertEqual(con1, '/org/freedesktop/NetworkManager/Settings/Mock_Con1')
        self.assertEqual(active_con1, '/org/freedesktop/NetworkManager/ActiveConnection/Mock_Active1')

        self.assertRegex(self.read_general(), 'connected.*\sfull')
        self.assertRegex(self.read_connection(), 'The_SSID.*\s802-11-wireless')
        self.assertRegex(self.read_active_connection(), 'The_SSID.*\s802-11-wireless')
        self.assertRegex(self.read_device_wifi(), 'The_SSID')

        self.dbusmock.RemoveActiveConnection(wifi1, active_con1)

        self.assertRegex(self.read_connection(), 'The_SSID.*\s802-11-wireless')
        self.assertFalse(re.compile('The_SSID.*\s802-11-wireless').search(self.read_active_connection()))
        self.assertRegex(self.read_device_wifi(), 'The_SSID')

        self.dbusmock.RemoveWifiConnection(wifi1, con1)

        self.assertFalse(re.compile('The_SSID.*\s802-11-wireless').search(self.read_connection()))
        self.assertRegex(self.read_device_wifi(), 'The_SSID')

        self.dbusmock.RemoveAccessPoint(wifi1, ap1)
        self.assertFalse(re.compile('The_SSID').search(self.read_device_wifi()))


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
