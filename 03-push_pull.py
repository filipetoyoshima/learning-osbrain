import time
from osbrain import run_agent
from osbrain import run_nameserver


def log_message(agent, message):
    agent.log_info('Received: %s' % message)


def log_2nd(agent, message):
    agent.log_info('Yeah, I confirm \"%s\" as a message' % message)


if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    alice = run_agent('Alice')
    bob = run_agent('Bob')

    # System configuration
    addr = alice.bind('PUSH', alias='main')
    """ The first parameter 'PUSH' represents the communication pattern we
    want to use. In this case we are using a simple push-pull (unidirectional)
    pattern to allow Alice to send messages to Bob.
        The second parameter is, once again, an alias. We can use this alias
    to refer to this communication channel in an easier way.
        The binding, as you already guessed, takes place in the remote agent,
    but it actually returns a value, which is the address the agent binded to.
    This address is serialized back to us so we can use it to connect other
    agents to it.
    """

    bob.connect(addr, handler=log_message)
    """ Calling connect() from an agent requires, first, an address. This
    address is, in this case, the one we got after binding Alice. This method
    will automatically select the appropriate communication pattern to connect
    to this pattern ('PULL' in this case).
        Bob will be receiving messages from Alice, so we must set a handler
    function that will be executed when a message from Alice is received. This
    handler will be serialized and stored in the remote agent to be executed
    there when needed.
    """

#   bob.connect(addr, handler=[log_message, log_2nd])
    """ handler parameter can receive a list of handlers
    """

    # Send messages
    for _ in range(3):
        time.sleep(1)
        alice.send('main', 'Hello, Bob!')

    ns.shutdown()