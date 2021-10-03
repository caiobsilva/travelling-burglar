class City():
  def __init__(self, name, item, value, weight, time_to_steal) -> None:
    self.name = name
    self.item_name = item
    self.item_value = float(value)
    self.item_weight = float(weight)
    self.time_to_steal = float(time_to_steal)
    self.trips = []

  def available_trips(self, skip=[]) -> list:
    '''Returns all available trips from a given city. Can receive a "skip" optional
    list argument, ignoring pruning all trips containing the given cities'''
    return [t for t in self.trips if t.city1 not in skip or t.city2 not in skip]
