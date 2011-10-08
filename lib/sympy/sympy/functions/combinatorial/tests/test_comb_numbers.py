from sympy import bernoulli, Symbol, Sum, harmonic, Rational, oo, zoo, pi, I, bell, \
        fibonacci, lucas, euler

x = Symbol('x')

def test_bernoulli():
    assert bernoulli(0) == 1
    assert bernoulli(1) == Rational(-1,2)
    assert bernoulli(2) == Rational(1,6)
    assert bernoulli(3) == 0
    assert bernoulli(4) == Rational(-1,30)
    assert bernoulli(5) == 0
    assert bernoulli(6) == Rational(1,42)
    assert bernoulli(7) == 0
    assert bernoulli(8) == Rational(-1,30)
    assert bernoulli(10) == Rational(5,66)
    assert bernoulli(1000001) == 0

    assert bernoulli(0, x) == 1
    assert bernoulli(1, x) == x-Rational(1,2)
    assert bernoulli(2, x) == x**2-x+Rational(1,6)
    assert bernoulli(3, x) == x**3 - (3*x**2)/2 + x/2

    # Should be fast; computed with mpmath
    b = bernoulli(1000)
    assert b.p % 10**10  == 7950421099
    assert b.q == 342999030

    b = bernoulli(10**6, evaluate=False).evalf()
    assert str(b) == '-2.23799235765713e+4767529'


def test_fibonacci():
    assert [fibonacci(n) for n in range(-3, 5)] == [2, -1, 1, 0, 1, 1, 2, 3]
    assert fibonacci(100) == 354224848179261915075
    assert [lucas(n) for n in range(-3, 5)] == [-4, 3, -1, 2, 1, 3, 4, 7]
    assert lucas(100) == 792070839848372253127

    assert fibonacci(1, x) == 1
    assert fibonacci(2, x) == x
    assert fibonacci(3, x) == x**2 + 1
    assert fibonacci(4, x) == x**3 + 2*x

def test_bell():
    assert [bell(n) for n in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]

    assert bell(0, x) == 1
    assert bell(1, x) == x
    assert bell(2, x) == x**2 + x
    assert bell(5, x) == x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x

def test_harmonic():
    assert harmonic(1,1) == 1
    assert harmonic(2,1) == Rational(3,2)
    assert harmonic(3,1) == Rational(11,6)
    assert harmonic(4,1) == Rational(25,12)
    # assert harmonic(3,1) == harmonic(3)
    assert harmonic(3,5) == 1 + Rational(1,2**5) + Rational(1,3**5)
    assert harmonic(10,0) == 10
    assert harmonic(oo,1) == zoo
    assert harmonic(oo,2) == (pi**2)/6

def test_euler():
    assert euler(0) == 1
    assert euler(1) == 0
    assert euler(2) == -1
    assert euler(3) == 0
    assert euler(4) == 5
    assert euler(6) == -61
    assert euler(8) == 1385

    assert euler(20, evaluate=False) != 370371188237525

    n = Symbol('n', integer=True)
    assert euler(n) != -1
    assert euler(n).subs(n, 2) == -1

    assert euler(20).evalf() == 370371188237525.0
    assert euler(20, evaluate=False).evalf() == 370371188237525.0

    assert euler(n).rewrite(Sum) == euler(n)
    #assert euler(2*n).rewrite(Sum) ==  I*Sum(Sum((-1)**_j*2**(-_k)*I**(-_k)*(-2*_j + _k)**(2*n + 1)*binomial(_k, _j)/_k, (_j, 0, _k)), (_k, 1, 2*n + 1))
    assert euler(2*n+1).rewrite(Sum) == 0