# slvstopy

Python library for reading SolveSpace files to a python-solvespace systems.

## Getting Started

### Installing

Use local repository as install path. Install instructions subject to change when the project is made public.

```bash
cd slvstopy
pip install .
```

### Example

```python
from slvstopy import load_from_filepath

filepath = 'path/to/your/solvespace/file.slvs'
system, entities = load_from_filepath(filepath)
```

Where:

* `system` is a `SolverSystem`
* `entities` is a dictionary of type `Dict[str, Entity]` with dictionary keys corresponding to the entity id (ie. `Entity.h.v`)

## Running Tests

### Environment

The `requirements.txt` file needs work before it is ready.

```bash
pip install requirements.txt
pip install -e .
```

### Testing

```bash
pytest
```

## Dependencies

This library uses [`python-solvespace`](https://github.com/KmolYuan/solvespace/tree/python/cython) as a SolveSpace backend. This library will only support entities implemented by `python-solvespace`.

## Caveats

* Entities and constraints only
* Not all entity types are implemented
* Circles are supported in 2D only
* Do not dimension from the reference planes for 2D linkages

## Motivation

The SolveSpace project has a powerful graphical user interface for drawing and constraining mechanisms. This library addressed a need to graphically draw complex mechanisms and analyze them programmatically (ex. suspension kinematic analysis).
