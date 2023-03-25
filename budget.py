class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = []

  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})

  def withdraw(self, amount, description=''):
    neg_amount = 0 - amount
    if self.check_funds(amount):
      self.ledger.append({'amount': neg_amount, 'description': description})
      return True
    return False

  def get_balance(self):
    amount = 0
    for items in self.ledger:
      amount += items['amount']
    return amount

  def transfer(self, amount, category: 'Category'):
    if self.check_funds(amount):
      self.withdraw(amount, description=f"Transfer to {category.category}")
      category.deposit(amount, description=f"Transfer from {self.category}")
      return True
    return False

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    return False

  def __repr__(self):
    remainder = (30 - len(self.category)) // 2
    top_line = '*' * remainder + self.category + '*' * remainder + '\n'
    remaining_lines = str()
    for desc in self.ledger:
      remaining_lines += f"{desc['description'][:23]:<23}{desc['amount']:>7.2f}" + '\n'
    return top_line + remaining_lines + 'Total: ' + f'{self.get_balance():<.2f}'


def create_spend_chart(categories):
  total_spent = 0
  spent_by_cat = []
  graph = "Percentage spent by category\n"
  for items in categories:
    cat_total = 0
    for spent in items.ledger:
      if spent['amount'] < 0:
        total_spent += abs(spent['amount'])
        cat_total += abs(spent['amount'])
    spent_by_cat.append(cat_total)

  percentage_by_cat = [
    int(item / total_spent * 100) // 10 * 10 for item in spent_by_cat
  ]

  labels = [
    '100| ', ' 90| ', ' 80| ', ' 70| ', ' 60| ', ' 50| ', ' 40| ', ' 30| ',
    ' 20| ', ' 10| ', '  0| '
  ]
  for items in labels:
    line = items
    for per in percentage_by_cat:
      if int(items.strip()[:-1]) > per:
        line += ' ' * 3
      else:
        line += 'o  '

    graph += line + '\n'
  graph += '    ' + '-' * (len(categories) * 3 + 1) + '\n'

  max_length = 0
  for items in categories:
    if len(items.category) >= max_length:
      max_length = len(items.category)

  for index in range(max_length):
    line = ' ' * 5
    for items in categories:
      if len(items.category) > index:
        line += items.category[index] + ' ' * 2
      else:
        line += ' ' * 3
    graph += line + '\n'

  return graph[:-1]
