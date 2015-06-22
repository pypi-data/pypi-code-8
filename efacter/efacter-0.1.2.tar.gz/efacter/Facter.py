import subprocess, json, sys
from datetime import datetime

class Facter (object):
    def __init__(self, piecesRequested):
        self.piecesRequested = piecesRequested
        self.separator = '.'
        self.facterCommand = ['facter', '--json', '--external-dir', '/etc/facter/facts.d/']

    def __listOfFacts(self):
        facts = []
        for piece in self.piecesRequested:
            fact = piece.split(self.separator)[0]
            if fact not in facts:
                facts.append(fact)
        return facts
    
    def allFacts(self):
        self.facterCommand.extend(self.__listOfFacts())
        p = subprocess.Popen(self.facterCommand, stdout=subprocess.PIPE)
        facterCommandOutput, facterCommandStderr = p.communicate()
        if facterCommandStderr:
            print >> sys.stderr, "[%s] %s" % (str(datetime.now()), facterCommandStderr)
            sys.exit(1)
        try:
            jsonFacts = json.loads(facterCommandOutput)
        except ValueError, e:
            return False
        return jsonFacts

    def pieces(self):
        pieces = {}
        factsRequested = self.allFacts()
        for piece in self.piecesRequested:
            result = factsRequested
            keys = piece.split(self.separator)
            for key in keys:
                try:
                    result = result[key]
                except KeyError:
                    result = ''
                    break
            pieces[piece] = result
        return pieces
