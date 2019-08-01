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
                (('value', '?y'), '?yv'),
                (lambda x, y: x <= y, '?x', '?y')], 
               [('value', ('exp', ('value', '?x'), ('value', '?y'))),
                (lambda x, y: pow(x, y), '?xv', '?yv')])

def check_prime(x):
    if x == 2:
        return True
    else:
        for i in range(2, x):
            if x % i == 0:
                return False

    return True


def prime_factorization(x):
    num_after_factorized = x
    cur_prime = 2
    factorization_list = []

    for num in range(cur_prime, x+1):
        while check_prime(num) and num_after_factorized % num == 0:
            factorization_list.append(num)
            num_after_factorized /= num

    return factorization_list


#  import pdb; pdb.set_trace()

def find_common_base(x, y):
    smaller = min(x, y)
    larger = min(x, y)
    
    factor_list_small = prime_factorization(smaller)
    factor_list_large = prime_factorization(larger)
#  common_base_rule = Operator()



















# ^^^^^^^^^^^^^^ DEFINE ALL YOUR OPERATORS ABOVE THIS LINE ^^^^^^^^^^^^^^^^
for name,op in locals().copy().items():
  if(isinstance(op, Operator)):
    Operator.register(name,op)    
