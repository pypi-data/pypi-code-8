#!/usr/bin/env python2
# -*- coding: latin-1 -*-
"""  This class is responsible for configuring a fortigate appliance.

 It uses the pexpect function to SSH into the appliance and then run the desired confing
 commands. The user of this class is expected to have specific knowledge of this appliance.

  Return codes:
    0 - all commands were executed. There will be an accompanying array of output lines.
    1 - nothing needs to be deleted.
    2 - an error occurred. There will be an accompanying error message."""

__author__ = 'Bruce Potter <bp@us.ibm.com>'
__copyright__ = '2015 IBM'
__license__ = 'EPL-1.0'

import pexpect, re, sys

class ConfigureFortigate:

    def __init__(self, user, pw, ip, verbose=False):
        self.user = user
        self.pw = pw
        self.ip = ip
        self.verbose = verbose

    # ----------------------------------------------------------------------------------------
    # Configure the appliance to deny all inbound and outbound user traffic from
    # the VLAN, but allow SL management and intra-VLAN traffic. Here is what a rule looks
    # like in the show firewall policy results:
    #
    #    edit 1
    #    set srcintf "v1234-inside"
    #    set dstintf "v432-outside"
    #    set srcaddr "all"
    #    set dstaddr "all"
    #    set action accept
    #    set schedule "always"
    #    set service "ANY"
    #    next
    #
    def denyAllUserTraffic(self):
        '''Remove all firewall policy rules that allow user traffic to flow into or out of the appliance.
        SoftLayer management traffic is allowed.'''
        # Get the current firewall policy config so we can parse it
        cmd = ['show firewall policy']
        code, output = self.getCommand(cmd)
        if code !=0: return code, output

        # Loop through each row in the output to find the rule sections that begin with 'edit', and
        # build up a list of rules that need to be deleted.
        entryToDelete = None
        foundInside, foundOutside, foundSL = False, False, False
        deleteCommands = ['config firewall policy']

        # Each row is a string. There is an example of a rule section above.
        # What we are looking for a rules that govern traffic going from either the SL VLAN
        # side of the fortigate or the internet side, to the other side. There is one exception.
        # There is a special policy that allows SL admin traffic, and we have to make sure that
        # we don't remove that rule.
        for row in output:
            if row.startswith('edit') or row.startswith('end'):      # edit x were x is a row number, indicates a new section
                # We have found the beginning of a section, or the end of the configuration. Its time to see
                # if we found a rule section that needs to be deleted. We will delete rule sections that describe
                # traffic flowing in->out or out->in and is NOT SL management traffic.
                if foundInside and foundOutside and not foundSL:
                    deleteCommands.append('delete '+entryToDelete)

                # If we've hit the end of the config, terminate the search for rule sections.
                if row.startswith('end'):
                    continue

                # Since we're starting a new rule section now, remember it's number and reset the
                # search variables.
                entryToDelete = row.split(' ')[1]
                foundInside, foundOutside, foundSL = False, False, False
                continue

            # Processing a row within the rule section. If the rule references the inside or the outside
            # of the Fortigate, remember that we saw this reference. ALso, if the rule references the
            # SL management group, remember that too.
            if 'inside' in row:
                foundInside = True
            if 'outside' in row:
                foundOutside = True
            if 'softlayer-admin' in row:
                foundSL = True

        # If we've accumulated any rules to delete, then delete them now.
        if len(deleteCommands) > 1:
            deleteCommands.append('end')
            return self.putConfigCmds(deleteCommands)

        return 1, ["No zones need to be deleted."]


    # ----------------------------------------------------------------------------------------
    # Drive config commands onto the device.
    #
    def putConfigCmds(self, cmds, remoteCmd='ssh', remoteCmdOpts='', remoteCmdArgs=''):
        '''Run the given cmds on the appliance via ssh. We will go into configure mode and save the changes,
        and just return a string saying it was successful (or the error msg).'''

        # Login to the appliance. child is actually a message if there is an error returned.
        code, child = self.login()

        if code == 0:
            # The prompt will change when we switch into config mode. We are assuming that the first command
            # Enters config mode and the rest do whatever config is needed. We also assume the command sequence
            # is terminated by and 'end' command to save the changes. This function will logout.
            self.prompt = re.compile(r'\S+\s\S+\s\$')           # df15-fcr01-tor01 (policy) $
            lines = []
            for c in cmds:
                child.sendline(c)
                if c == 'end':
                    self.prompt = re.compile(r'\S+\s\$')        # df15-fcr01-tor01 $
                child.expect(self.prompt)
                lines.extend([child.before, child.after])

            # Log out
            child.sendline('exit')

            # At this point, the output is a long string that needs to be massaged into an array of output lines.
            output = self.normalizeOutput(lines)

            return 0,output

        return code,child

    # ----------------------------------------------------------------------------------------
    # Drive commands onto the device for the purpose of finding out what config is there.
    #
    def getCommand(self, cmds, remoteCmd='ssh', remoteCmdOpts='', remoteCmdArgs=''):
        '''Run the given cmds on the appliance via ssh. The commands are assumed to be non-destructive,
        and just return the results of each command concatenated together into an array of strings.'''

        # Login to the appliance. child is actually a message if there is an error returned.
        code, child = self.login()

        if code == 0:
            lines = []
            for c in cmds:
                child.sendline(c)
                child.expect(self.prompt)
                lines.extend([child.before, child.after])

            # Log out
            child.sendline('exit')

            # At this point, the output is in long strings that needs to be massaged into an array of output lines.
            output = self.normalizeOutput(lines)

            return 0,output

        return code,child

    # ----------------------------------------------------------------------------------------
    # Login to the appliance.
    #
    # We will try the login a few times before we give up. Initially the ssh timeout will be
    # 15 seconds and this routine will try 4 times.
    #
    def login(self, remoteCmd='ssh', remoteCmdOpts='', remoteCmdArgs=''):
        '''Login to the appliance, and return a handle to login.'''
        if not self.user or not self.pw:  raise ConfigurationError('Userid and password have not been configured.')

        loginCmd = "/usr/bin/"+remoteCmd+" -o 'ConnectTimeout=15' -o 'StrictHostKeyChecking=no' -o 'UserKnownHostsFile /dev/null' "+remoteCmdOpts+' '+self.user+'@'+self.ip+remoteCmdArgs

        self.prompt = re.compile(r'\S+\s\$')          # df15-fcr01-tor01 $
        try:
            # SSH to the appliance before running any commands.
            loopTry = 1
            loggedIn = False
            while not loggedIn and loopTry < 100:
                child = pexpect.spawn(loginCmd)
                if self.verbose:
                    child.logfile = sys.stdout
                index = child.expect(['assword:', self.prompt, pexpect.TIMEOUT, pexpect.EOF])
                if index == 0:
                    loggedIn = True
                else:
                    print "Login attempt "+str(loopTry)+" failed (pexpect index="+str(index)+")."
                    if index == 2:
                        # this could be invalid ip, or the ssh service is not running
                        print 'pexpect '+remoteCmd+' to '+self.user+'@'+self.ip+' timed out'
                    elif index == 3:
                        print 'pexpect '+remoteCmd+' to '+self.user+'@'+self.ip+' reached EOF prematurely'
                    loopTry += 1

            if index == 2:
                # this could be invalid ip, or the ssh service is not running
                return 2, ['pexpect '+remoteCmd+' to '+self.user+'@'+self.ip+' timed out']
            elif index == 3:
                return 2, ['pexpect '+remoteCmd+' to '+self.user+'@'+self.ip+' reached EOF prematurely']
            elif index == 0:
                # we were prompted for pw
                child.sendline(self.pw)
                index = child.expect([self.prompt, 'ermission denied', pexpect.EOF])
                if index == 1:
                    # pw was wrong
                    return 2, ['pexpect '+remoteCmd+' to '+self.user+'@'+self.ip+' had permission denied']
            return 0,child

        except Exception as e:
            print "exception:"+str(e.args)
            return 2, ["pxepect Exception when ssh'ing to "+self.user+'@'+self.ip+':\n'+str(e)+'\noutput:\n'+'\n']

    # ----------------------------------------------------------------------------------------
    # Normalize the output strings into 1 line per array element.
    #
    def normalizeOutput(self,lines):
        '''Massage getCommand output into a usable array of output lines.'''
        # Make 1 long string
        s = ''.join(l for l in lines if isinstance(l,basestring))

        # Split on new line characters
        o = s.splitlines()

        # For every line, get rid of the empty lines, and strip leading/trailing whitespace from the rest.
        output = []
        for l in o:
            if l != '':
                output.append(l.strip())

        return output


class ConfigurationError(Exception):
    pass

# vim: set ts=4 sw=4 expandtab:
