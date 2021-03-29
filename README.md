# gdslib 0.2.1

Circuit simulations for Photonic components.

You can leverage:

- Compact models for photonic components from FDTD Sparameter simulations
- Compact models from Neural networks thanks to [SiPANN package](https://sipann.readthedocs.io/en/latest/?badge=latest)
- Circits simulations thanks to [simphony](https://simphonyphotonics.readthedocs.io/en/stable/) which provides a linear circuit solver for [Sparameters](https://en.wikipedia.org/wiki/Scattering_parameters). Which allows you to compute the spectral response of a circuit made of different components connected together.

## Usage

See jupyer notebooks

## Tests

`make test` runs 2 types of tests with pytest:

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
