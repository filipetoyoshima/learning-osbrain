from osbrain import run_nameserver
from osbrain import run_agent


if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    run_agent('Agent0')
    run_agent('Agent1')
    run_agent('Agent2')

    # Show agents registered in the name server
    for alias in ns.agents():
        print(alias)

    specific_agent = ns.proxy('Agent1')
    specific_agent.log_info('Hey!')

    ns.shutdown()