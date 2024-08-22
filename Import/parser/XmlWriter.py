import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class XmlWriter(ABC):
    def __init__(self, ontology, tree):
        self.ontology = ontology
        self.tree = tree

    @staticmethod
    def add_declaration(parent_node: ET.Element, iri: str, class_: bool) -> ET.Element:
        declaration = ET.SubElement(parent_node, 'Declaration')
        if class_:
            ET.SubElement(declaration, 'Class', {'IRI': iri})
        else:
            ET.SubElement(declaration, 'NamedIndividual', {'IRI': iri})
        return declaration

    @staticmethod
    def add_subclass(parent_node: ET.Element, parent_iri: str, child_iri: str) -> ET.Element:
        subclass = ET.SubElement(parent_node, 'SubClassOf')
        ET.SubElement(subclass, 'Class', {'IRI': child_iri})
        ET.SubElement(subclass, 'Class', {'IRI': parent_iri})
        return subclass

    @staticmethod
    def add_disjoint_classes(parent_node: ET.Element, iri_list: list) -> ET.Element:
        subclass = ET.SubElement(parent_node, 'DisjointClasses')
        for iri in iri_list:
            ET.SubElement(subclass, 'Class', {'IRI': iri})
        return subclass

    @staticmethod
    def add_subclass_some_values(parent_node: ET.Element, parent_iri: str, object_property_iri: str, child_iri: str,
                                 some: bool = True):
        subclass = ET.SubElement(parent_node, 'SubClassOf')
        ET.SubElement(subclass, 'Class', {'IRI': child_iri})
        object_ = ET.SubElement(subclass, 'ObjectSomeValuesFrom' if some else 'ObjectAllValuesFrom')
        ET.SubElement(object_, 'ObjectProperty', {'IRI': object_property_iri})
        ET.SubElement(object_, 'Class', {'IRI': parent_iri})
        return subclass

    @staticmethod
    def add_subclass_exact_cardinality(parent_node: ET.Element,
                                       parent_iri: str, object_property_iri: str, child_iri: str,
                                       property_attributes: dict):
        subclass = ET.SubElement(parent_node, 'SubClassOf')
        ET.SubElement(subclass, 'Class', {'IRI': child_iri})
        object_ = ET.SubElement(subclass, 'ObjectExactCardinality', property_attributes)
        ET.SubElement(object_, 'ObjectProperty', {'IRI': object_property_iri})
        ET.SubElement(object_, 'Class', {'IRI': parent_iri})
        return subclass

    @staticmethod
    def add_literal_property(parent_node: ET.Element, iri: str,
                             property_attributes: dict,
                             property_type: dict, property_value: str):
        annotation_assertion = ET.SubElement(parent_node, 'AnnotationAssertion')
        ET.SubElement(annotation_assertion, 'AnnotationProperty',
                      property_attributes)
        iri_element = ET.SubElement(annotation_assertion, 'IRI')
        iri_element.text = iri
        if property_type.items() is None:
            literal = ET.SubElement(annotation_assertion, 'Literal')
        else:
            literal = ET.SubElement(annotation_assertion, 'Literal', property_type)
        literal.text = property_value
        return annotation_assertion

    @staticmethod
    def add_object_property(parent_node: ET.Element, iri: str,
                            property_attributes: dict,
                            property_value: str):
        annotation_assertion = ET.SubElement(parent_node, 'AnnotationAssertion')
        ET.SubElement(annotation_assertion, 'AnnotationProperty',
                      property_attributes)
        iri_element = ET.SubElement(annotation_assertion, 'IRI')
        iri_element.text = iri
        iri_element = ET.SubElement(annotation_assertion, 'IRI')
        iri_element.text = property_value
        return annotation_assertion

    @staticmethod
    def add_instance(parent_node: ET.Element, parent_iri: str,
                     named_individual_iri: str):
        subclass = ET.SubElement(parent_node, 'ClassAssertion')
        ET.SubElement(subclass, 'Class', {'IRI': parent_iri})
        ET.SubElement(subclass, 'NamedIndividual', {'IRI': named_individual_iri})

    @abstractmethod
    def write(self, entities: dict, linked_entities: dict):
        raise NotImplementedError()


class HarmonisedMeasureXmlWriter(XmlWriter):
    def write(self, entities, linked_entities):
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue

            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology, iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_subclass(parent_node=self.ontology,
                              parent_iri=entity.parent_iri,
                              child_iri=entity.iri)

            self.add_subclass_some_values(
                parent_node=self.ontology,
                parent_iri=entity.iri,
                object_property_iri=entity.base_iri + "00000000000000000333",
                child_iri=entity.base_iri + "00000000000000000549",  # harmonised questionarie component class
                some=False)

            ET.indent(self.ontology, '    ')
            ET.indent(declaration, '    ')


class QualityXmlWriter(XmlWriter):
    def write(self, entities, linked_entities):
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue

            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology, iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_subclass(parent_node=self.ontology,
                              parent_iri=entity.parent_iri,
                              child_iri=entity.iri)

            ET.indent(self.ontology, '    ')
            ET.indent(declaration, '    ')


class HarmonisedQuestionarieComponentXmlWriter(XmlWriter):

    def write(self, entities, linked_entities):
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue
                
            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology, iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'IRI': "#theoretical_background"},
                property_type={'xml:lang': "en"},
                property_value=entity.theoretical_background)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "obo:IAO_0000115"},
                property_type=dict(),
                property_value=entity.definition)

            self.add_subclass(
                parent_node=self.ontology,
                parent_iri=entity.parent_iri,
                child_iri=entity.iri)

            self.add_subclass_some_values(
                parent_node=self.ontology,
                parent_iri=linked_entities['measures'][entity.harmonised_measure].iri,
                object_property_iri=entity.base_iri + "00000000000000000350",
                child_iri=entity.iri,
                some=True)

            # link between qualities and harmonised questionarie components
            self.add_subclass_some_values(
                parent_node=self.ontology,
                parent_iri=entity.iri,
                object_property_iri="#OWLObjectProperty_aebfc327_8e90_47ec_afa4_23b12c522631",
                child_iri=linked_entities['qualities'][entity.quality].iri,
                some=True)

            ET.indent(self.ontology, '    ')
            ET.indent(declaration, '    ')


class QuestionXmlWriter(XmlWriter):

    def write(self, entities, linked_entities):
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue

            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology, iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'IRI': "#hasQuestion"},
                property_type={'xml:lang': "en"},
                property_value=entity.has_question)

            self.add_subclass(
                parent_node=self.ontology,
                parent_iri=entity.parent_iri,
                child_iri=entity.iri)

            self.add_subclass_some_values(
                parent_node=self.ontology,
                parent_iri=linked_entities['components'][entity.harmonised_component].iri,
                object_property_iri=entity.base_iri + "00000000000000000350",
                child_iri=entity.iri,
                some=True)

            # object properties is the answer of and is answered by
            self.add_subclass_exact_cardinality(
                parent_node=self.ontology,
                parent_iri=linked_entities['classifications'][entity.linked_classification].iri,
                object_property_iri=entity.base_iri + "00000000000000000362",
                child_iri=entity.iri,
                property_attributes={"cardinality": "1"})

            self.add_subclass_exact_cardinality(
                parent_node=self.ontology,
                parent_iri=entity.iri,
                object_property_iri=entity.base_iri + "00000000000000000543",
                child_iri=linked_entities['classifications'][entity.linked_classification].iri,
                property_attributes={"cardinality": "1"})

            ET.indent(self.ontology, '    ')
            ET.indent(declaration, '    ')


class MatrixStatementXmlWriter(XmlWriter):

    def write(self, entities, linked_entities):
        question_statements = dict()
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue

            if entity.matrix_question in question_statements.keys():
                values = question_statements[entity.matrix_question]
                values.append(entity.iri)
                question_statements[entity.matrix_question] = values
            else:
                values = [entity.iri]
                question_statements[entity.matrix_question] = values

            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:description"},
                property_type=dict(),
                property_value=entity.description)

            self.add_subclass(
                parent_node=self.ontology,
                parent_iri=linked_entities['questions'][entity.matrix_question].iri,
                child_iri=entity.iri)

            ET.indent(declaration, '    ')

        for question in question_statements:
            self.add_disjoint_classes(
                parent_node=self.ontology,
                iri_list=question_statements[question]
            )
        ET.indent(self.ontology, '    ')


class ClassificationXmlWriter(XmlWriter):

    def write(self, entities, linked_entities):
        for key in entities:
            entity = entities[key]
            if entity.added:
                continue

            declaration = self.add_declaration(self.ontology, entity.iri, class_=True)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "rdfs:label"},
                property_type={'xml:lang': "en"},
                property_value=entity.label)

            self.add_object_property(
                parent_node=self.ontology, iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:creator"},
                property_value=entity.creator)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "dc:date"},
                property_type={'datatypeIRI': "http://www.w3.org/2001/XMLSchema#dateTime"},
                property_value=entity.date)

            self.add_literal_property(
                parent_node=self.ontology,
                iri=entity.iri,
                property_attributes={'abbreviatedIRI': "obo:IAO_0000115"},
                property_type=dict(),
                property_value=entity.definition)

            self.add_subclass(
                parent_node=self.ontology,
                parent_iri=entity.parent_iri,
                child_iri=entity.iri)

            for individual in entity.individuals:
                self.add_declaration(self.ontology, individual.iri, class_=False)
                self.add_literal_property(
                    parent_node=self.ontology,
                    iri=individual.iri,
                    property_attributes={'abbreviatedIRI': "rdfs:label"},
                    property_type={'xml:lang': "en"},
                    property_value=individual.label)
                self.add_instance(self.ontology, individual.parent_iri, individual.iri)

            ET.indent(self.ontology, '    ')
            ET.indent(declaration, '    ')
