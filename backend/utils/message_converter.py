"""
Message Converter Utility

Converts between different message formats for audio watermarking:
- Numeric: 5 integers (0-255)
- Text: String representation
- Binary: 40-bit binary string
"""

from typing import List, Union, Tuple


class MessageConverter:
    """Handles conversion between message formats for audio watermarking."""
    
    @staticmethod
    def text_to_numeric(text: str) -> List[int]:
        """
        Convert text string to 5-integer array (0-255).
        
        Uses UTF-8 encoding and packs bytes into 5 integers.
        If text is shorter, pads with zeros. If longer, truncates.
        
        Args:
            text: Input text string
            
        Returns:
            List of 5 integers (0-255)
        """
        # Encode text to bytes (UTF-8)
        text_bytes = text.encode('utf-8')
        
        # Pad or truncate to 5 bytes
        if len(text_bytes) < 5:
            text_bytes = text_bytes + b'\x00' * (5 - len(text_bytes))
        else:
            text_bytes = text_bytes[:5]
        
        # Convert bytes to list of integers
        return list(text_bytes)
    
    @staticmethod
    def binary_to_numeric(binary_str: str) -> List[int]:
        """
        Convert 40-bit binary string to 5-integer array (0-255).
        
        Each 8 bits represents one integer.
        
        Args:
            binary_str: 40-bit binary string (e.g., "0101010101010101...")
            
        Returns:
            List of 5 integers (0-255)
            
        Raises:
            ValueError: If binary string is not 40 bits or contains invalid characters
        """
        # Remove any whitespace
        binary_str = binary_str.replace(' ', '').replace('_', '')
        
        # Validate length
        if len(binary_str) != 40:
            raise ValueError(f"Binary string must be exactly 40 bits, got {len(binary_str)}")
        
        # Validate characters
        if not all(c in '01' for c in binary_str):
            raise ValueError("Binary string must contain only '0' and '1' characters")
        
        # Convert each 8-bit chunk to integer
        result = []
        for i in range(0, 40, 8):
            byte_str = binary_str[i:i+8]
            result.append(int(byte_str, 2))
        
        return result
    
    @staticmethod
    def numeric_to_text(numeric_array: List[int]) -> str:
        """
        Convert 5-integer array to text string.
        
        Args:
            numeric_array: List of 5 integers (0-255)
            
        Returns:
            Decoded text string (strips null bytes)
            
        Raises:
            ValueError: If array is not valid
        """
        # Validate input
        if len(numeric_array) != 5:
            raise ValueError(f"Numeric array must have exactly 5 integers, got {len(numeric_array)}")
        
        if not all(isinstance(x, int) and 0 <= x <= 255 for x in numeric_array):
            raise ValueError("All values must be integers between 0 and 255")
        
        # Convert to bytes
        byte_array = bytes(numeric_array)
        
        # Decode to text, removing null bytes
        try:
            text = byte_array.decode('utf-8', errors='ignore')
            # Strip null bytes and trailing whitespace
            text = text.rstrip('\x00')
            return text
        except Exception as e:
            raise ValueError(f"Failed to decode numeric array to text: {e}")
    
    @staticmethod
    def numeric_to_binary(numeric_array: List[int]) -> str:
        """
        Convert 5-integer array to 40-bit binary string.
        
        Args:
            numeric_array: List of 5 integers (0-255)
            
        Returns:
            40-bit binary string
            
        Raises:
            ValueError: If array is not valid
        """
        # Validate input
        if len(numeric_array) != 5:
            raise ValueError(f"Numeric array must have exactly 5 integers, got {len(numeric_array)}")
        
        if not all(isinstance(x, int) and 0 <= x <= 255 for x in numeric_array):
            raise ValueError("All values must be integers between 0 and 255")
        
        # Convert each integer to 8-bit binary string
        binary_parts = []
        for num in numeric_array:
            binary_parts.append(format(num, '08b'))
        
        return ''.join(binary_parts)
    
    @staticmethod
    def validate_message(message: Union[str, List[int]], format_type: str) -> Tuple[bool, str]:
        """
        Validate message format.
        
        Args:
            message: Message to validate
            format_type: One of 'numeric', 'text', 'binary'
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if format_type == 'numeric':
            if not isinstance(message, list):
                return False, "Numeric message must be a list"
            
            if len(message) != 5:
                return False, f"Numeric message must have exactly 5 integers, got {len(message)}"
            
            for i, val in enumerate(message):
                if not isinstance(val, int):
                    return False, f"Value at index {i} must be an integer, got {type(val).__name__}"
                
                if not 0 <= val <= 255:
                    return False, f"Value at index {i} must be between 0 and 255, got {val}"
            
            return True, ""
        
        elif format_type == 'text':
            if not isinstance(message, str):
                return False, "Text message must be a string"
            
            if len(message) == 0:
                return False, "Text message cannot be empty"
            
            # Check if text can be encoded to UTF-8
            try:
                message.encode('utf-8')
            except UnicodeEncodeError:
                return False, "Text message contains invalid UTF-8 characters"
            
            return True, ""
        
        elif format_type == 'binary':
            if not isinstance(message, str):
                return False, "Binary message must be a string"
            
            # Remove whitespace for validation
            clean_binary = message.replace(' ', '').replace('_', '')
            
            if len(clean_binary) != 40:
                return False, f"Binary message must be exactly 40 bits, got {len(clean_binary)}"
            
            if not all(c in '01' for c in clean_binary):
                return False, "Binary message must contain only '0' and '1' characters"
            
            return True, ""
        
        else:
            return False, f"Invalid format type: {format_type}. Must be 'numeric', 'text', or 'binary'"
