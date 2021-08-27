import math


class StatesData:

    def __init__(self, filename="states.txt"):
        # This will read all of the states and their data form the data file i will add in a minute
        # And make an individual state for each of the points and
        self.fileName = filename
        self.states = []
        self.target_value = 0
        self.build_state_nodes()
        self.state_names = []
        self.build_state_names()
        return

    def build_state_nodes(self):
        # This will read the state data from the state data name provided and
        fill = open(self.fileName, "r")
        self.target_value = int(next(fill).split()[-1])
        for line in fill:
            state_array = []
            for x in line.split(","):
                state_array.append(x)
            if len(state_array) == 4:
                new_state = IndividualState(state_array[0], int(state_array[1]), int(state_array[2]), int(state_array[3]))
                self.states.append(new_state)
        fill.close()
        return

    def build_state_names(self):
        # This will read the names of each state node form the states and return the
        for state in self.states:
            self.state_names.append(state.get_name())

    def get_states(self):
        # This will return the states
        return self.states

    def get_state_names(self):
        return self.state_names

    def get_target_value(self):
        return self.target_value


class IndividualState:

    def __init__(self, name, population, electorate, id):
        # Each state has a name, a population, an electoral point awarded, and a identifying prime
        self.name = name
        self.population = population
        self.electorates = electorate
        self.id = id
        return

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_population(self):
        return self.population

    def get_electorate(self):
        return self.electorates

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ElectorateState:

    def __init__(self, not_visited, id, electorate_total, vote_total, visited=[]):
        if not isinstance(visited, list):
            raise Exception("Must give a list of states as visited")
        if not isinstance(not_visited, list):
            raise Exception("Must give a list as not visited")
        self.visited = visited
        self.not_visited = not_visited
        self.id = id
        self.electorate_total = electorate_total
        self.vote_total = vote_total

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_state(self, state):
        # This returns a new Electoral State that with an updated visited and not visited and 1d list, or false
        # if the state has already been visited.
        if not isinstance(state, IndividualState):
            raise Exception("The State given is not an Individual State")
        if self.visited.__contains__(state):
            return False
        # Then we make a new ElectoralState with an updated visited, id, and so on,
        # updates the visited and not visited for the new state
        not_visited = []
        for i in self.not_visited:
            if i != state:
                not_visited.append(i)
        visited = list(self.visited)
        visited.append(state)
        id = self.id*state.get_id()
        # adds the electorate total
        electorate = self.electorate_total + state.get_electorate()
        # adds the vote total
        population = math.floor(state.population/2) + 1 + self.vote_total
        new_ec_state = ElectorateState(not_visited, id, electorate, population, visited)
        return new_ec_state

    def get_not_visited(self):
        return self.not_visited

    def get_not_visited_arr(self, arr):
        if not self.visited:
            return arr
        not_visited = []
        for item in self.not_visited:
            if not self.visited.__contains__(item):
               not_visited.append(item)
        return not_visited


    def get_electorate_total(self):
        return self.electorate_total

    def get_vote_total(self):
        return self.vote_total

    def get_states(self):
        # This will return a list of names of all the states needed to get the current total of votes.
        str = " "
        for state in self.visited:
            str += " " + state.get_name() + ","
        return str

    def get_total_voter_count(self):
        # This will return a
        sum = 0
        for state in self.visited:
            sum += state.get_population()
        for state in self.not_visited:
            sum += state.get_population()
        return sum

    def get_id(self):
        #returns the id of the node.
        return self.id

    def get_priority(self):
        return self.vote_total/self.electorate_total
