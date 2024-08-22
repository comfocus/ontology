import csv
from abc import ABC, abstractmethod

from Entities import HarmonisedQuestionarieComponent, Quality, HarmonisedMeasure, Classification, \
    SingleChoiceQuestion, \
    QuestionType, Ontology, ClassificationInstance, OpenQuestion, MatrixQuestion, MatrixStatement


class CsvParser(ABC):
    def __init__(self, id_columns: list, ontology: Ontology):
        self.id_columns = id_columns
        self.ontology = ontology

    def get_id(self, row: dict):
        ids = []
        for key in self.id_columns:
            ids.append(row[key].strip())
        return '_'.join(ids)

    @abstractmethod
    def read(self, file: str):
        raise NotImplementedError()

    @abstractmethod
    def filter(self, entities: dict):
        raise NotImplementedError()

    def add(self, entities: dict):
        raise NotImplementedError()


class HarmonisedMeasureParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = HarmonisedMeasure(self.ontology.get_counter(), row['Harmonised measure'].strip())
                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: HarmonisedMeasure):
        return entity.label in ['InformedConsent']

    def add(self, entities: dict):
        pass


class HarmonisedQuestionareComponentParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = HarmonisedQuestionarieComponent(
                        id_=self.ontology.get_counter(),
                        label=row['harmonised questionare Component'].strip(),
                        theoretical_background=row['Theoretical background'].strip(),
                        definition=row['Definition'].strip(),
                        harmonised_measure=row['Harmonised measure'].strip(),
                        quality=row['Quality'].strip())

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: HarmonisedQuestionarieComponent):
        return entity.harmonised_measure in ['InformedConsent']

    def add(self, entities: dict):
        pass


class QualityParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = Quality(id_=self.ontology.get_counter(),
                                     label=row['Quality'].strip().lower(),
                                     harmonised_measure=row['Harmonised measure'].strip())

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: Quality):
        return entity.harmonised_measure in ['InformedConsent']

    def add(self, entities: dict):
        pass


class ClassificationParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = Classification(
                        id_=self.ontology.get_counter(),
                        label=row['Classification'].strip().lower(),
                        definition=row['Definiton within a specific classification'].strip())

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

                        entity.add_individual(ClassificationInstance(
                            id_=self.ontology.get_counter(),
                            label=row['Instances: '].strip().lower(),
                            parent_iri=entity.iri))
                        self.ontology.update_counter()

                else:
                    entity = entities[self.get_id(row)]
                    entity.add_individual(ClassificationInstance(
                        self.ontology.get_counter(),
                        row['Instances: '].strip().lower(),
                        entity.iri))
                    self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: Classification):
        return entity.label in []

    def add(self, entities: dict):
        pass


class SingleChoiceQuestionParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = SingleChoiceQuestion(
                        self.ontology.get_counter(),
                        row['Annotation: Label'].strip().lower(),
                        QuestionType.get_id(row['Question']),
                        row['Annotation: hadQuestion'].strip(),
                        row['Linked classification ID'],
                        row['ComponentId'])

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: SingleChoiceQuestion):
        return (entity.question_type not in [QuestionType.SINGLE_CHOICE] or
                entity.harmonised_component in ['209'])

    def add(self, entities: dict):
        pass


class OpenQuestionParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = OpenQuestion(
                        self.ontology.get_counter(),
                        row['Annotation: Label'].strip().lower(),
                        QuestionType.get_id(row['Question']),
                        row['Annotation: hadQuestion'].strip(),
                        'open',
                        row['ComponentId'])

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: OpenQuestion):
        return (entity.question_type not in [QuestionType.OPEN] or
                entity.harmonised_component in ['209'])

    def add(self, entities: dict):
        pass


class MatrixQuestionParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    entity = MatrixQuestion(
                        self.ontology.get_counter(),
                        row['Annotation: Label'].strip().lower(),
                        QuestionType.get_id(row['Question']),
                        row['Annotation: hadQuestion'].strip(),
                        row['Linked classification ID'],
                        row['ComponentId'])

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: MatrixQuestion):
        return (entity.question_type not in [QuestionType.MATRIX] or
                entity.harmonised_component in ['209'])

    def add(self, entities: dict):
        pass


class MatrixStatementParser(CsvParser):
    def read(self, file: str):
        entities = dict()
        counters = dict()
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.get_id(row) not in entities.keys():
                    counter = 1
                    question_name = row['Question name']  # .strip().lower()

                    if question_name in counters.keys():
                        counter = counters[question_name] + 1
                    counters[question_name] = counter

                    entity = MatrixStatement(
                        id_=self.ontology.get_counter(),
                        label=question_name.strip().lower() + '_' + str(counter),
                        description=row['Item name'].strip(),
                        matrix_question=question_name,
                        harmonised_component=row['ComponentId'])

                    if not self.filter(entity):
                        entities[self.get_id(row)] = entity
                        self.ontology.update_counter()

        self.add(entities)

        return entities

    def filter(self, entity: MatrixStatement):
        return entity.harmonised_component in ['209']

    def add(self, entities: dict):
        pass
