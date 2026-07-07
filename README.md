
# SineCosSum v1.0
Academically-focused Fourier harmonic summation visualization tool, adapted to Python from original application written in Matlab by EE261 students over the years
#### Contact mferker@stanford.edu

## Tech Stack
- [NumPy](https://numpy.org/) for the calculations
- [Plot.ly](https://plotly.com/) for graphing
- [Streamlit](https://streamlit.io/) for front-end and webserver

## Codebase
- The entire application is contained within one py file for convenience.
- [Application](http://3.20.46.61/) currently running on an AWS Lightsail instance (Ubuntu 22.04)

## UX
- The application works best in a horizontal desktop experience. It also works on mobile but the CSS is not optimized for it.
- The application is best suited for an educational exploration rather than true professional harmonic analysis.
  * The amplitude, phase, frequency and A0 only accept integers rather than fractions.
  * The 3D plot uses Plot.ly's camera angle capabilities to facilitate more detailed inspection of a waveform in a non-flattened presentation, but it is not a true representation of phase.
