import csv

def load_csv(path: str) -> dict:
  with open(path) as file:
    data = csv.DictReader(file)
    return [row for row in data]

def print_individual(individual: list) -> None:
  print('===== Current best route =====')

  total_value = total_weight = total_time = 0.
  for i, city in enumerate(individual.route):
    total_value += city.item_value
    total_weight += city.item_weight
    total_time += city.time_to_steal
    print('{}. City: {}, item: {}, weight: {}, time: {}, value: {}'.format(
      i+1, city.name, city.item_name, city.item_weight, city.time_to_steal, city.item_value
    ))
  print('\nTotal value: {}\nTotal weight: {}\nTime elapsed: {}\n\n'.format(
    individual.total_value(), individual.total_weight(), individual.total_time()
  ))

def count(x,y):
  a = list(map(lambda a: a.name, x))
  b = list(map(lambda b: b.name, y))
  return len(set(a) & set(b))
