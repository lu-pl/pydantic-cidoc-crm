## Pydantic Cidoc-CRM Implementation
[![License](https://img.shields.io/github/license/jonasengelmann/pydantic-cidoc-crm)](LICENSE)

This is a fork of [pydantic-cidoc-crm](https://github.com/jonasengelmann/pydantic-cidoc-crm) which provides a Python implementation of [Cidoc-CRM 7.1.1](https://doi.org/10.26225/FDZH-X261) using [pydantic](https://pydantic-docs.helpmanual.io/) and [rdflib](https://rdflib.readthedocs.io/).

## Rationale

Using [Pydantic](https://docs.pydantic.dev/latest/) for Ontology abstractions in Python is a nifty idea; however `pydantic-cidoc-crm` doesn't utilize `rdflib`'s power to handle graph generation and serialization, which I consider a serious and unnecessary limitation.

### Changes

* 
* Changed List type to Iterable type
All model field types use union types like 'List[<type>] | <type>'; this allows multiple predicate assignment (which otherwise wouldn't be possible with argument initialization in a model, since keyword arguments obviously mustn't repeat); Iterable imo is a more general (i.e. better) choice here.

## License

This project is licensed under MIT license - see the [LICENSE](LICENSE) file for more information.
