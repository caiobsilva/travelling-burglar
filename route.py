from __future__ import annotations
import random

class Route():
  MAX_WEIGHT_AMOUNT = 20.
  MAX_TIME_AMOUT = 72.

  def __init__(self, cities) -> None:
    self.cities = cities
    self.trip_expenses = []
    self.travel_time = []
    self.route = []
    self.generate_individual()

  def mutate_individual(self) -> Route:
    i = random.randint(1, len(self.route)-2)
    previous_city = self.route[i-1]
    possible_trips = previous_city.available_trips(skip=self.route)

    chosen_trip = random.choice(possible_trips)
    self.route[i] = chosen_trip.destination_for(previous_city)
    # self.trip_expenses[i-1] = chosen_trip.value
    # self.travel_time[i-1] = chosen_trip.time

    if not self.is_valid_route():
      # import ipdb; ipdb.set_trace()
      self.route.pop(-2)
      self.trip_expenses.pop(-2)
      self.travel_time.pop(-2)
    return self

  def total_weight(self) -> float:
    return sum([c.item_weight for c in self.route])

  def total_time(self) -> float:
    return sum([c.time_to_steal for c in self.route]) + sum(self.travel_time)

  def total_value(self) -> float:
    return sum([c.item_value for c in self.route]) - sum(self.trip_expenses)

  def is_valid_route(self) -> bool:
    return self.total_time() < self.MAX_TIME_AMOUT and self.total_weight() < self.MAX_WEIGHT_AMOUNT

  def generate_individual(self) -> None:
    '''Populates the route with cities that have trips connecting each other. Cities are
    appended until time and weight constraints are violated. Routes always start and end
    by the city of "Escondidos"'''

    origin_city = self.cities[0] # must start and end at "Escondidos"
    self.route.append(origin_city)

    for _ in self.cities:
      last_city = self.route[-1]
      available_trips = last_city.available_trips(skip=self.route)
      chosen_trip = random.choice(available_trips)

      self.route.append(chosen_trip.destination_for(last_city))
      self.trip_expenses.append(chosen_trip.value)
      self.travel_time.append(chosen_trip.time)
      if not self.is_valid_route():
        self.route.pop()
        self.trip_expenses.pop()
        self.travel_time.pop()
        self.route.append(origin_city)
        break
