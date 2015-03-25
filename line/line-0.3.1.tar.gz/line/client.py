# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    LineClient for sending and receiving message from LINE server.

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
import re
import requests
import sys

from api import LineAPI
from models import LineGroup, LineContact, LineRoom, LineMessage
from curve.ttypes import TalkException, ToType, OperationType, Provider

reload(sys)
sys.setdefaultencoding("utf-8")

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class LineClient(LineAPI):
    profile  = None
    contacts = []
    rooms    = []
    groups   = []

    def __init__(self, id=None, password=None, authToken=None, is_mac=True, com_name="carpedm20"):
        """Provide a way to communicate with LINE server.

        :param id: `NAVER id` or `LINE email`
        :param password: LINE account password
        :param authToken: LINE session key
        :param is_mac: (optional) os setting
        :param com_name: (optional) name of your system

        >>> client = LineClient("carpedm20", "xxxxxxxxxx")
        Enter PinCode '9779' to your mobile phone in 2 minutes
        >>> client = LineClient("carpedm20@gmail.com", "xxxxxxxxxx")
        Enter PinCode '7390' to your mobile phone in 2 minutes
        """

        if not (authToken or id and password):
            msg = "id and password or authToken is needed"
            self.raise_error(msg)

        if is_mac:
            os_version = "10.9.4-MAVERICKS-x64"
            user_agent = "DESKTOP:MAC:%s(%s)" % (os_version, self.version)
            app = "DESKTOPMAC\t%s\tMAC\t%s" % (self.version, os_version)
        else:
            os_version = "5.1.2600-XP-x64"
            user_agent = "DESKTOP:WIN:%s(%s)" % (os_version, self.version)
            app = "DESKTOPWIN\t%s\tWINDOWS\t%s" % (self.version, os_version)

        if com_name:
            self.com_name = com_name

        self._headers['User-Agent']         = user_agent
        self._headers['X-Line-Application'] = app

        if authToken:
            self.authToken = self._headers['X-Line-Access'] = authToken

            self.tokenLogin()
            #self.ready()
        else:
            if EMAIL_REGEX.match(id):
                self.provider = Provider.LINE # LINE
            else:
                self.provider = Provider.NAVER_KR # NAVER

            self.id = id
            self.password = password
            self.is_mac = is_mac

            self.login()
            self.ready()

        self.revision = self._getLastOpRevision()
        self.getProfile()

        try:
            self.refreshGroups()
        except: pass

        try:
            self.refreshContacts()
        except: pass

        try:
            self.refreshActiveRooms()
        except: pass

    def getProfile(self):
        """Get `profile` of LINE account"""
        if self._check_auth():
            self.profile = LineContact(self, self._getProfile())

            return self.profile

        return None

    def getContactByName(self, name):
        """Get a `contact` by name
        
        :param name: name of a `contact`
        """
        for contact in self.contacts:
            if name == contact.name:
                return contact

        return None

    def getContactById(self, id):
        """Get a `contact` by id
        
        :param id: id of a `contact`
        """
        for contact in self.contacts:
            if contact.id == id:
                return contact
        if self.profile:
            if self.profile.id == id:
                return self.profile

        return None

    def getContactOrRoomOrGroupById(self, id):
        """Get a `contact` or `room` or `group` by its id

        :param id: id of a instance
        """
        return self.getContactById(id)\
                or self.getRoomById(id)\
                or self.getGroupById(id)

    def refreshGroups(self):
        """Refresh groups of LineClient"""
        if self._check_auth():
            self.groups = []

            self.addGroupsWithIds(self._getGroupIdsJoined())
            self.addGroupsWithIds(self._getGroupIdsInvited(), False)

    def addGroupsWithIds(self, group_ids, is_joined=True):
        """Refresh groups of LineClient"""
        if self._check_auth():
            new_groups  = self._getGroups(group_ids)

            for group in new_groups:
                self.groups.append(LineGroup(self, group, is_joined))

            self.groups.sort()

    def refreshContacts(self):
        """Refresh contacts of LineClient """
        if self._check_auth():
            contact_ids = self._getAllContactIds()
            contacts    = self._getContacts(contact_ids)

            self.contacts = []

            for contact in contacts:
                self.contacts.append(LineContact(self, contact))

            self.contacts.sort()

    def findAndAddContactByUserid(self, userid):
        """Find and add a `contact` by userid

        :param userid: user id
        """
        if self._check_auth():
            try:
                contact = self._findAndAddContactsByUserid(userid)
            except TalkException as e:
                self.raise_error(e.reason)

            contact = contact.values()[0]

            for c in self.contacts:
                if c.id == contact.mid:
                    self.raise_error("%s already exists" % contact.displayName)
                    return 

            c = LineContact(self, contact.values()[0])
            self.contacts.append(c)

            self.contacts.sort()
            return c

    def _findAndAddContactByPhone(self, phone):
        """Find and add a `contact` by phone number

        :param phone: phone number (unknown format)
        """
        if self._check_auth():
            try:
                contact = self._findAndAddContactsByPhone(phone)
            except TalkException as e:
                self.raise_error(e.reason)

            contact = contact.values()[0]

            for c in self.contacts:
                if c.id == contact.mid:
                    self.raise_error("%s already exists" % contact.displayName)
                    return 

            c = LineContact(self, contact.values()[0])
            self.contacts.append(c)

            self.contacts.sort()
            return c

    def _findAndAddContactByEmail(self, email):
        """Find and add a `contact` by email

        :param email: email
        """
        if self._check_auth():
            try:
                contact = self._findAndAddContactsByEmail(email)
            except TalkException as e:
                self.raise_error(e.reason)

            contact = contact.values()[0]

            for c in self.contacts:
                if c.id == contact.mid:
                    self.raise_error("%s already exists" % contact.displayName)
                    return 

            c = LineContact(self, contact.values()[0])
            self.contacts.append(c)

            self.contacts.sort()
            return c

    def _findContactByUserid(self, userid):
        """Find a `contact` by userid

        :param userid: user id
        """
        if self._check_auth():
            try:
                contact = self._findContactByUserid(userid)
            except TalkException as e:
                self.raise_error(e.reason)

            return LineContact(self, contact)

    def refreshActiveRooms(self):
        """Refresh active chat rooms"""
        if self._check_auth():
            start = 1
            count = 50

            self.rooms = []

            while True:
                channel = self._getMessageBoxCompactWrapUpList(start, count)

                for box in channel.messageBoxWrapUpList:
                    if box.messageBox.midType == ToType.ROOM:
                        room = LineRoom(self, self._getRoom(box.messageBox.id))
                        self.rooms.append(room)

                if len(channel.messageBoxWrapUpList) == count:
                    start += count
                else:
                    break

    def createGroupWithIds(self, ids=[]):
        """Create a group with contact ids

        :param name: name of group
        :param ids: list of contact ids
        """
        if self._check_auth():
            try:
                group = LineGroup(self, self._createGroup(name, ids))
                self.groups.append(group)

                return group
            except Exception as e:
                self.raise_error(e)

                return None

    def createGroupWithContacts(self, name, contacts=[]):
        """Create a group with contacts
        
        :param name: name of group
        :param contacts: list of contacts
        """
        if self._check_auth():
            try:
                contact_ids = []
                for contact in contacts:
                    contact_ids.append(contact.id)

                group = LineGroup(self, self._createGroup(name, contact_ids))
                self.groups.append(group)

                return group
            except Exception as e:
                self.raise_error(e)

                return None

    def getGroupByName(self, name):
        """Get a group by name
        
        :param name: name of a group
        """
        for group in self.groups:
            if name == group.name:
                return group

        return None

    def getGroupById(self, id):
        """Get a group by id
        
        :param id: id of a group
        """
        for group in self.groups:
            if group.id == id:
                return group

        return None

    def inviteIntoGroup(self, group, contacts=[]):
        """Invite contacts into group
        
        :param group: LineGroup instance
        :param contacts: LineContact instances to invite
        """
        if self._check_auth():
            contact_ids = [contact.id for contact in contacts]
            self._inviteIntoGroup(group.id, contact_ids)

    def acceptGroupInvitation(self, group):
        """Accept a group invitation

        :param group: LineGroup instance
        """
        if self._check_auth():
            try:
                self._acceptGroupInvitation(group.id)
                return True
            except Exception as e:
                self.raise_error(e)
                return False

    def leaveGroup(self, group):
        """Leave a group
        
        :param group: LineGroup instance to leave
        """
        if self._check_auth():
            try:
                self._leaveGroup(group.id)
                self.groups.remove(group)

                return True
            except Exception as e:
                self.raise_error(e)

                return False

    def createRoomWithIds(self, ids=[]):
        """Create a chat room with contact ids"""
        if self._check_auth():
            try:
                room = LineRoom(self, self._createRoom(ids))
                self.rooms.append(room)

                return room
            except Exception as e:
                self.raise_error(e)

                return None

    def createRoomWithContacts(self, contacts=[]):
        """Create a chat room with contacts"""
        if self._check_auth():
            try:
                contact_ids = []
                for contact in contacts:
                    contact_ids.append(contact.id)

                room = LineRoom(self, self._createRoom(contact_ids))
                self.rooms.append(room)

                return room
            except Exception as e:
                self.raise_error(e)

                return None

    def getRoomById(self, id):
        """Get a room by id
        
        :param id: id of a room
        """
        for room in self.rooms:
            if room.id == id:
                return room

        return None

    def inviteIntoRoom(self, room, contacts=[]):
        """Invite contacts into room
        
        :param room: LineRoom instance
        :param contacts: LineContact instances to invite
        """
        if self._check_auth():
            contact_ids = [contact.id for contact in contacts]
            self._inviteIntoRoom(room.id, contact_ids)

    def leaveRoom(self, room):
        """Leave a room
        
        :param room: LineRoom instance to leave
        """
        if self._check_auth():
            try:
                self._leaveRoom(room.id)
                self.rooms.remove(room)

                return True
            except Exception as e:
                self.raise_error(e)

                return False

    def sendMessage(self, message, seq=0):
        """Send a message
        
        :param message: LineMessage instance to send
        """
        if self._check_auth():
            self._sendMessage(message, seq)

    def getMessageBox(self, id):
        """Get MessageBox by id

        :param id: `contact` id or `group` id or `room` id
        """
        if self._check_auth():
            try:
                messageBoxWrapUp = self._getMessageBoxCompactWrapUp(id)

                return messageBoxWrapUp.messageBox
            except:
                return None

    def getRecentMessages(self, messageBox, count):
        """Get recent message from MessageBox

        :param messageBox: MessageBox object
        """
        if self._check_auth():
            id = messageBox.id
            messages = self._getRecentMessages(id, count)
        
            return self.getLineMessageFromMessage(messages)

    def longPoll(self, count=50):
        """Receive a list of operations that have to be processed by original
        Line cleint.

        :param count: number of operations to get from 
        :returns: a generator which returns operations

        >>> for op in client.longPoll():
                sender   = op[0]
                receiver = op[1]
                message  = op[2]
                print "%s->%s : %s" % (sender, receiver, message)
        """
        if self._check_auth():
            """Check is there any operations from LINE server"""
            OT = OperationType

            try:
                operations = self._fetchOperations(self.revision, count)
            except EOFError:
                return
            except TalkException as e:
                if e.code == 9:
                    self.raise_error("user logged in to another machien")
                else:
                    return

            for operation in operations:
                if operation.type == OT.END_OF_OPERATION:
                    pass
                elif operation.type == OT.SEND_MESSAGE:
                    pass
                elif operation.type == OT.RECEIVE_MESSAGE:
                    message    = LineMessage(self, operation.message)

                    raw_sender   = operation.message._from
                    raw_receiver = operation.message.to

                    sender   = self.getContactOrRoomOrGroupById(raw_sender)
                    receiver = self.getContactOrRoomOrGroupById(raw_receiver)

                    # If sender is not found, check member list of group chat sent to
                    if sender is None and type(receiver) is LineGroup:
                        for m in receiver.members:
                            if m.id == raw_sender:
                                sender = m
                                break

                    if sender is None or receiver is None:
                        self.refreshGroups()
                        self.refreshContacts()
                        self.refreshActiveRooms()

                        sender   = self.getContactOrRoomOrGroupById(raw_sender)
                        receiver = self.getContactOrRoomOrGroupById(raw_receiver)

                    if sender is None or receiver is None:
                        contacts = self._getContacts([raw_sender, raw_receiver])
                        if contacts:
                            if len(contacts) == 2:
                                sender = LineContact(self, contacts[0])
                                receiver = LineContact(self, contacts[1])

                    yield (sender, receiver, message)
                else:
                    print "[*] %s" % OT._VALUES_TO_NAMES[operation.type]
                    print operation

                self.revision = max(operation.revision, self.revision)

    def createContactOrRoomOrGroupByMessage(self, message):
        if message.toType == ToType.USER:
            pass
        elif message.toType == ToType.ROOM:
            pass
        elif message.toType == ToType.GROUP:
            pass

    def getLineMessageFromMessage(self, messages=[]):
        """Change Message objects to LineMessage objects

        :param messges: list of Message object
        """
        lineMessages = []

        for message in messages:
            lineMessages.append(LineMessage(self, message))

        return lineMessages

    def _check_auth(self):
        """Check if client is logged in or not"""
        if self.authToken:
            return True
        else:
            msg = "you need to login"
            self.raise_error(msg)

