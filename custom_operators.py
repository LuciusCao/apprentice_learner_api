from planners.fo_planner import Operator
# from planners.VectorizedPlanner import BaseOperator

'''							USAGE INSTRUCTIONS 
FO Operator Structure: Operator(<header>, [<conditions>...], [<effects>...])

	<header> : ('<name>', '?<var_1>', ... , '?<var_n>')
			example : ('Add', '?x', '?y')
	<conditions> : [(('<attribute>', '?<var_1>'),'?<value_1>'), ... ,
					 (<func>, '?<value_1>', ...), ...
				   ]
			example : [ (('value', '?x'), '?xv'),
	                  (('value', '?y'), '?yv'),
	                  (lambda x, y: x <= y, '?x', '?y')
	                  ]
	<effects> : [(<out_attribute>, 
				 	('<name>', ('<in_attribute1>', '?<var_1>'), ...),
				  	(<func>, '?<value_1>', ...)
			     ), ...]
			example :[(('value', ('Add', ('value', '?x'), ('value', '?y'))),
	                     (int_float_add, '?xv', '?yv'))])
	Full Example: 
	def int_float_add(x, y):
	    z = float(x) + float(y)
	    if z.is_integer():
	        z = int(z)
	    return str(z)
    
	add_rule = Operator(('Add', '?x', '?y'),
			            [(('value', '?x'), '?xv'),
			             (('value', '?y'), '?yv'),
			             (lambda x, y: x <= y, '?x', '?y')
			             ],
			            [(('value', ('Add', ('value', '?x'), ('value', '?y'))),
			              (int_float_add, '?xv', '?yv'))])
	
	Note: You should explicitly register your operators so you can
			 refer to them in your training.json, otherwise the name will
			 be the same as the local variable 
			example: Operator.register("Add")

vvvvvvvvvvvvvvvvvvvv WRITE YOUR OPERATORS BELOW vvvvvvvvvvvvvvvvvvvvvvv '''


exp = Operator(('exp', '?x', '?y'),
               [(('value', '?x'), '?xv'), 
                (('value', '?y'), '?yv')],
               [(('value', ('exp', ('value', '?x'), ('value', '?y'))),
                (lambda x, y: str(pow(int(x), int(y))), '?xv', '?yv'))])


def check_prime(x):
    x = int(x)
    if x == 2:
        return True
    else:
        for i in range(2, x):
            if x % i == 0:
                return False

    return True


def prime_factorization(x):
    x = int(x)
    num_after_factorized = x
    cur_prime = 2
    factorization_list = []

    for num in range(cur_prime, num_after_factorized):
        while check_prime(num) and num_after_factorized % num == 0:
            factorization_list.append(num)
            num_after_factorized /= num

    return factorization_list


def if_common_base_exists(x, y):
    x = int(x)
    y = int(y)

    smaller = min(x, y)
    larger = max(x, y)

    factor_list_small = prime_factorization(smaller)
    factor_list_large = prime_factorization(larger)

    factor_set_small = set(factor_list_small)
    factor_set_large = set(factor_list_large)

    if not factor_set_small == factor_set_large:
        return '2'

    from collections import Counter
    small_counter = Counter(factor_list_small)
    large_counter = Counter(factor_list_large)

    scale = []
    for k, v in small_counter.items():
        scale.append(large_counter[k] / v) # may require round here

    scale_set = set(scale)
    if len(scale_set) == 1:
        return '1'
    else:
        return '2'


def find_common_base(x, y):
    x = int(x)
    y = int(y)
    smaller = min(x, y)
    larger = min(x, y)
    
    factor_list_small = prime_factorization(smaller)
    factor_list_large = prime_factorization(larger)

    from collections import Counter
    small_counter = Counter(factor_list_small)
    large_counter = Counter(factor_list_large)

    factor_set = set(factor_list_small)

    if len(factor_set) == 1:
        return factor_set.pop()

    common_base_factor = []
    
    scale = min(small_counter[k] for k in factor_set)
    if all(small_counter[k] % scale == 0  for k in factor_set):
        common_base_counter = {k: v // scale for k,v in small_counter.items()}
        for k, v in common_base_counter.items():
            for i in range(v):
                common_base_factor.append(k)
    else:
        for k,v in small_counter.items():
            for i in range(v):
                common_base_factor.append(k)

    common_base = 1
    for f in common_base_factor:
        common_base *= f

    return str(common_base)
    
common_base_exists = Operator(('common_base_exists', '?x', '?y'), 
                              [(('value', '?x'), '?xv'),
                               (('value', '?y'), '?yv'),
                               #  ('is_str_number', '?xv'),
                               #  ('is_str_number', '?yv'),
                               (lambda x, y: x <= y, '?x', '?y')],
                              [(('value', ('common_base_exists', ('value', '?x'), ('value', '?y')))),
                               (if_common_base_exists, '?xv', '?yv')])

common_base = Operator(('common_base', '?x', '?y'),
                       [(('value', '?x'), '?xv'),
                        (('value', '?y'), '?yv'),
                        #  ('is_str_number', '?xv'),
                        #  ('is_str_number', '?yv'),
                        (lambda x, y: x <= y, '?x', '?y')],
                       [(('value', ('common_base', ('value', '?x'), ('value', '?y')))),
                        (find_common_base, '?xv', '?yv')])


def find_exp(original_base, base):
    original_base = int(original_base)
    base = int(base)
    number = original_base

    if original_base < base:
        raise Exception('original_base must be gte the new base')
    elif base == 1:
        raise Exception('base cannot be 1')
    elif original_base < 0 or base < 0:
        raise Exception('both original_base and base need to be larger than 0')

    exp = 0
    while number != 1:
        number /= base
        if not number.is_integer():
            raise Exception('invalid number&base combination')
        else:
            exp += 1

    return str(exp)

find_exp = Operator(('find_exp', '?x', '?y'),
                    [(('value', '?x'), '?xv'),
                     (('value', '?y'), '?yv'),
                     #  ('is_str_number', '?xv'),
                     #  ('is_str_number', '?yv'),
                     (lambda x, y: x <= y, '?x', '?y')],
                    [(('value', ('find_exp', ('value', '?x'), ('value', '?y')))),
                     (find_exp, '?xv', '?yv')])

#  import pdb; pdb.set_trace()

# ^^^^^^^^^^^^^^ DEFINE ALL YOUR OPERATORS ABOVE THIS LINE ^^^^^^^^^^^^^^^^
for name,op in locals().copy().items():
  if(isinstance(op, Operator)):
    Operator.register(name,op)    
