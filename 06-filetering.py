import time
import random
from osbrain import run_agent
from osbrain import run_nameserver


def log_a(agent, message):
    agent.log_info('Log a: %s' % message)


def log_b(agent, message):
    agent.log_info('Log b: %s' % message)


def send_message(agent):
    agent.send('main', 'Apple', topic='a')
    agent.send('main', 'Banana', topic='b')


if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    alice = run_agent('Alice')
    bob = run_agent('Bob')
    eve = run_agent('Eve')
    dave = run_agent('Dave')
    carl = run_agent('Carl')
    fiora = run_agent('Fiora')

    # System configuration
    addr = alice.bind('PUB', alias='main')
    bob.connect(addr, handler={'a': log_a, 'b': log_b})
    eve.connect(addr, handler={'a': log_a})
    dave.connect(addr, handler={'b': log_b})
    """ This will specify a topic
        Agents will only receive messages with topic
    they can handle
    """

    # Send messages
    for _ in range(6):
        time.sleep(1)
        topic = random.choice(['a', 'b'])
        print('I choose ' + topic)
        message = 'Hello, %s!' % topic
        alice.send('main', message, topic=topic)

    print("-------------------------------------")
    print("Example of changing topics to listen:")

    addr = carl.bind('PUB', alias='main')
    carl.each(0.5, send_message)
    fiora.connect(addr, alias='listener', handler={'a': log_a})

    time.sleep(2)

    fiora.unsubscribe('listener', 'a')
    fiora.subscribe('listener', handler={'b': log_b})

    time.sleep(2)

    ns.shutdown()