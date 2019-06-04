# This example describe how to integrate ODEs with scipy.integrate module, and how
# to use the matplotlib module to plot trajectories, direction fields and other
# useful information.
#
# == Presentation of the Lokta-Volterra Model ==
#
# We will have a look at the Lokta-Volterra model, also known as the
# predator-prey equations, which are a pair of first order, non-linear, differential
# equations frequently used to describe the dynamics of biological systems in
# which two species interact, one a predator and one its prey. They were proposed
# independently by Alfred J. Lotka in 1925 and Vito Volterra in 1926:
# du/dt =  a*u -   b*u*v
# dv/dt = -c*v + d*b*u*v
#
# with the following notations:
#
# *  u: number of preys (for example, rabbits)
#
# *  v: number of predators (for example, foxes)
#
# * a, b, c, d are constant parameters defining the behavior of the population:
#
#   + a is the natural growing rate of rabbits, when there's no fox
#
#   + b is the natural dying rate of rabbits, due to predation
#
#   + c is the natural dying rate of fox, when there's no rabbit
#
#   + d is the factor describing how many caught rabbits let create a new fox
#
# We will use X=[u, v] to describe the state of both populations.
#
# Definition of the equations:
#
from numpy import *
import numpy
import matplotlib.pylab as pylab
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import integrate

# Definition of parameters


# a is the natural growing rate of rabbits, when there's no fox

# b is the natural dying rate of rabbits, due to predation

# c is the natural dying rate of fox, when there's no rabbit

# d is the factor describing how many caught rabbits let create a new fox
a = 1.
b = 0.1
c = 1.5
d = 0.75
def dX_dt(X,t, a, b, c, d):
    """ Return the growth rate of fox and rabbit populations. """
    return array([ a*X[0] -   b*X[0]*X[1] ,
                   -c*X[1] + d*b*X[0]*X[1] ])
def d2X_dt2(X, t, a, b, c, d):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[a -b*X[1],   -b*X[0]     ],
                  [b*d*X[1] ,   -c +b*d*X[0]] ])
#
# === Population equilibrium ===
#
# Before using !SciPy to integrate this system, we will have a closer look on
# position equilibrium. Equilibrium occurs when the growth rate is equal to 0.
# This gives two fixed points:
#
X_f0 = array([     0. ,  0.])
X_f1 = array([c / (d * b), a / b])
all(dX_dt(X_f0, 0, a, b, c, d) == zeros(2)) and all(dX_dt(X_f1, 0, a, b, c, d) == zeros(2)) # => True
#
# === Stability of the fixed points ===
# Near theses two points, the system can be linearized:
# dX_dt = A_f*X where A is the Jacobian matrix evaluated at the corresponding point.
# We have to define the Jacobian matrix:
#

#
# So, near X_f0, which represents the extinction of both species, we have:
# A_f0 = d2X_dt2(X_f0)                    # >>> array([[ 1. , -0. ],
#                                         #            [ 0. , -1.5]])
#
# Near X_f0, the number of rabbits increase and the population of foxes decrease.
# The origin is a [http://en.wikipedia.org/wiki/Saddle_point saddle point].
#
# Near X_f1, we have:
A_f1 = d2X_dt2(X_f1, 0, a, b, c, d)

# whose eigenvalues are +/- sqrt(c*a).j:
lambda1, lambda2 = linalg.eigvals(A_f1) # >>> (1.22474j, -1.22474j)

# They are imaginary number, so the fox and rabbit populations are periodic and
# their period is given by:
T_f1 = 2*pi/abs(lambda1)                # >>> 5.130199
#
# == Integrating the ODE using scipy.integate ==
#
# Now we will use the scipy.integrate module to integrate the ODEs.
# This module offers a method named odeint, very easy to use to integrate ODEs:
#

t = linspace(0, 15,  1000)              # time
X0 = array([10, 5])                     # initials conditions: 10 rabbits and 5 foxes

X, infodict = integrate.odeint(dX_dt, X0, args=(a, b, c, d), t=t, full_output=True)
infodict['message']                     # >>> 'Integration successful.'
#
# `infodict` is optional, and you can omit the `full_output` argument if you don't want it.
# Type "info(odeint)" if you want more information about odeint inputs and outputs.
#
# We can now use Matplotlib to plot the evolution of both populations:
#
rabbits, foxes = X.T
f1, ax = pylab.subplots()
pylab.subplots_adjust(left=0.15, bottom=0.55)

plot1, = pylab.plot(t, rabbits, lw=2, color='red', label='Ofiary')
plot2, = pylab.plot(t, foxes, lw=2, color='blue', label='Drapieżniki')
pylab.grid()
pylab.legend(loc='best')
pylab.xlabel('Czas')
pylab.ylabel('Populacja')
pylab.title('Model Lotka-Volterra')
pylab.axis([0, 15, 0, 100])


axcolor = 'lightgoldenrodyellow'
axa = pylab.axes([0.1, 0.35, 0.75, 0.03], facecolor=axcolor, title='Współczynnik narodzin ofiar')
axb = pylab.axes([0.1, 0.25, 0.75, 0.03], facecolor=axcolor, title='Współczynnik śmierci ofiar')
axc = pylab.axes([0.1, 0.15, 0.75, 0.03], facecolor=axcolor, title='Współczynnik śmierci drapieżników')
axd = pylab.axes([0.1, 0.05, 0.75, 0.03], facecolor=axcolor, title='Efektywność uśmiercania ofiar')
sa = Slider(axa, 'a', 0.1, 10.0, valinit=1.)
sb = Slider(axb, 'b', 0.01, 1.0, valinit=0.1)
sc = Slider(axc, 'c', 0.1, 10.0, valinit=1.5)
sd = Slider(axd, 'd', 0.1, 10.0, valinit=0.75)

def update(val):
    a = sa.val
    b = sb.val
    c = sc.val
    d = sd.val
    X, infodict = integrate.odeint(dX_dt, X0, args=(a, b, c, d), t=t, full_output=True)
    rabbits, foxes = X.T
    plot1.set_ydata(rabbits)
    plot2.set_ydata(foxes)
    f1.canvas.draw_idle()
sa.on_changed(update)
sb.on_changed(update)
sc.on_changed(update)
sd.on_changed(update)


pylab.show()
f1.savefig('rabbits_foxes.png')
#
#
# The populations are indeed periodic, and their period is near to the T_f1 we calculated.
#
