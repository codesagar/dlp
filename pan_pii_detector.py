from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from presidio_analyzer import AnalyzerEngine
from typing import List, Tuple, Dict


def detect(text: str, entities: List[str]) -> Tuple[str, Dict[str, Dict[str, float]]]:
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text, entities=entities, language='en')
    mapping = {}

    for result in results:
        result_dict = result.to_dict()
        entity_type = result_dict['entity_type']
        entity_text = text[result.start:result.end]
        entity_score = result.score

        if entity_type not in mapping:
            mapping[entity_type] = {}

        mapping[entity_type][entity_text] = {"start":result.start, "end":result.end, "confidence":result.score}

    return text, mapping


def mask(text: str, entities: List[str]) -> Tuple[str, Dict[str, str]]:
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text, entities=entities, language='en')
    mapping = {}
    result_text = text
    for result in results:
        original_text = text[result.start:result.end]
        masked_text = original_text[0:2] + "X" * (len(original_text) - 4) + original_text[-2:]
        result_text = result_text[:result.start] + masked_text + result_text[result.end:]
        entity_type = result.to_dict()['entity_type']
        result_dict = result.to_dict()
        if entity_type not in mapping:
            mapping[entity_type] = {}
        mapping[entity_type][masked_text] = original_text            
    return result_text, mapping


def anonymize(text: str, entities: List[str]) -> Tuple[str, Dict[str, str]]:
    anonymizer = PresidioReversibleAnonymizer(analyzed_fields = entities, faker_seed=123)
    anonymized_results = anonymizer.anonymize(text)
    mapping = anonymizer.deanonymizer_mapping
    return anonymized_results, mapping