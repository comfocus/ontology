import datetime
import xml.etree.ElementTree as ET
from abc import ABC
from enum import Enum


class Ontology:
    NAMESPACES = {'xmlns': "http://www.w3.org/2002/07/owl#",
                  'xml:base': "http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_Contextv4",
                  'xmlns:rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                  'xmlns:xml': "http://www.w3.org/XML/1998/namespace",
                  'xmlns:xsd': "http://www.w3.org/2001/XMLSchema#",
                  'xmlns:rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                  'ontologyIRI': "http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_Contextv4",
                  'versionIRI': "http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_v1/1.0.1"}

    PREFIXES = {
        "base": "http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_Contextv4#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "obo": "http://purl.obolibrary.org/obo/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xml": "http://www.w3.org/XML/1998/namespace",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "terms": "http://purl.org/dc/terms/",
        "schema": "https://schema.org/",
        "OntoV24": "http://www.semanticweb.org/clarisse/ontologies/2023/5/OntoV24#",
        "oboInOwl": "http://www.geneontology.org/formats/oboInOwl#",
        "Comfocus_Contextv4": "http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_Contextv4#"
    }

    ontology = None
    tree = None
    counter = 701

    def get_ontology(self):
        if self.ontology is None:
            self.ontology = ET.Element('Ontology', self.NAMESPACES)
            self.tree = ET.ElementTree(self.ontology)

            for key in self.PREFIXES.keys():
                if key == 'base':
                    ET.SubElement(self.ontology, 'Prefix', {'name': "", 'IRI': self.PREFIXES['base']})
                else:
                    ET.SubElement(self.ontology, 'Prefix', {'name': key, 'IRI': self.PREFIXES[key]})

        return [self.ontology, self.tree]

    def get_counter(self):
        return self.counter

    def update_counter(self):
        self.counter += 1

    def write(self, file: str):
        self.tree.write(file)


class Entity(ABC):
    base_iri = r'http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_v1/COMFOCUS_'
    context_iri = r'http://www.semanticweb.org/bkorousicseljak/ontologies/2023/5/Comfocus_Contextv4#COMFOCUS_'
    creator = r'http://orcid.org/0000-0001-7597-2590'

    def __init__(self, parent_iri: str, id_: int, label: str, added: bool):
        self.iri = self.base_iri + f'{id_:020d}'
        self.parent_iri = parent_iri
        self.label = label
        self.date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.added = added


class Instance(ABC):
    base_iri = r'#OWLNamedIndividual_'
    creator = r'http://orcid.org/0000-0001-7597-2590'

    def __init__(self, parent_iri: str, id_: int, label: str):
        self.iri = self.base_iri + str(id_)
        self.parent_iri = parent_iri
        self.label = label  # .lower()
        self.date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


class HarmonisedMeasure(Entity):

    def __init__(self, id_: int, label: str, added: bool = False):
        super().__init__(parent_iri=r'#OWLClass_832ab481_6bdd_49e2_86dd_6042773f6aef', id_=id_, label=label, added=added)


class Quality(Entity):
    def __init__(self, id_: int, label: str,
                 harmonised_measure: str, added: bool = False):
        super().__init__(parent_iri=self.base_iri + '00000000000000000610', id_=id_, label=label, added=added)
        self.harmonised_measure = harmonised_measure


class HarmonisedQuestionarieComponent(Entity):
    def __init__(self, id_: int, label: str,
                 theoretical_background: str, definition: str,
                 harmonised_measure: str, quality: str, added: bool = False):
        super().__init__(parent_iri=self.base_iri + '00000000000000000549', id_=id_, label=label, added=added)
        self.theoretical_background = theoretical_background
        self.definition = definition
        self.harmonised_measure = harmonised_measure
        self.quality = quality


class ClassificationInstance(Instance):
    def __init__(self, id_: int, label: str,
                 parent_iri: str):
        super().__init__(parent_iri=parent_iri, id_=id_, label=label)


class Classification(Entity):
    def __init__(self, id_: int, label: str,
                 definition: str, added: bool = False):
        super().__init__(parent_iri=self.context_iri + '00000000000000000002', id_=id_, label=label, added=added)
        self.definition = definition
        self.individuals = []

    def add_individual(self, individual: ClassificationInstance):
        self.individuals.append(individual)


class QuestionType(Enum):
    BIPOLAR: str = 'Bipolar',
    MATRIX: str = 'Matrix',
    MULTIPLE_CHOICE: str = 'Multiple choice',
    OPEN: str = 'Open',
    SINGLE_CHOICE: str = 'Single choice'

    @staticmethod
    def get_id(value: str):
        if value == 'Bipolar':
            return QuestionType.BIPOLAR
        elif value == 'Matrix':
            return QuestionType.MATRIX
        elif value == 'Multiple choice':
            return QuestionType.MULTIPLE_CHOICE
        elif value == 'Open':
            return QuestionType.OPEN
        elif value == 'Single choice':
            return QuestionType.SINGLE_CHOICE


class SingleChoiceQuestion(Entity):
    def __init__(self, id_: int, label: str, question_type: QuestionType,
                 has_question: str, linked_classification: str,
                 harmonised_component: str, added: bool = False):
        super().__init__(parent_iri=self.base_iri + '00000000000000000388', id_=id_, label=label, added=added)
        self.question_type = question_type
        self.has_question = has_question
        self.linked_classification = linked_classification
        self.harmonised_component = harmonised_component


class OpenQuestion(Entity):
    def __init__(self, id_: int, label: str, question_type: QuestionType,
                 has_question: str, linked_classification: str,
                 harmonised_component: str, added: bool = False):
        super().__init__(parent_iri=self.base_iri + '00000000000000000358', id_=id_, label=label, added=added)
        self.question_type = question_type
        self.has_question = has_question
        self.linked_classification = linked_classification
        self.harmonised_component = harmonised_component


class MatrixQuestion(Entity):
    def __init__(self, id_: int, label: str, question_type: QuestionType,
                 has_question: str, linked_classification: str,
                 harmonised_component: str, added: bool = False):
        super().__init__(parent_iri=self.base_iri + '00000000000000000533', id_=id_, label=label, added=added)
        self.question_type = question_type
        self.has_question = has_question
        self.linked_classification = linked_classification
        self.harmonised_component = harmonised_component


class MatrixStatement(Entity):
    def __init__(self, id_: int, label: str, description: str,
                 matrix_question: str, harmonised_component: str, added: bool = False):
        super().__init__(parent_iri='', id_=id_, label=label, added=added)
        self.description = description
        self.matrix_question = matrix_question
        self.harmonised_component = harmonised_component
