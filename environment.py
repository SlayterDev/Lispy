import math
import operator as op

Symbol = str
List   = list
Number = (int, float)

class Procedure(object):
	def __init__(self, params, body, env):
		self.params, self.body, self.env = params, body, env

	def __call__(self, *args):
		return eval(self.body, Env(self.params, args, self.env))

class Env(dict):
	def __init__(self, params=(), args=(), outer=None):
		self.update(zip(params, args))
		self.outer = outer

	def find(self, var):
		try:
			return self if (var in self) else self.outer.find(var)
		except AttributeError:
			raise SyntaxError("'" + var + "' is not defined")

def standard_env():
	env = Env()
	env.update(vars(math)) # sin, cos, sqrt, pi, etc...
	env.update({
		'+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
		'>': op.gt,  '<': op.lt,  '>=': op.ge, '<=': op.le, '=': op.eq,
		'abs':        abs,
		'append':     op.add,
		'apply':      apply,
		'begin':      lambda *x: x[-1],
		'car':	      lambda x: x[0],
		'cdr':	      lambda x: x[1:],
		'cons':	      lambda x,y: [x] + y,
		'eq?':	      op.is_,
		'equal?':     op.eq,
		'length':     len,
		'list':	      lambda *x: list(x),
		'list?':      lambda x: isinstance(x, list),
		'map':	      map,
		'max':	      max,
		'min':	      min,
		'not':	      op.not_,
		'null?':      lambda x: x == [],
		'number?':    lambda x: isinstance(x, Number),
		'procedure?': callable,
		'round':	  round,
		'symbol?':	  lambda x: isinstance(x, Symbol)
	})
	return env

global_env = standard_env()

def eval(x, env=global_env):
	if isinstance(x, Symbol): # variable reference
		return env.find(x)[x]
	elif not isinstance(x, List): # constant literal
		return x
	elif x[0] == 'quote': # quote
		(_, exp) = x
		return exp
	elif x[0] == 'if': # if statement
		(_, test, conseq, alt) = x
		exp = (conseq if eval(test, env) else alt)
		return eval(exp, env)
	elif x[0] == 'define': # definition
		(_, var, exp) = x
		env[var] = eval(exp, env)
	elif x[0] == 'set!': # assignment
		(_, var, exp) = x
		env.find(var)[var] = eval(exp, env)
	elif x[0] == 'lambda': # procedure
		(_, params, body) = x
		return Procedure(params, body, env)
	else: #procedure call
		proc = eval(x[0], env)
		args = [eval(arg, env) for arg in x[1:]]
		return proc(*args)

