from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
import os


class AppSession(ApplicationSession):

    def onConnect(self):
        print "Attempting to Join"
        user = os.getenv('ROUTER_AUTH_USER', None)
        if user is not None:
            self.join(self.config.realm, [u"wampcra"], unicode(user))
        else:
            super(AppSession, self).onConnect()

    def onChallenge(self, challenge):
        print "Received Auth Challenge"
        if challenge.method == u"wampcra":
            secret = os.environ['ROUTER_AUTH_SECRET']
            signature = auth.compute_wcs(unicode(secret).encode('utf8'), challenge.extra['challenge'].encode('utf8'))
            return signature.decode('ascii')
        else:
            raise Exception("don't know how to handle authmethod {}".format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        print "Connected to the router"

        def test_method(*args, **kwargs):
            return True

        self.register(test_method, "com.example.test")

        while 1:
            yield sleep(10)

    def onDisconnect(self):
        print "Disconnected from the router"
