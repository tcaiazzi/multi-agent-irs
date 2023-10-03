def doAction(action,spazio,agent_selection):
    # mossa 0
    if action == 0:
        spazio[agent_selection][action]=True
    # mossa 1
    elif action == 1:
        spazio[agent_selection][0]=True
        spazio[agent_selection][action]=True
    # mossa 2
    elif action == 2:
        spazio[agent_selection][0]=True
        spazio[agent_selection][1]=True
        spazio[agent_selection][action]=True
    return spazio

