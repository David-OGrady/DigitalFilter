# ddaDigitalFilter
Repository for the design and in code implementation and realization of a digital filter.
Code repository for designing an IIR digital filter. 
Properties of the filter are as follows, the digitl filter must NOT be a butterworth filter:
- Digital HIGH-PASS filter with infinite impulse response (IIR).
- Operation above 200 kHz.
- Passband lower than 85 kHz.
- Passband ripple less than 0.3 dB.
- Minimum stopband attenuation of 40 dB.
- Stopband cutoff frequency of 45 kHz using the bilinear tranform.

The implementation must be done from first principles, supporting libraries may NOT be used - direct form cascaded implementation.
The use of a virtual environment is advised.
