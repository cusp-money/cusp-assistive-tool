"""Provides fi data analyzer based on fi type."""

from utils.fi_data_analysis.fi_data_analyzers import (
    analyse_deposits,
    analyse_equities,
    analyse_general_insurance,
    analyse_life_insurance_policy,
    analyse_mutual_funds,
    analyse_recurrent_deposits,
    analyse_term_deposits,
    base_analyzer,
)


def get_fi_analysis_handler(fi_type: str) -> base_analyzer.FiDataAnalyzerBase:
    """Gets the function to summarize data of given fi type."""
    match fi_type:
        case "TERM_DEPOSIT":
            return analyse_term_deposits.TermDepositsAnalyzer
        case "RECURRING_DEPOSIT":
            return analyse_recurrent_deposits.RecurrentDepositsAnalyzer
        case "DEPOSIT":
            return analyse_deposits.DepositsAnalyzer
        case "EQUITIES":
            return analyse_equities.EquitiesAnalyzer
        case "MUTUAL_FUNDS":
            return analyse_mutual_funds.MutualFundsAnalyzer
        case "INSURANCE_POLICIES":
            return analyse_life_insurance_policy.LifeInsuranceAnalyzer
        case "GENERAL_INSURANCE":
            return analyse_general_insurance.GeneralInsuranceAnalyzer

    return None
