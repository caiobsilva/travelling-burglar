from city import City

class Trip():
  def __init__(self, city1: City, city2: City, value: float, time: float) -> None:
    self.city1 = city1
    self.city2 = city2
    self.value = float(value)
    self.time = float(time)

  def destination_for(self, city: City) -> City:
    '''Returns the destination for a given city on a trip'''
    return self.city2 if self.city1 == city else self.city1
