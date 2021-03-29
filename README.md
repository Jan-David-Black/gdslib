# gdslib 0.2.1

Circuit simulations for Photonic components.

You can Component circuit models are

You can leverage

- Compact models for photonic components from FDTD Sparameter simulations
- Compact models from Neural networks thanks to [SiPANN](https://sipann.readthedocs.io/en/latest/?badge=latest)
- Circits simulations thanks to Open source package [simphony](https://simphonyphotonics.readthedocs.io/en/stable/) which provides a linear circuit solver for [Sparameters](https://en.wikipedia.org/wiki/Scattering_parameters)

## Usage

See jupyer notebooks

## Tests

`pytest` runs 2 types of tests:

- testing functions
- pytest-regressions over the Sparameters for components and circuits

## Installation

You can install install the latest released version.

```
pip install gdslib
```

Or you can install the development version if you plan to contribute

```
git clone https://github.com/gdsfactory/gdslib.git
cd gdslib
make install
```
