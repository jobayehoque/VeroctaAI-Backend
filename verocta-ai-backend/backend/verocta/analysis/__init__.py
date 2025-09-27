"""Analysis and engines shims.

Unify access to analysis engines, parsers, generators.
"""

try:
    from spend_score_advanced import calculate_advanced_spend_score, spend_score_engine  # noqa: F401
except Exception:
    calculate_advanced_spend_score = None  # type: ignore
    spend_score_engine = None  # type: ignore

try:
    from spend_score_engine import (
        calculate_spend_score,
        get_score_label,
        get_score_color,
        get_enhanced_analysis,
    )  # noqa: F401
except Exception:
    calculate_spend_score = None  # type: ignore
    get_score_label = None  # type: ignore
    get_score_color = None  # type: ignore
    get_enhanced_analysis = None  # type: ignore

try:
    from csv_parser import parse_csv_file, parse_csv_file_with_mapping  # noqa: F401
except Exception:
    parse_csv_file = None  # type: ignore
    parse_csv_file_with_mapping = None  # type: ignore

try:
    from pdf_generator import generate_report_pdf  # noqa: F401
except Exception:
    generate_report_pdf = None  # type: ignore

__all__ = [
    "calculate_advanced_spend_score",
    "spend_score_engine",
    "calculate_spend_score",
    "get_score_label",
    "get_score_color",
    "get_enhanced_analysis",
    "parse_csv_file",
    "parse_csv_file_with_mapping",
    "generate_report_pdf",
]



