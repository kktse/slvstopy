# slvstopy

Python library for reading a SolveSpace file as a python-solvespace system

## Getting Started

### Installing

```bash
cd slvstopy
pip install git+https://github.com/kktse/slvstopy.git
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
* Not all constraint types are implemented
* Circles are supported in 2D only
* Do not dimension from a workplane in 2D

## Motivation

 This library addresses a need to graphically draw complex mechanisms and analyze them programmatically (ex. suspension kinematic analysis).The SolveSpace project has a powerful graphical user interface for drawing and constraining mechanisms. The python-solvespace library provides Python bindings to the SolveSpace API. This library lets you move between the two without drawing the mechanism multiple times.
