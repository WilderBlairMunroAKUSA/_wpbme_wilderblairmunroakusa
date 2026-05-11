





# eg A:

["<Obj>", ["<None>", [{}]]]

["<Obj>", ["<Some>", [
	[
		["<Key>", ["user"]],
		["<Str>", ["<Some>", ["dev"]]]
	]
]]]


#eg A, improved

["<Obj>", ["<None>", [{}]]]

["<Obj>", ["<Some>", [ 

	[
		["<Key>", ["<Str>", ["<Some>", ["pro"]]]],
		["<Val>", ["<Str>", ["<Some>", ["dev"]]]]
	] 
]]]

# adjusted universal container wrapper
take,
value
->
[value]
Where bracker wrapper translates to
[[type], [value]]
In json, type is always a value.
So [value] <==> [[valuetype], [valuevalue]],
which is always in valid json specification,
[[value], [value]]
Note: in case of json object value type,
a key is always a string value.

In the case where value is a literal,
singleton [value] implies
[value] = [[()], [value]] 
we should stay json valid though, so
[value] ==> [["<()>"], [value]]

Right now, we are working with byte pairs though, for any type.
Let's adjust notation one step farther, and this will help disambiguate
between json terminology, and json syntax, in concurrent contexts:

[value
