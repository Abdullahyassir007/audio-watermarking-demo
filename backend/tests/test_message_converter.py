"""
Unit tests for MessageConverter class
"""

import pytest
from utils.message_converter import MessageConverter


class TestTextToNumeric:
    """Tests for text_to_numeric conversion"""
    
    def test_simple_text(self):
        """Test basic text conversion"""
        result = MessageConverter.text_to_numeric("hello")
        assert len(result) == 5
        assert all(isinstance(x, int) and 0 <= x <= 255 for x in result)
        # "hello" in UTF-8: h=104, e=101, l=108, l=108, o=111
        assert result == [104, 101, 108, 108, 111]
    
    def test_short_text_padding(self):
        """Test that short text is padded with zeros"""
        result = MessageConverter.text_to_numeric("hi")
        assert len(result) == 5
        assert result == [104, 105, 0, 0, 0]  # h=104, i=105, then zeros
    
    def test_long_text_truncation(self):
        """Test that long text is truncated to 5 bytes"""
        result = MessageConverter.text_to_numeric("hello world")
        assert len(result) == 5
        assert result == [104, 101, 108, 108, 111]  # Only "hello"
    
    def test_empty_text(self):
        """Test empty string conversion"""
        result = MessageConverter.text_to_numeric("")
        assert result == [0, 0, 0, 0, 0]
    
    def test_numeric_characters(self):
        """Test text with numbers"""
        result = MessageConverter.text_to_numeric("12345")
        assert len(result) == 5
        # ASCII: 1=49, 2=50, 3=51, 4=52, 5=53
        assert result == [49, 50, 51, 52, 53]


class TestBinaryToNumeric:
    """Tests for binary_to_numeric conversion"""
    
    def test_valid_binary_string(self):
        """Test valid 40-bit binary string"""
        binary = "0000000100000010000000110000010000000101"
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [1, 2, 3, 4, 5]
    
    def test_all_zeros(self):
        """Test binary string of all zeros"""
        binary = "0" * 40
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [0, 0, 0, 0, 0]
    
    def test_all_ones(self):
        """Test binary string of all ones"""
        binary = "1" * 40
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [255, 255, 255, 255, 255]
    
    def test_mixed_values(self):
        """Test binary with mixed values"""
        # 10101010 = 170, 01010101 = 85
        binary = "10101010" * 2 + "01010101" * 3
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [170, 170, 85, 85, 85]
    
    def test_binary_with_spaces(self):
        """Test that spaces are removed"""
        binary = "00000001 00000010 00000011 00000100 00000101"
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [1, 2, 3, 4, 5]
    
    def test_binary_with_underscores(self):
        """Test that underscores are removed"""
        binary = "00000001_00000010_00000011_00000100_00000101"
        result = MessageConverter.binary_to_numeric(binary)
        assert result == [1, 2, 3, 4, 5]
    
    def test_invalid_length_short(self):
        """Test that short binary string raises error"""
        with pytest.raises(ValueError, match="must be exactly 40 bits"):
            MessageConverter.binary_to_numeric("0101010101")
    
    def test_invalid_length_long(self):
        """Test that long binary string raises error"""
        with pytest.raises(ValueError, match="must be exactly 40 bits"):
            MessageConverter.binary_to_numeric("0" * 50)
    
    def test_invalid_characters(self):
        """Test that non-binary characters raise error"""
        with pytest.raises(ValueError, match="must contain only '0' and '1'"):
            MessageConverter.binary_to_numeric("0123456789" * 4)


class TestNumericToText:
    """Tests for numeric_to_text conversion"""
    
    def test_simple_conversion(self):
        """Test basic numeric to text conversion"""
        numeric = [104, 101, 108, 108, 111]  # "hello"
        result = MessageConverter.numeric_to_text(numeric)
        assert result == "hello"
    
    def test_with_trailing_zeros(self):
        """Test that trailing zeros are stripped"""
        numeric = [104, 105, 0, 0, 0]  # "hi" with padding
        result = MessageConverter.numeric_to_text(numeric)
        assert result == "hi"
    
    def test_all_zeros(self):
        """Test all zeros returns empty string"""
        numeric = [0, 0, 0, 0, 0]
        result = MessageConverter.numeric_to_text(numeric)
        assert result == ""
    
    def test_invalid_length(self):
        """Test that wrong length raises error"""
        with pytest.raises(ValueError, match="must have exactly 5 integers"):
            MessageConverter.numeric_to_text([1, 2, 3])
    
    def test_invalid_range_negative(self):
        """Test that negative values raise error"""
        with pytest.raises(ValueError, match="between 0 and 255"):
            MessageConverter.numeric_to_text([1, 2, -1, 4, 5])
    
    def test_invalid_range_too_large(self):
        """Test that values > 255 raise error"""
        with pytest.raises(ValueError, match="between 0 and 255"):
            MessageConverter.numeric_to_text([1, 2, 256, 4, 5])
    
    def test_non_integer_values(self):
        """Test that non-integer values raise error"""
        with pytest.raises(ValueError, match="between 0 and 255"):
            MessageConverter.numeric_to_text([1, 2, 3.5, 4, 5])


class TestNumericToBinary:
    """Tests for numeric_to_binary conversion"""
    
    def test_simple_conversion(self):
        """Test basic numeric to binary conversion"""
        numeric = [1, 2, 3, 4, 5]
        result = MessageConverter.numeric_to_binary(numeric)
        assert result == "0000000100000010000000110000010000000101"
        assert len(result) == 40
    
    def test_all_zeros(self):
        """Test all zeros"""
        numeric = [0, 0, 0, 0, 0]
        result = MessageConverter.numeric_to_binary(numeric)
        assert result == "0" * 40
    
    def test_all_max_values(self):
        """Test maximum values (255)"""
        numeric = [255, 255, 255, 255, 255]
        result = MessageConverter.numeric_to_binary(numeric)
        assert result == "1" * 40
    
    def test_mixed_values(self):
        """Test mixed values"""
        numeric = [170, 85, 170, 85, 170]  # 10101010, 01010101 pattern
        result = MessageConverter.numeric_to_binary(numeric)
        assert result == "10101010" + "01010101" + "10101010" + "01010101" + "10101010"
    
    def test_invalid_length(self):
        """Test that wrong length raises error"""
        with pytest.raises(ValueError, match="must have exactly 5 integers"):
            MessageConverter.numeric_to_binary([1, 2, 3])
    
    def test_invalid_range(self):
        """Test that out of range values raise error"""
        with pytest.raises(ValueError, match="between 0 and 255"):
            MessageConverter.numeric_to_binary([1, 2, 300, 4, 5])


class TestValidateMessage:
    """Tests for validate_message function"""
    
    def test_valid_numeric(self):
        """Test valid numeric message"""
        is_valid, error = MessageConverter.validate_message([1, 2, 3, 4, 5], 'numeric')
        assert is_valid is True
        assert error == ""
    
    def test_invalid_numeric_not_list(self):
        """Test numeric validation with non-list"""
        is_valid, error = MessageConverter.validate_message("12345", 'numeric')
        assert is_valid is False
        assert "must be a list" in error
    
    def test_invalid_numeric_wrong_length(self):
        """Test numeric validation with wrong length"""
        is_valid, error = MessageConverter.validate_message([1, 2, 3], 'numeric')
        assert is_valid is False
        assert "exactly 5 integers" in error
    
    def test_invalid_numeric_out_of_range(self):
        """Test numeric validation with out of range value"""
        is_valid, error = MessageConverter.validate_message([1, 2, 300, 4, 5], 'numeric')
        assert is_valid is False
        assert "between 0 and 255" in error
    
    def test_invalid_numeric_non_integer(self):
        """Test numeric validation with non-integer"""
        is_valid, error = MessageConverter.validate_message([1, 2, "3", 4, 5], 'numeric')
        assert is_valid is False
        assert "must be an integer" in error
    
    def test_valid_text(self):
        """Test valid text message"""
        is_valid, error = MessageConverter.validate_message("hello", 'text')
        assert is_valid is True
        assert error == ""
    
    def test_invalid_text_not_string(self):
        """Test text validation with non-string"""
        is_valid, error = MessageConverter.validate_message([1, 2, 3], 'text')
        assert is_valid is False
        assert "must be a string" in error
    
    def test_invalid_text_empty(self):
        """Test text validation with empty string"""
        is_valid, error = MessageConverter.validate_message("", 'text')
        assert is_valid is False
        assert "cannot be empty" in error
    
    def test_valid_binary(self):
        """Test valid binary message"""
        is_valid, error = MessageConverter.validate_message("0" * 40, 'binary')
        assert is_valid is True
        assert error == ""
    
    def test_valid_binary_with_spaces(self):
        """Test valid binary with spaces"""
        binary = "00000001 00000010 00000011 00000100 00000101"
        is_valid, error = MessageConverter.validate_message(binary, 'binary')
        assert is_valid is True
        assert error == ""
    
    def test_invalid_binary_not_string(self):
        """Test binary validation with non-string"""
        is_valid, error = MessageConverter.validate_message([0, 1, 0, 1], 'binary')
        assert is_valid is False
        assert "must be a string" in error
    
    def test_invalid_binary_wrong_length(self):
        """Test binary validation with wrong length"""
        is_valid, error = MessageConverter.validate_message("0101010101", 'binary')
        assert is_valid is False
        assert "exactly 40 bits" in error
    
    def test_invalid_binary_invalid_characters(self):
        """Test binary validation with invalid characters"""
        is_valid, error = MessageConverter.validate_message("0123456789" * 4, 'binary')
        assert is_valid is False
        assert "must contain only '0' and '1'" in error
    
    def test_invalid_format_type(self):
        """Test validation with invalid format type"""
        is_valid, error = MessageConverter.validate_message("test", 'invalid')
        assert is_valid is False
        assert "Invalid format type" in error


class TestRoundTripConversions:
    """Tests for round-trip conversions"""
    
    def test_numeric_to_binary_to_numeric(self):
        """Test numeric -> binary -> numeric"""
        original = [10, 20, 30, 40, 50]
        binary = MessageConverter.numeric_to_binary(original)
        result = MessageConverter.binary_to_numeric(binary)
        assert result == original
    
    def test_text_to_numeric_to_text(self):
        """Test text -> numeric -> text"""
        original = "hello"
        numeric = MessageConverter.text_to_numeric(original)
        result = MessageConverter.numeric_to_text(numeric)
        assert result == original
    
    def test_binary_to_numeric_to_binary(self):
        """Test binary -> numeric -> binary"""
        original = "1010101001010101101010100101010110101010"
        numeric = MessageConverter.binary_to_numeric(original)
        result = MessageConverter.numeric_to_binary(numeric)
        assert result == original
