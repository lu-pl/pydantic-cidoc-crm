"""Pydantic base model and configuration for RDFBaseModel."""

import abc
from typing import Any, Generator, overload, Union, get_origin
import datetime
from collections.abc import Iterable, MutableMapping

import mapping

from pydantic import BaseModel, Field
from rdflib import Literal, URIRef, Graph
from rdflib.namespace import RDF, XSD

_Triple = tuple[URIRef, URIRef, URIRef | Literal]


class NotInMapping(Exception):
    pass


class InvalidType(Exception):
    pass


class RDFBaseModel(BaseModel, abc.ABC):
    """ABC for pydantic Basemodel.

    Basically this defines an ABC for a strictly subtype-validated field type.
    """

    iri: URIRef = Field(exclude=True, allow_mutation=False)

    _mapping: MutableMapping = mapping.mapping
    _graph = Graph()

    class Config:
        """BaseModel config.

        See: https://docs.pydantic.dev/latest/usage/model_config/

        Settings:
        - also validate field default values (validate_all)
        - also validate on assignment (validate_assignment)
        - disallow arbitrary (extra) kwargs at init (extra)
        - allow arbitray user types for fields (arbitrary_types_allowed)
        """

        validate_all = True
        validate_assignment = True
        extra = "forbid"
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        """Yield a validator for field value validation.

        See: https://docs.pydantic.dev/latest/usage/types/#classes-with-__get_validators__

        If the field value is not a subclass of the field type
        specified in the model, an error is raised.
        """

        def validator(v: Any):
            if isinstance(v, cls):
                return v
            raise ValueError(
                f"Domain must be '{cls.__name__}' or a subclass of it.")

        yield validator

    @overload
    def _convert_to_rdf_term(URIRef) -> URIRef:
        ...

    @overload
    def _convert_to_rdf_term(Any) -> Literal:
        ...

    @staticmethod
    def _convert_to_rdf_term(value: Any | URIRef) -> Literal | URIRef:
        """Convert Any to an RDF triple component.

        Note that rdflib.Literals already handle conversions and datatype assignments.
        """
        if isinstance(value, URIRef):
            return value
        return Literal(value)

    def to_triples(self) -> Generator[_Triple, None, None]:
        """Generate triples from a model.

        Recursively constructs a generator of triples (_Triple type).
        """
        yield (
            URIRef(self.iri),
            RDF.type,
            URIRef(self._mapping[self.__class__.__name__])
        )

        _model_dict = {
            key: value for key, value
            in dict(self).items()
            if value and key != "iri"
        }

        for key, values in _model_dict.items():

            # ensure list for multiple assignment
            if not isinstance(values, list):
                values = [values]

            # get object(s)
            for value in values:
                if isinstance(value, RDFBaseModel):
                    yield from value.to_triples()
                    value = URIRef(value.iri)
                else:
                    value = self._convert_to_rdf_term(value)

                # get predicate
                try:
                    predicate = URIRef(self._mapping[key])
                except KeyError:
                    raise NotInMapping(key)

                # construct triple and yield
                yield (URIRef(self.iri), predicate, value)

    def to_graph(self) -> Graph:
        """Iterate over triple generator and add triples to graph component."""
        for triple in self.to_triples():
            self._graph.add(triple)

        return self._graph

    def serialize(self, *args, **kwargs) -> str:
        """Proxy for rdflib.Graph.serialize."""
        g = self.to_graph()
        return g.serialize(*args, **kwargs)
