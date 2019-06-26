from osbrain import run_agent
from osbrain import run_nameserver


def reply(agent, message):
    return str(agent.name) + ' received ' + str(message)


def replyYield(agent, message):
    """ This can be used to send a reply before finish
    stuff inside the handler
    """
    yield str(agent.name) + ' received ' + str(message)
    agent.log_info('Already sent a reply back!')


if __name__ == '__main__':

    ns = run_nameserver()
    alice = run_agent('Alice')
    bob = run_agent('Bob')

#   addr = alice.bind('REP', alias='main', handler=reply)
    addr = alice.bind('REP', alias='main', handler=replyYield)
    bob.connect(addr, alias='main')

    for i in range(10):
        bob.send('main', i)
        reply = bob.recv('main')
        print(reply)

    ns.shutdown()