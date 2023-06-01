## Pydantic Cidoc-CRM Implementation
[![License](https://img.shields.io/github/license/jonasengelmann/pydantic-cidoc-crm)](LICENSE)

This is a fork of [pydantic-cidoc-crm](https://github.com/jonasengelmann/pydantic-cidoc-crm), a Python implementation of [Cidoc-CRM 7.1.1](https://doi.org/10.26225/FDZH-X261) using [pydantic](https://pydantic-docs.helpmanual.io/) and [rdflib](https://rdflib.readthedocs.io/).

## Rationale

Using [Pydantic](https://docs.pydantic.dev/latest/) for Ontology abstractions in Python is a nifty idea;
leveraging Pydantic's powerful data modelling and validation functionality, OWL relationships can be expressed as Pydantic models simply by the use of Python type hints and plain subtyping.
This approach is not only elegant and concise, but also makes available the full might of Pydantic for Ontology mappings, e.g. one can easily derive JSON Schema from a Pydantic Ontology model.

However `pydantic-cidoc-crm` doesn't utilize `rdflib`'s functioniality to handle graph generation and serialization, which could be considered a serious and unnecessary limitation. 
Also some general cleanup and basic testing would be beneficial.
  
### Changes

* Refactored `RDFBaseModel.to_triples`

    `RDFBaseModel.to_triples` is now a *recursive generator*. Generated triples are no longer (C-style) appended to a list, but lazily yielded.
	
* Refactored `RDFBaseModel.serialize`

    `RDFBaseModel.serialize` is now an `rdflib.Graph.serialize` proxy that uses an internal `rdflib.Graph` component; this allows for far more powerful serialization functionality (see [rdflib.Graph.serialize](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.serialize)).
	
* Simplified `_convert_to_rdf_literl`

    Actually `rdflib.Literal` handles conversions and datatype assignment well by itself.
	
* ~~Changed `List` to `Iterable` type in all model field types~~

	~~All model field types use union types like `List[<type>] | <type>`; this allows multiple predicate assignment (which otherwise wouldn't be possible with argument initialization in a model, since keyword arguments obviously mustn't repeat); `Iterable` imo is a more general (i.e. better) choice here.
Note that this requires an origin check in `to_triples`.~~
    
	This caused a major bug since pydantic auto-sanitizes fields to generators when Iterable is defined in the union type.
	
* Merged `AbstractBaseModel` and `RDFBaseModel` and moved to `rdfbasemodel` module

    Separation of `AbstractBaseModel` and `RDFBaseModel` seems somewhat motiveless; also I find having `mapping` assigned right in the base class is more concise.

## Example

The following example uses a cidoc-based custom class and shows how to serialize RDF from an object representation: 

```python
import pydantic_cidoc_crm as cidoc


class D1DigitalObject(cidoc.E73InformationObject):
    """D1DigitalObject: https://ontome.net/class/477/namespace/47."""
    pass


class F3Manifestation:
    """F3Manifestation:  https://cidoc-crm.org/f3-manifestation-product-type.

    This is just a dummy for a FRBRoo class.
    """
    pass


class X1Corpus(D1DigitalObject, F3Manifestation):
    """ClsCor X1Corpus implementation."""

    def __init__(self, *args, **kwargs):
        """Add ClsCor URIs to _mappings.

        Note: In a full ClsCor Implemenation _mapping.update should
        probably be moved to the base class.
        """
        super().__init__(*args, **kwargs)

        self._mapping.update(
            {
                "X1Corpus": "https://clscor.io/ontologies/CRMcls/X1Corpus"
            }
        )


id_type = cidoc.E55Type(iri="https://types.clscor.io/entity/id")
corpusname_type = cidoc.E55Type(iri="https://types.clscor.io/entity/corpus_name")
acrynom_type = cidoc.E55Type(iri="https://types.clscor.io/entity/acronym")

corpus_identifier = cidoc.E42Identifier(
    iri="https://eltec.clscor.io/entity/corpus/id",
    p190_has_symbolic_content="eltec_en",
    p2_has_type=id_type
)

corpus_name = cidoc.E41Appellation(
    iri="https://eltec.clscor.io/entity/corpus/corpus_name",
    p190_has_symbolic_content="English ELTeC Corpus",
    p2_has_type=corpusname_type
)

corpus_acronym = cidoc.E41Appellation(
    iri="https://eltec.clscor.io/entity/corpus/acronym",
    p190_has_symbolic_content="eltecen",
    p2_has_type=acrynom_type
)

eltec_en_corpus = X1Corpus(
    iri="https://eltec.clscor.io/entity/corpus",
    p1_is_identified_by=[corpus_identifier, corpus_name],
)

# ttl
print(eltec_en_corpus.serialize(format="ttl"))

# xml
print(eltec_en_corpus.serialize(format="xml"))
```

Outpout for ttl:
```ttl
@prefix ns1: <http://www.cidoc-crm.org/cidoc-crm/> .

<https://eltec.clscor.io/entity/corpus> a <https://clscor.io/ontologies/CRMcls/X1Corpus> ;
    ns1:P1_is_identified_by <https://eltec.clscor.io/entity/corpus/corpus_name>,
        <https://eltec.clscor.io/entity/corpus/id> .

<https://eltec.clscor.io/entity/corpus/corpus_name> a ns1:E41_Appellation ;
    ns1:P190_has_symbolic_content "English ELTeC Corpus" ;
    ns1:P2_has_type <https://types.clscor.io/entity/corpus_name> .

<https://eltec.clscor.io/entity/corpus/id> a ns1:E42_Identifier ;
    ns1:P190_has_symbolic_content "eltec_en" ;
    ns1:P2_has_type <https://types.clscor.io/entity/id> .

<https://types.clscor.io/entity/corpus_name> a ns1:E55_Type .

<https://types.clscor.io/entity/id> a ns1:E55_Type .
```

Outpout for xml:
```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
   xmlns:ns1="http://www.cidoc-crm.org/cidoc-crm/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="https://types.clscor.io/entity/id">
    <rdf:type rdf:resource="http://www.cidoc-crm.org/cidoc-crm/E55_Type"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://eltec.clscor.io/entity/corpus/id">
    <rdf:type rdf:resource="http://www.cidoc-crm.org/cidoc-crm/E42_Identifier"/>
    <ns1:P2_has_type rdf:resource="https://types.clscor.io/entity/id"/>
    <ns1:P190_has_symbolic_content>eltec_en</ns1:P190_has_symbolic_content>
  </rdf:Description>
  <rdf:Description rdf:about="https://eltec.clscor.io/entity/corpus/corpus_name">
    <rdf:type rdf:resource="http://www.cidoc-crm.org/cidoc-crm/E41_Appellation"/>
    <ns1:P2_has_type rdf:resource="https://types.clscor.io/entity/corpus_name"/>
    <ns1:P190_has_symbolic_content>English ELTeC Corpus</ns1:P190_has_symbolic_content>
  </rdf:Description>
  <rdf:Description rdf:about="https://types.clscor.io/entity/corpus_name">
    <rdf:type rdf:resource="http://www.cidoc-crm.org/cidoc-crm/E55_Type"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://eltec.clscor.io/entity/corpus">
    <rdf:type rdf:resource="https://clscor.io/ontologies/CRMcls/X1Corpus"/>
    <ns1:P1_is_identified_by rdf:resource="https://eltec.clscor.io/entity/corpus/id"/>
    <ns1:P1_is_identified_by rdf:resource="https://eltec.clscor.io/entity/corpus/corpus_name"/>
  </rdf:Description>
</rdf:RDF>
```

## License

This project is licensed under MIT license - see the [LICENSE](LICENSE) file for more information.
