from Entities import Ontology
from CsvParser import HarmonisedMeasureParser, HarmonisedQuestionareComponentParser, \
    QualityParser, ClassificationParser, SingleChoiceQuestionParser, OpenQuestionParser, MatrixQuestionParser, \
    MatrixStatementParser
from XmlWriter import HarmonisedMeasureXmlWriter, QualityXmlWriter, \
    HarmonisedQuestionarieComponentXmlWriter, QuestionXmlWriter, ClassificationXmlWriter, MatrixStatementXmlWriter

HARMONISED_COMPONENT_METADATA_FILE = r'path\to\csv\file'
HARMONISED_COMPONENT_FILE = r'path\to\csv\file'
CLASSIFICATION_FILE = r'path\to\csv\file'
ITEMS_FILE = r'path\to\csv\file'

OUTPUT_FILE = r'path\to\xml\file\'

if __name__ == '__main__':
    base = Ontology()
    [ontology, tree] = base.get_ontology()

    parser = HarmonisedMeasureParser(id_columns=['Harmonised measure'], ontology=base)
    writer = HarmonisedMeasureXmlWriter(ontology, tree)
    measures = parser.read(HARMONISED_COMPONENT_METADATA_FILE)
    writer.write(measures, dict())

    parser = QualityParser(id_columns=['Quality'], ontology=base)
    writer = QualityXmlWriter(ontology, tree)
    qualities = parser.read(HARMONISED_COMPONENT_METADATA_FILE)
    writer.write(qualities, dict())

    parser = HarmonisedQuestionareComponentParser(id_columns=['ID'], ontology=base)
    writer = HarmonisedQuestionarieComponentXmlWriter(ontology, tree)
    components = parser.read(HARMONISED_COMPONENT_METADATA_FILE)
    writer.write(components, {
        'measures': measures,
        'qualities': qualities})

    parser = ClassificationParser(id_columns=['ID'], ontology=base)
    writer = ClassificationXmlWriter(ontology, tree)
    classifications = parser.read(CLASSIFICATION_FILE)
    writer.write(classifications, {
        'qualities': qualities,
        'components': components})

    parser = SingleChoiceQuestionParser(
        id_columns=['Annotation: Label', 'Annotation: hadQuestion', 'Linked classification ID'],
        ontology=base)
    writer = QuestionXmlWriter(ontology, tree)
    questions = parser.read(HARMONISED_COMPONENT_FILE)
    writer.write(questions, {
        'components': components,
        'classifications': classifications})

    parser = OpenQuestionParser(
        id_columns=['Annotation: Label', 'Annotation: hadQuestion', 'Linked classification ID'],
        ontology=base)
    writer = QuestionXmlWriter(ontology, tree)
    questions = parser.read(HARMONISED_COMPONENT_FILE)
    writer.write(questions, {
        'components': components,
        'classifications': classifications})

    parser = MatrixQuestionParser(
        id_columns=['Annotation: Label'],
        ontology=base)
    writer = QuestionXmlWriter(ontology, tree)
    questions = parser.read(HARMONISED_COMPONENT_FILE)
    writer.write(questions, {
        'components': components,
        'classifications': classifications})

    parser = MatrixStatementParser(
        id_columns=['Question name', 'Item name', 'Item label'],
        ontology=base)
    writer = MatrixStatementXmlWriter(ontology, tree)
    statements = parser.read(ITEMS_FILE)
    writer.write(statements, {
        'questions': questions})

    base.write(OUTPUT_FILE)
