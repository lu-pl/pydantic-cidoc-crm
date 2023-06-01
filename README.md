## Pydantic Cidoc-CRM Implementation
[![License](https://img.shields.io/github/license/jonasengelmann/pydantic-cidoc-crm)](LICENSE)

This is a fork of [pydantic-cidoc-crm](https://github.com/jonasengelmann/pydantic-cidoc-crm), a Python implementation of [Cidoc-CRM 7.1.1](https://doi.org/10.26225/FDZH-X261) using [pydantic](https://pydantic-docs.helpmanual.io/) and [rdflib](https://rdflib.readthedocs.io/).

## Rationale

Using [Pydantic](https://docs.pydantic.dev/latest/) for Ontology abstractions in Python is a nifty idea;
leveraging Pydantic's powerful data modelling and validation functionality, OWL relationships can be expressed as Pydantic models simply by the use of Python type hints and plain subtyping.
Apart from being elegant and concise, this approach also ...

However `pydantic-cidoc-crm` doesn't utilize `rdflib`'s functioniality to handle graph generation and serialization, which could be considered a serious and unnecessary limitation. 
Also some general cleanup and basic testing would be beneficial.
  
### Changes

* Refactored `RDFBaseModel.to_triples`

    `RDFBaseModel.to_triples` is now a *recursive generator*. Generated triples are no longer (C-style) appended to a list, but lazily yielded.
	
* Refactored `RDFBaseModel.serialize`

    `RDFBaseModel.serialize` is now an `rdflib.Graph.serialize` proxy that uses an internal `rdflib.Graph` component; this allows for far more powerful serialization funcitonality (see [rdflib.Graph.serialize](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.serialize)).
	
* Simplified `_convert_to_rdf_literl`

    Actually `rdflib.Literal` handles conversions and datatype assignment well by itself.
	
* ~~Changed `List` to `Iterable` type in all model field types~~

	~~All model field types use union types like `List[<type>] | <type>`; this allows multiple predicate assignment (which otherwise wouldn't be possible with argument initialization in a model, since keyword arguments obviously mustn't repeat); `Iterable` imo is a more general (i.e. better) choice here.
Note that this requires an origin check in `to_triples`.~~
    
	This caused a major bug since pydantic auto-sanitizes fields to generators when Iterable is defined in the union type.
	
* Merged `AbstractBaseModel` and `RDFBaseModel` and moved to `rdfbasemodel` module

    Separation of `AbstractBaseModel` and `RDFBaseModel` seems somewhat motiveless; also I find having `mapping` assigned right in the base class is more concise.


## License

This project is licensed under MIT license - see the [LICENSE](LICENSE) file for more information.
