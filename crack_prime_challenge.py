#!/bin/python

#56807
#52379
#done
#sum 109186
import itertools

def is_prime(n):
  i = 2
  while i < n:
    if n%i == 0:
      return False
    i += 1
  return True

n = int(raw_input("What number should I go up to? "))

primes = [];
p = 2
while p <= n:
  if is_prime(p):
    primes.append(p);
  p=p+1
#print primes;
#print "done"
print "primes calculated"

for it in itertools.product(primes,repeat=2):
  fact = it[0] * it[1];
  if (fact==2975493853):
    print "FOUND"
    print it[0];
    print it[1];
    exit
print "done"

