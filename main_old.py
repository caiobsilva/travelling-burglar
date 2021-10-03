import random
import math

import helpers
from city import City

MAX_GENERATIONS = 1000
POP_SIZE = 1000
MUTATION_RATE = 0.5
MAX_WEIGHT_AMOUNT = 20.
MAX_TIME_AMOUT = 72.
ITEMS = helpers.load_csv('data/items.csv')
DESTINATIONS = helpers.load_csv('data/cities.csv')

def load_cities(city_dict: list) -> list:
  cities = []
  for c in city_dict:
    cities.append(City(c['city'], c['item'], c['value'], c['weight'], c['time']))
  return cities

CITIES = load_cities(ITEMS)

def generate_individual() -> list:
  return random.sample(CITIES, 12)

# Returns routes containing the provided city's name. I miss sql
def valid_routes(city: City) -> list:
  valid_destinations = lambda at, to: [c[to] for c in DESTINATIONS if c[at] == city.name]
  routes = valid_destinations('city1', 'city2') + valid_destinations('city2', 'city1')
  return [c for c in CITIES if c.name in routes]

def mutate_pop(population: list) -> list:
  amount_to_mutate = math.ceil(len(population) * MUTATION_RATE)
  pop_to_mutate = random.choices(population, k=amount_to_mutate)
  return [mutate_individual(i) for i in pop_to_mutate]

def mutate_individual(individual: list) -> list:
  i = random.randint(0, len(individual)-1)
  routes = valid_routes(individual[i])
  available_routes = [route for route in routes if route not in individual]
  individual[i] = random.choice(available_routes)
  return individual

def fitness(individual: list) -> float:
  score = total_weight = total_time = 0.
  for gene in individual:
    total_weight += gene.item_weight
    total_time += gene.time_to_steal
    if total_weight > MAX_WEIGHT_AMOUNT or total_time > MAX_TIME_AMOUT:
      break
    score += gene.item_value #/ (gene.time_to_steal + gene.item_weight)
  return score

def select(population: list) -> list:
  new_pop = sorted(population, key=fitness, reverse=True)
  return new_pop[0:POP_SIZE]

def prune_unfitting(individual: list) -> None:
  total_weight = total_time = 0.
  for gene in individual:
    total_weight += gene.item_weight
    total_time += gene.time_to_steal

  if total_weight > MAX_WEIGHT_AMOUNT or total_time > MAX_TIME_AMOUT:
    individual.pop()
    prune_unfitting(individual)


generation = 0
population = [generate_individual() for _ in range(0, POP_SIZE)]
sorted(population, key=fitness, reverse=True)
while generation < MAX_GENERATIONS:
  generation += 1

  mutated_pop = mutate_pop(population.copy())
  population = select(population + mutated_pop)

  if generation % 100 == 0:
    helpers.print_population(population[0])

prune_unfitting(population[0])
helpers.print_population(population[0])
