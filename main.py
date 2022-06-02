# Imports
import numpy as num
#from sympy.plotting import plot as symplot
#from numpy.fft import fft, ifft
import matplotlib.pyplot as plot
#--

# Global variables
f_passband = 80000 #kHz
f_stopband = 55000 #kHz
f_sampling = 220000 #kHz
passband_attenuation = 0.25 #Db
stopband_attenuation = 45 #Db

#--

# Function definitions
def bodePlot(H):
    from scipy import signal
    import matplotlib.pyplot as plt
    import numpy as np

    w_start = 0.01
    w_stop = 10
    step = 0.001
    N = int((w_stop - w_start) / step) + 1
    w = np.linspace(w_start, w_stop, N)
    # Bode Plot
    w, mag, phase = signal.bode(H, w)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.semilogx(w, mag)  # Bode Magnitude Plot
    plt.title("Bode Plot")
    plt.grid(visible=True, which='major', axis='both')
    plt.grid(visible=True, which='major', axis='both')
    plt.ylabel("Magnitude (dB)")
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)  # Bode Phase plot
    plt.grid(visible=True, which='major', axis='both')
    plt.grid(visible=True, which='minor', axis='both')
    plt.ylabel("Phase (deg)")
    plt.xlabel("Frequency (kHz)")
    plt.show()

def generateSignal() :
    # Constructing composite signal
    sample_rate = f_sampling
    sample_period = 1 / sample_rate
    time = num.arange(0, 0.001, sample_period)  # Sample set up to got from 0 - 2 seconds

    # Signal 1
    freq = 65000
    y = num.sin(2 * num.pi * freq * time)
    # Signal 2
    freq = 40000
    y += num.sin(2 * num.pi * freq * time)
    # Signal 3
    freq = 100000
    y += num.sin(2 * num.pi * freq * time)

  #  Time domain plot of signal
  #   plot.figure(figsize=(6, 4))
  #   plot.title('Plot of sampled signal y')
  #   plot.xlabel('Time (s)')
  #   plot.ylabel('Amplitude')
  #   plot.plot(time,y,'b') # Remove this line to see only the samples of the signal.
  #   plot.stem(time,y,'r')
  #   plot.show()
    return y


# Main script
def main():
    # Local variables
    import numpy as num
    import sympy as sym
    from scipy import signal
    import matplotlib.pyplot as plt
    #--

    y = generateSignal()
    print("The sampled signal is the following array:\n %r \n" %(y))

    # Normalize digital frequencies --
    print("Sampling frequency: ", f_sampling, " Hz")
    w_p = (2 * num.pi * f_passband)/(f_sampling)
    w_s = (2 * num.pi * f_stopband)/(f_sampling)

    print("Normalized passband: ", w_p, " rad/s")
    print("Normalized stopband: ", w_s, " rad/s\n")

    # Sampling wrapping equations, digital to analogue domain --
    Omega_p = num.tan(w_p/2)
    Omega_s = num.tan(w_s/2)
    print("Omega_p :", Omega_p, "rad/s")
    print("Omega_s :", Omega_s, "rad/s\n")

    # Swap normalized analogue frequencies --
    temp = Omega_s
    Omega_s = Omega_p
    Omega_p = temp

    # Convert to analogue frequencies --
    f_ap = (Omega_p * f_sampling)/(2 * num.pi)
    f_as = (Omega_s * f_sampling) / (2 * num.pi)

    print("The normalized analogue frequencies are swapped to form a prototype low-pass filter. The new pass- and stop-bands are determined.")
    print("Analogue passband: ", f_ap, " Hz")
    print("Analogue stopband: ", f_as, " Hz\n")

    Omega = f_as/f_ap
    print("Omega for determining filter order: ", Omega, "\n")

    a = 0.27005
    b = 1.09543
    c = 0.70700
    d = 0.53642
    e = 0.43695
    k = 0.25676

    s = sym.symbols('s')
    z = sym.symbols('z')

    numerator = (1*s**2 + a*s + b)*(1*s**2 + c*s + d)*(1*s + e)
    denominator = k

    H_LP = numerator/denominator
    H_LP = sym.expand(H_LP)
    print("\nThe transfer function of the prototype analogue low-pass filter is H_LP(s) = \n", sym.expand(H_LP))
    b = np.array([3.89468764605079, 5.50708833151581, 8.76186846666148, 6.68246970004089, 3.85305915284877, 0.999986113312704])
    a = np.array([0, 0, 0, 0, 1])
    H = signal.TransferFunction(a, b)
    bodePlot(H)

    # De-normalize and transform to high-pass filter --
    H_HP = H_LP.subs(s, f_as/s)
    print("\nThe analogue transfer function of the high-pass filter is determined by making the substitution s = (f_as/s) and is given by H_HP(s) = \n", sym.expand(H_HP))
    b = np.array([1.03182107805362e+25, 1.9029503287469e+20, 3.94889682379915e+15, 39281648321.8845, 295414.650115535, 0.999986113312704])
    a = np.array([0, 0, 0, 0, 1])
    H = signal.TransferFunction(a, b)
    bodePlot(H)

    # Transform to Z domain --
    H_HP_z = H_HP.subs(s, ((z-1)/(z+1)))
    H_HP_fact_z = sym.factor(H_HP_z)

    print("\nThe high-pass filter is taken to the z-domain by making the substitution s = ((z-1)/(z+1)) -- The bilinear transform.")
    print("The new transfer function is H_HP(z) = \n", H_HP_fact_z)
    b = [1.031840107951801e+25, 5.159162479172857e+25, 1.031824883875300e+26, 1.031817272073987e+26, 5.159048302153137e+25, 1.031802048945219e+25]
    a = [1, -5, 10, -10, 5, -1]
    H = signal.TransferFunction(a, b)
    bodePlot(H)

#--

if __name__ == "__main__":
   main()