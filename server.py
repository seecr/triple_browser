#!/usr/bin/env python
from sys import argv
from os.path import dirname, abspath, join
from urllib import urlencode
from simplejson import loads

from weightless.io import Reactor
from weightless.http import httpget
from weightless.core import be, compose

from meresco.core import Observable
from meresco.components.http import ObservableHttpServer

from seecr.html import DynamicHtml
from meresco.xml import namespaces

mydir = dirname(abspath(__file__))

namespaces = namespaces.copy()

def main(port):
    reactor = Reactor()

    dna = (Observable(),
        (ObservableHttpServer(reactor, int(port)),
            (DynamicHtml(
                [join(mydir, "dynamic")],
                reactor=reactor,
                indexPage="/index",
                additionalGlobals={
                    'httpget': httpget,
                    'urlencode': urlencode,
                    'json_loads': loads,
                    'namespaces': namespaces
                }),
            )
        )
    )

    server = be(dna)
    list(compose(server.once.observer_init()))

    reactor.loop()

if __name__ == '__main__':
    args = argv[1:]
    if len(args) != 1:
        print "Usage: %s <port>" % argv[0]
        exit()
    main(*args)
