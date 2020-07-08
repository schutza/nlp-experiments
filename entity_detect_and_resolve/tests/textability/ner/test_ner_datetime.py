import pytest

from textability.ner.ner_datetime import detect_and_resolve


class TestDetectAndResolveDatetime:

    datetime_testdata = [
        ('on december 24th 1943', 'december 24th 1943', '1943-12-24T'),
        ('tomorrow', 'tomorrow', '2020-07-09T'),
        ('just like yesterday', 'yesterday', '2020-07-07T'),
    ]

    @pytest.mark.parametrize("input_text,expected_surface_string,expected_resolved_prefix", datetime_testdata)
    def test_detect_and_resolve(self, input_text, expected_surface_string, expected_resolved_prefix):
        actual_result = detect_and_resolve(input_text)
        actual_surface_text = actual_result[0][0]
        actual_resolved_date = actual_result[0][1]

        assert actual_surface_text == expected_surface_string
        assert actual_resolved_date.startswith(expected_resolved_prefix)
