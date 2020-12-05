# slvstopy

Python library for reading a [SolveSpace](https://solvespace.com/index.pl) file as a [`python-solvespace`](https://github.com/KmolYuan/solvespace/tree/python/cython) system.

## Getting Started

### Installing

```bash
pip install git+https://github.com/kktse/slvstopy.git
```

### Example

```python
from slvstopy import Slvstopy

system_factory = Slvstopy('path/to/your/solvespace/file.slvs')
system, entities = system_factory.generate_system()
```

Where:

* `system` is a `SolverSystem`
* `entities` is a dictionary of type `Dict[str, Entity]` with dictionary keys corresponding to the entity id (ie. `Entity.h.v`)

## Running Tests

### Environment

Create a virtual environment (ex. `python -m venv env`) and run the following command to install project dependencies:

```bash
make init
```

### Testing

To run unit tests:

```bash
make test
```

With code coverage:

```back
make test-coverage
```

### Linting

```bash
make lint
```

### Formatting

```bash
make format
```

## Dependencies

This library uses [`python-solvespace`](https://github.com/KmolYuan/solvespace/tree/python/cython) as a SolveSpace backend. This library will only support entities implemented by `python-solvespace`.

## Caveats

* Entities and constraints only
* Not all entity types are implemented
* Not all constraint types are implemented
* Circles are supported in 2D only
* Do not dimension from a workplane in 2D

## Motivation

 This library addresses a need to graphically draw complex mechanisms and analyze them programmatically.
