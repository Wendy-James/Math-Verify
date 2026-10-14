"""Regression tests for Markdown-bold final answers (huggingface/Math-Verify#76)."""

import pytest

from math_verify import ExprExtractionConfig, parse, verify


@pytest.mark.parametrize(
    "prediction,expected_value",
    [
        ("Final Answer: **73**", "73"),
        ("✅ Final Answer: **73**", "73"),
        ("The answer is **73**.", "73"),
        ("Answer: **-5**", "-5"),
    ],
)
def test_markdown_bold_number_does_not_capture_closing_asterisks(
    prediction, expected_value
):
    config = [ExprExtractionConfig()]
    extracted = parse(prediction, extraction_config=config)

    assert verify(parse(expected_value, extraction_config=config), extracted)
    assert extracted[-1] == expected_value


@pytest.mark.parametrize(
    "prediction,expected_value,raw_expression",
    [
        ("Final Answer: **2 + 3**", "5", "2 + 3"),
        ("Final Answer: **2 * 3**.", "6", "2 * 3"),
        ("Final Answer: **1/2**", "1/2", "1/2"),
        ("Final Answer: 2**3", "8", "2**3"),
    ],
)
def test_markdown_bold_math_preserves_legitimate_operators(
    prediction, expected_value, raw_expression
):
    config = [ExprExtractionConfig()]
    extracted = parse(prediction, extraction_config=config)

    assert verify(parse(expected_value, extraction_config=config), extracted)
    assert extracted[-1] == raw_expression


def test_issue_76_long_solution_selects_bold_final_answer():
    prediction = """
    ... - 73 = 489 ...(iii)
    Now sum (i)+(ii)+(iii):
    Left: (x_D + x_G + x_S) + 2(y_DG + y_DS + y_GS) = 437 + 2*234 = 437 + 468 = 905
    Right: 122 + 294 + 489 = 905
    ✅ Consistent!
    So answer is consistent.
    Thus, the number of residents who own all four of the things is **73**.
    ---
    ✅ Final Answer: **73**
    """
    extracted = parse(prediction)

    assert verify(parse("73"), extracted)
    assert extracted[-1] == "73"
