from ompl import base as ob
from ompl import geometric as og
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import DisplayTools

def isStateValid(state):
    # Some arbitrary condition on the state (note that thanks to
    # dynamic type checking we can just call getX() and do not need
    # to convert state to an SE2State.)
    return state.getX() < .6

def PlanSE2(display_solution=True):
    # create an SE2 state space
    space = ob.SE2StateSpace()

    # set lower and upper bounds
    bounds = ob.RealVectorBounds(2)
    bounds.setLow(-1)
    bounds.setHigh(1)
    space.setBounds(bounds)

    # construct an instance of space information from this state space
    si = ob.SpaceInformation(space)

    # set state validity checking for this space
    si.setStateValidityChecker(ob.StateValidityCheckerFn(isStateValid))

    # create a random start state
    start = ob.State(space)
    start.random()

    # create a random goal state
    goal = ob.State(space)
    goal.random()

    print(f"start:\n{start.__str__()}\ngoal:\n{goal.__str__()}")

    # create a problem instance
    pdef = ob.ProblemDefinition(si)

    # set the start and goal states
    pdef.setStartAndGoalStates(start, goal)

    # create a planner for the defined space
    # planner = og.RRTConnect(si)
    planner = og.PRM(si)
    planner.setMaxNearestNeighbors(3)

    # set the problem we are trying to solve for the planner
    planner.setProblemDefinition(pdef)

    # perform setup steps for the planner
    planner.setup()

    # print the settings for this space
    print(si.settings())

    # print the problem settings
    print(pdef)

    # attempt to solve the problem within one second of planning time
    time_limit = 10.0
    solved = planner.solve(time_limit)
    if solved:
        # get the goal representation from the problem definition (not the same as the goal state)
        # and inquire about the found path
        path = pdef.getSolutionPath()
        print("Found solution:\n%s" % path)

        if display_solution:
            DisplayTools.display_solution_path_SE2(path)
            planer_data = ob.PlannerData(si)
            planner.getPlannerData(planer_data)
            DisplayTools.display_roadmap_graph(planer_data)
    else:
        print("No solution found")


if __name__ == "__main__":
    PlanSE2()
