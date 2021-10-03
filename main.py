import helpers, math, random
from route import Route
from city import City
from trip import Trip

POP_SIZE = 10000
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.5

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
    # import ipdb; ipdb.set_trace()
    trip = Trip(city1, city2, t['cost'], t['time'])
    city1.trips.append(trip)
    city2.trips.append(trip)

def mutate_pop(population: list) -> list:
  amount_to_mutate = math.ceil(len(population) * MUTATION_RATE)
  pop_to_mutate = random.choices(population, k=amount_to_mutate)
  return [i.mutate_individual() for i in pop_to_mutate]

def fitness(route: Route) -> float:
  return route.total_value()

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
  population = select(population + mutated_pop)

  if generation % 100 == 0:
    helpers.print_individual(population[0])
