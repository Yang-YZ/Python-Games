"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
        The total number of cookies produced throughout the entire game (this should be initialized to 0.0).
        The current number of cookies you have (this should be initialized to 0.0).
        The current time (in seconds) of the game (this should be initialized to 0.0).
        The current CPS (this should be initialized to 1.0).
        The history list should be initialized as [(0.0, None, 0.0, 0.0)].
        """
        self._total_cookies = 0.0
        self._avail_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return str(self._total_cookies) + ", " + str(self._avail_cookies) + ", " + str(self._time) + ", " + str(self._cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._avail_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._avail_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._avail_cookies) / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        increase the time, the current number of cookies, 
        and the total number of cookies.
        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time += time
            self._avail_cookies += time * self._cps
            self._total_cookies += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        adjust the current number of cookies, the CPS, 
        and add an entry into the history.
        Should do nothing if you cannot afford the item
        """
        if self._avail_cookies >= cost:
            self._avail_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # make a clone of the build_info object 
    build_info_local = build_info.clone()
    # create a new ClickerState object.
    clicker_state = ClickerState()
    
    # Each iteration of this while loop simulates one bribe
    while clicker_state.get_time() <= duration:
        # Call the strategy function with the appropriate arguments 
        # to determine which item to purchase next. 
        # If the strategy function returns None, 
        # you should break out of the loop, as that means no more items will be purchased.
        item_name = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), clicker_state.get_history(), (duration - clicker_state.get_time()), build_info_local)
        if item_name == None:
            break
        # Determine how much time must elapse until it is possible to purchase the item. 
        # If you would have to wait past the duration of the simulation to purchase the item, 
        # you should end the simulation.
        wait_time = clicker_state.time_until(build_info_local.get_cost(item_name))
        if (clicker_state.get_time() + wait_time) > duration:
            break
        # Wait until that time.
        clicker_state.wait(wait_time)
        # Buy the item.
        clicker_state.buy_item(item_name, build_info_local.get_cost(item_name), build_info_local.get_cps(item_name))
        # Update the build information.
        build_info_local.update_item(item_name)
   
    final_time = duration - clicker_state.get_time()    
    clicker_state.wait(final_time)
    
    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    available_cookies = cookies + cps * time_left
    cheapest_item = None
    cheapest_cost = 0.0    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if available_cookies >= item_cost and (cheapest_item == None or cheapest_cost > item_cost):
            cheapest_item = item
            cheapest_cost = item_cost
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    available_cookies = cookies + cps * time_left
    expensive_item = None
    expensive_cost = 0.0    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if available_cookies >= item_cost and (expensive_item == None or expensive_cost < item_cost):
            expensive_item = item
            expensive_cost = item_cost
    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    available_cookies = cookies + cps * time_left
    best_item = None
    best_cps = 0.0    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        if available_cookies >= item_cost and (best_item == None or best_cps < item_cps/item_cost):
            best_item = item
            best_cps = item_cps/item_cost
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
