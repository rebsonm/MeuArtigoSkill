"""Exploratory lexical risk signals: warnings, not entailment or approvals."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from claim_overreach_signals import signals

class PossibleOverreachSignalTests(unittest.TestCase):
    def assert_flag(self,claim,passage,code):
        actual=signals(claim,passage)
        self.assertIn(code,actual["codes"])
        self.assertFalse(actual["semantic_entailment_proven"])
        self.assertFalse(actual["is_scientific_verification"])
        self.assertTrue(actual["potential_review_needed"])
        self.assertEqual(actual["codes"],signals(claim,passage)["codes"])

    def test_causal_jump_is_only_an_advisory_risk(self):
        self.assert_flag(
            "The checklist caused a reduction in missing data.",
            "The observational comparison was not randomized and groups differed in case complexity.",
            "CAUSALITY_FROM_NONCAUSAL_EVIDENCE")

    def test_significance_inversion(self):
        self.assert_flag("Treatment significantly improved outcomes.",
                         "The evaluation found no statistically significant differences.",
                         "SIGNIFICANCE_POLARITY_CONFLICT")

    def test_direction_inversion(self):
        self.assert_flag("The median time decreased from 14 to 11 days.",
                         "The report says the median time rose from 11 to 14 days.",
                         "DIRECTION_OF_CHANGE_CONFLICT")

    def test_scope_universalization(self):
        self.assert_flag("All public organizations improved performance.",
                         "Only two organizations in one region were studied.",
                         "POPULATION_EXTRAPOLATION")

    def test_no_outcome_observations(self):
        self.assert_flag("The new system reduced missing fields.",
                         "The data collection had not started and no results were reported.",
                         "OUTCOME_WITHOUT_COLLECTED_RESULTS")

    def test_method_and_population_contradictions(self):
        self.assert_flag("The study used an AI system to classify decisions.",
                         "The method used manual coding without deploying any language model.",
                         "METHOD_CONTRADICTS_SOURCE")
        self.assert_flag("The sample included private companies.",
                         "The protocol excluded private companies.",
                         "EXCLUDED_POPULATION_ASSERTED_PRESENT")

    def test_ambiguous_date_stays_advisory(self):
        self.assert_flag("The decision was formally approved on 10 April 2024.",
                         "The two versions have different dates; the discrepancy remains unresolved.",
                         "CONFLICTING_DATE_REPORTED_AS_FINAL")

    def test_missing_group_and_nonrespondent_data(self):
        self.assert_flag("Unit C reduced its backlog by 20 percent.",
                         "Records for Unit C were missing. No outcomes were available.",
                         "MISSING_SUBGROUP_OUTCOME")
        self.assert_flag("Nonrespondents had higher compliance.",
                         "No compliance observations were collected for nonrespondents.",
                         "UNOBSERVED_GROUP_COMPARISON")

    def test_bounded_supported_claim_is_not_pretended_verified(self):
        result=signals(
            "In the hypothetical sample, 18 of 30 records included complete dates.",
            "Among 30 sampled records, 18 included complete dates and 12 had missing dates.")
        self.assertEqual(result["status"],"SCREENED_HEURISTIC_ONLY")
        self.assertEqual(result["codes"],[])
        self.assertFalse(result["semantic_entailment_proven"])
        self.assertFalse(result["potential_review_needed"])

    def test_portuguese_bounded_case_needs_no_automatic_approval(self):
        result=signals("Em duas unidades, 18 dos 30 registros estavam completos.",
                       "Somente duas unidades foram examinadas, e 18 de 30 registros continham as datas.")
        self.assertEqual(result["codes"],[])
        self.assertFalse(result["semantic_entailment_proven"])

    def test_large_or_missing_input_is_explicitly_not_evaluated(self):
        for claim,source in (("", "a source"),("some claim",""),("x"*13000,"an excerpt")):
            result=signals(claim,source)
            self.assertEqual(result["status"],"NOT_EVALUATED")
            self.assertEqual(result["codes"],[])
            self.assertFalse(result["semantic_entailment_proven"])

    def test_no_excerpt_in_output_and_stable_codes(self):
        claim="The method caused a reduction in cost because of the checklist."
        passage="This observational study was not randomized and did not estimate causes."
        result=signals(claim,passage)
        self.assertNotIn(claim,repr(result))
        self.assertNotIn(passage,repr(result))
        self.assertTrue(all(x.isupper() and x.replace("_","").isalpha() for x in result["codes"]))

if __name__=="__main__":
    unittest.main()
