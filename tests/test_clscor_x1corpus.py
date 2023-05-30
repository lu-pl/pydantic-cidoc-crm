"""Pytest entry point for testing pydantic-cidoc-clr with cidoc-based custom classes (ClsCor).
"""

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
# acrynom_type = cidoc.E55Type(iri="https://types.clscor.io/entity/acronym")

corpus_identifier = cidoc.E42Identifier(
    iri="https://eltec.clscor.io/entity/corpus/id",
    p190_has_symbolic_content="eltec_en",
    p2_has_type=id_type
)

## this shows a major problem!!!
## obviously to_triples loops over a string which of course it shouldn't
# print(corpus_identifier.serialize(format="ttl"))

corpus_name = cidoc.E41Appellation(
    iri="https://eltec.clscor.io/entity/corpus/corpus_name",
    p190_has_symbolic_content="English ELTeC Corpus",
    p2_has_type=corpusname_type
)

print(corpus_name.serialize(format="ttl"))

# corpus_acronym = cidoc.E41Appellation(
#     iri="https://eltec.clscor.io/entity/corpus/acronym",
#     p190_has_symbolic_content="eltecen",
#     p2_has_type=acrynom_type
# )

# eltec_en_corpus = X1Corpus(
#     iri="https://eltec.clscor.io/entity/corpus",
#     p1_is_identified_by=[corpus_identifier, corpus_name],
# )

## this doesn't work on initial run with fresh interpreter
# print(eltec_en_corpus.serialize(format="ttl"))

# g = eltec_en_corpus.to_graph()
# print(g.serialize(format="ttl"))
