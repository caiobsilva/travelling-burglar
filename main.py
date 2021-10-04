import helpers, math, random, copy
from route import Route
from city import City
from trip import Trip

POP_SIZE = 100
MAX_GENERATIONS = 50
MUTATION_RATE = 0.5
CROSSOVER_RATE = 0.01

def load_cities(city_dict: list) -> list:
  cities = []
  for c in city_dict:
    cities.append(City(c['city'], c['item'], c['value'], c['weight'], c['time']))
  return cities

def load_trips(cities: list, trip_dict: list) -> None:
  find_city = lambda name: next((c for c in cities if c.name == name), None)
  for t in trip_dict:
    city1 = find_city(t['city1'])
    city2 = find_city(t['city2'])
    trip = Trip(city1, city2, t['cost'], t['time'])
    city1.trips.append(trip)
    city2.trips.append(trip)

def mutate_pop(population: list) -> list:
  amount_to_mutate = math.ceil(len(population) * MUTATION_RATE)
  # pop_to_mutate = random.choices(population, k=amount_to_mutate)
  pop_to_mutate = copy.deepcopy(random.choices(population, k=amount_to_mutate))
  return [i.mutate_individual() for i in pop_to_mutate]

def crossover(population: list) -> list:
  crossed_population = []
  amount_to_cross = math.ceil(len(population) * CROSSOVER_RATE)
  pop_to_cross = random.choices(population, k=amount_to_cross)
  for i in range(len(pop_to_cross)-1):
    for j in range(i+1, len(pop_to_cross)):
      new_route = copy.deepcopy(pop_to_cross[i])
      route2 = pop_to_cross[j]

      cross_index = random.randint(0, len(new_route.route)-1)
      new_route.route[cross_index:-1] = route2.route[cross_index:-1]
      new_route.travel_time[cross_index:-1] = route2.travel_time[cross_index:-1]
      new_route.trip_expenses[cross_index:-1] = route2.trip_expenses[cross_index:-1]
      crossed_population.append(new_route)
      # print([c.name for c in new_route.route])
  return crossed_population

def fitness(route: Route) -> float:
  return route.fitness()
  # return route.total_value()

def select(population: list) -> list:
  new_pop = sorted(population, key=fitness, reverse=True)
  return new_pop[0:POP_SIZE]

city_dict = helpers.load_csv('data/items.csv')
trip_dict = helpers.load_csv('data/cities.csv')

cities = load_cities(city_dict)
load_trips(cities, trip_dict)

generation = 0
population = [Route(cities) for _ in range(0, POP_SIZE)]
while generation < MAX_GENERATIONS:
  generation += 1

  mutated_pop = mutate_pop(population)
  crossover_pop = crossover(population)
  population = select(population + mutated_pop + crossover_pop)

  if generation % 10 == 0:
    # import ipdb; ipdb.set_trace()
    helpers.print_individual(population[0])
    # print([r.valid_route().total_value() for r in mutated_pop])
    # print([r.valid_route().total_value() for r in population])
