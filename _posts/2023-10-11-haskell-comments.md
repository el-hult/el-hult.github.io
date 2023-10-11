---
title: "Documenting correctness in Haskell"
tags: [haskell, programming]
---

In the Functional Programming 1 course we teach at Uppsala University, there is some confusion about how to document code.
Every year, there is confusion.
I suppose part of the problem is that many university students are not experienced enough to have seen large messy code bases. 
They have not yet worked on a single code base for more than 3 years continuously.
Therefore, they have not yet understood that everyone needs documentation to help themselves sane.

For some reason, functional programmers seem extra careful about correctness, so we put extra emphasis on the documentation in relation to correctness.
This blog post is a summary, recap and motivation for *some* of the documentation guidelines we use in the course.
I don't even remotely claim that the documentation in this post is enough to be a best practice, but I hope it provides some examples and motivation.

## Function specifications 
Functions are the core of our functional programming. Here, we put in the most effort. 

### The function name, argument names and the return

The first line in the function specification is just the function name and identifiers for the arguments

Since implementation of the function can have several patterns that introduce different code branches with different symbols in them, we define common names for arguments in the function specification.
In the below example, we match on a datatype that have different symbols in different matches. 
If the vehicle is a train, we will in implementation introduce the symbol `cars` but that is not available in the other pattern match.
Therefore, we make sure to introduce all symbols we need in the function specification, on this very first line.

{% highlight haskell %}
data Vehicle = Automobile | Train [TrainPart]
data TrainPart = PassengerCar | FreightCar | Locomotive

-- | wheels vehicle
-- when the vehicle is a train, we count the wheels on all the cars
-- RETURNS the number of wheels on the vehicle
wheels :: Vehicle -> Integer
wheels Automobile  = 4
wheels (Train cars) = 4 * (length cars)
{% endhighlight %}

The point of the `RETURNS` clause is self explanatory most of the time.


### Preconditions 

`PRE`, for preconditions. Similar to the idea in Design by Cotnract. We use the term in two principal ways

First, if the function operates on values of a type `a`, it is possible that the function is not total, and the domain of definition is smaller. The preconditions define the reduced domain of definition. Example with non-total function:
{% highlight haskell %}
-- | head xs
-- PRE: length xs > 0
-- RETURNS the first element in xs
xs :: [a] -> a
head [] = error "Called 'head' on empty list"
head (x:_) = x
{% endhighlight %}

Secondly, in stateful code (e.g. monadic), the preconditions may also describe valid states before the function is called.
Below comes an example with state monad with a counter. The count must always be nonnegative. This function decrease the counter, but does not check if the current count is `0`. So the caller must check this. 

{% highlight haskell %}
-- | INVARIANT: the count must be nonnegative
type CountState = State Int

-- | decrement
-- PRE: the current count >= 1
-- RETURNS: ()
-- SIDE EFFECT: reduce the count by one
decrement :: CountState ()
decrement = do
    count <- get
    put (count - 1)
{% endhighlight %}

### Side effects
When a function has side effects, we document them in the `SIDE EFFECT` clause. All things that make a function non-pure are side effects.

The major example is working with the IO monad.
    
{% highlight haskell %}
-- | printHello
-- SIDE EFFECT: print "Hello" to stdout
printHello :: IO ()
printHello = putStrLn "Hello"
{% endhighlight %}

Nonterminating code is also a side effect.

{% highlight haskell %}
-- | loop
-- SIDE EFFECT: does not terminate
loop = loop
{% endhighlight %}

Any non-pure function can break our equational reasoning, so we want to know about them.
Something as innocent as reading from stdin can cause a program to not be reliable. 

### Variants
Recursion variants are not as well described on the web as loop variants are. See e.g. [wikipedia](https://en.wikipedia.org/wiki/Loop_variant) for a discussion. The idea is the same, nonetheless.

The variant is an expression of the function arguments (remember, you named these on the first line of the function specification!), it takes values in a set with total order, such that all descending sequences in that set terminate. Typically, you pick the nonnegative integers as the set of values for the variant. 
The variant must also be strictly decreasing on every recursive call. Given this, there is a theorem saying that every recursive function with a variant will terminate.

One of the simplest cases, working with only integers
{% highlight haskell %}
-- | factorial n
-- PRE: n >= 0
-- RETURNS: n!
-- VARIANT: n
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n-1)
{% endhighlight %}

Next example is on lists. Here, it is not certain that the base case is when the variant is 0. But it might be.
{% highlight haskell %}
-- | zipWith f list1 list2
-- combine the lists using the function f
-- terminate as soon as either xs or ys is empty
-- VARIANT: length (list1 ++ list2)
zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
zipWith f [] _ = []
zipWith f _ [] = []
zipWith f (x:xs) (y:ys) = f x y : zipWith f xs ys
{% endhighlight %}

We might omit the variant if we do structural recursion, and can assume the datastructure to be finite.
    
{% highlight haskell %}
data RoseTree a = RoseTree a [RoseTree a]

-- | size t
-- compute size of a rose tree with structural recursion
-- RETURNS: the number of nodes in t
size :: RoseTree a -> Integer
size (RoseTree _ []) = 1
size (RoseTree _ ts) = 1 + sum (map size ts) 
{% endhighlight %}

If we have an internal helper, we might omit the function specification, but we must still include a variant statement.
    
{% highlight haskell %}
-- | sumPairs list
-- Sum up the elements in the list, pairwise
-- If there are an odd number of elements, the last element is left out
sumPairs x = go x [] 
    where
        -- go ls acc
        -- variant: lenght ls
        go (x:y:xs) acc = go xs (x+y:acc)
        go _ acc = acc
{% endhighlight %}


## Datatype Representations

Every new type, and `data`{:.haskell} in specific, should have a description of what it is, how it is represented, and whether the data type has any invariants.

The use of an invariant here is similar to a Class Invariant in Design by Contract, but has just slightly different semantics.
It is a restriction on the data type, stating some criterion that all valid values of the type must fullfil.

In the best of worlds, we would not need invariants, since the type system should make invalid values unrepresentable. 
In reality, we often have good tradeoffs where a type is more efficient or simple to code with even if it can hold invalid values.

In the example below, we back a Set with a list, and to make the type not the worst possible, we require that the backing list never contains duplicates.
This is documented on the datatype representation, and all functions returning values of the type must respect this.

{% highlight haskell %}
-- | A module for an abstract data type representing a set, with some operations
-- The constructors for Set are not exported, so the user cannot create invalid values
-- However, the functions in this module must respect the invariants of the type
module Set(Set, empty, contains, insert, fromList, toList) where

import Data.List(nub)

-- | Set 
-- A implementation of a set, based on a backing list
-- It will not get the quick performance of a ordered set or a hash set, but it is simple and
-- space efficient for very small sets
-- INVARIANT: the backing list must only hold unique values
data Set a = SetC [a] deriving Show

-- | empty
-- create an empty set
empty = SetC []

-- | insert s e
-- insert e into s
-- creates values of the type @Set@, and must thus respect the invariant
insert s@(SetC xs) e
  | s `contains` e = s
  | otherwise      = SetC (e:xs)

-- | fromList xs
-- convert @xs@ to a @Set@
-- creates values of the type @Set@, and must thus respect the invariant
fromList xs = SetC (nub xs)

-- | contains s e
-- check if e is in s
-- RETURNS: True if e is in s, False otherwise
contains (SetC xs) e = e `elem` xs

-- | toList s
-- convert @s@ to a list
-- note that since the backing list holds unique values, we don't need 
-- to deduplicate the list before returning (which would be the case if
-- we returned the invariant on @Set@)
toList (SetC xs) = xs
{% endhighlight %}

I extended this example in [this gist](https://gist.github.com/el-hult/197020edb6e860917f70a736bb35f53f)

