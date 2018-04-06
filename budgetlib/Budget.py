from abc import ABCMeta, abstractmethod
from json import dumps, dump
from .utils import is_tuple, expected_len

class Budget(object, metaclass=ABCMeta):
  """
    A Budget is a time series with multiple index hierarchies
    [Year][Month][Day][SeqNo]
    Each transaction has a year, month, day, and sequence number
  """

  @abstractmethod
  def __init__(self, *args, **kw):
    pass

  @abstractmethod
  def __getitem__(self, x):
    pass

  @abstractmethod
  def __iter__(self):
    pass

  @abstractmethod
  def __len__(self):
    pass

  @abstractmethod
  def __setitem__(self, key, value):
    pass

  @abstractmethod
  def __repr__(self):
    pass

  @abstractmethod
  def __str__(self):
    pass

  @abstractmethod
  def values(self):
    pass

  @abstractmethod
  def keys(self):
    pass

  @abstractmethod
  def items(self):
    """
    """
    pass

  @abstractmethod
  def write(self, write_path = '.'):
    """
    save the budget to write_path
    """
    pass

class DefaultBudget(Budget):
  """
    DefaultBudget uses dictionaries to implement Budget
      This class is implemented using the datetime module.
      Keys are tuples of (datetime instances, seqno (ints))
  """

  def __init__(self, name, processed_data=dict({})):
    """
    Default Budget is given a name to identify it.
    It contains a dict like object to store datetime - value pairs
    """
    self.__budget = processed_data
    self.name = str(name)

  def __getitem__(self, x):
    return self.__budget[x]

  def __iter__(self):
    return iter(self.__budget)

  def __len__(self):
    return len(self.__budget)

  def __setitem__(self, key, value):

    if is_tuple(key) and is_tuple(value) and\
       expected_len(key, 2) and expected_len(value, 3):

      self.__budget[key] = value

    else:
      err = "[Bad key value pair]\n\tkey: {}\n\tvalue: {}".format(str(key), str(value))
      raise ValueError(err)

  def __repr__(self):
    return self.name

  def __str__(self):
    """
    return as json
    [
      {
        "key": [ {"date": date, "seqno": seqno} ],
        "values": [ { "description": ..., "change": ..., "total": ... } ],
      }
    ]
    """
    data = [ dict( {'key': [ x[0], x[1] ],\
                    'values': [ dict( { 'description': y[0], 'change': y[1] , 'total': y[2] }) ] } )\
             for x, y in self.__budget.items() ]

    return dumps(data)

  def values(self):
    return self.__budget.values()

  def keys(self):
    return self.__budget.keys()

  def items(self):
    return self.__budget.items()

  def write(self, write_path = 'budget.json'):
    with open(write_path, 'w') as f:
      dump(self.__budget, f)



class TimeIndexKeyBudget(Budget):

  """
  TimeIndexKeyBudget uses a TimeIndexKey to implement Budget.
  """
  pass

class TimeIndexKeyRangeBudget(Budget):
  """
  TimeIndexKeyRangeBudget is optimized for range type queries on a Budget.
  """
  pass
