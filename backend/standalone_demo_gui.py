#!/usr/bin/env python3
"""
Standalone Audio Watermarking Demo - GUI Interface

A simple Tkinter-based GUI for testing SilentCipher audio watermarking
functionality. This provides a graphical alternative to the CLI interface.

Usage:
    python standalone_demo_gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import threading

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.audio_processor import AudioProcessor
from services.silentcipher_service import SilentCipherService
from utils.message_converter import MessageConverter


class WatermarkingGUI:
    """Simple GUI for audio watermarking operations."""
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Audio Watermarking Demo")
        self.root.geometry("700x600")
        
        # Initialize services
        self.audio_processor = AudioProcessor()
        self.silentcipher_service = SilentCipherService()
        self.message_converter = MessageConverter()
        
        # Check if SilentCipher is available
        if not self.silentcipher_service.is_available():
            messagebox.showerror(
                "Error",
                "SilentCipher library is not installed.\n"
                "Install with: pip install silentcipher"
            )
            self.root.destroy()
            return
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout GUI widgets."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create encode tab
        encode_frame = ttk.Frame(notebook)
        notebook.add(encode_frame, text='Encode')
        self.create_encode_tab(encode_frame)
        
        # Create decode tab
        decode_frame = ttk.Frame(notebook)
        notebook.add(decode_frame, text='Decode')
        self.create_decode_tab(decode_frame)
    
    def create_encode_tab(self, parent):
        """Create the encode tab widgets."""
        # Input file selection
        input_frame = ttk.LabelFrame(parent, text="Input Audio", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.encode_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.encode_input_var, width=50).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_encode_input).pack(side='left')
        
        # Output file selection
        output_frame = ttk.LabelFrame(parent, text="Output Audio", padding=10)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        self.encode_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.encode_output_var, width=50).pack(side='left', padx=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_encode_output).pack(side='left')
        
        # Message input
        message_frame = ttk.LabelFrame(parent, text="Message", padding=10)
        message_frame.pack(fill='x', padx=10, pady=5)
        
        # Format selection
        format_frame = ttk.Frame(message_frame)
        format_frame.pack(fill='x', pady=5)
        ttk.Label(format_frame, text="Format:").pack(side='left', padx=5)
        
        self.encode_format_var = tk.StringVar(value='text')
        ttk.Radiobutton(format_frame, text="Text", variable=self.encode_format_var, value='text').pack(side='left', padx=5)
        ttk.Radiobutton(format_frame, text="Numeric", variable=self.encode_format_var, value='numeric').pack(side='left', padx=5)
        ttk.Radiobutton(format_frame, text="Binary", variable=self.encode_format_var, value='binary').pack(side='left', padx=5)
        
        # Message entry
        ttk.Label(message_frame, text="Message:").pack(anchor='w', padx=5)
        self.encode_message_var = tk.StringVar()
        ttk.Entry(message_frame, textvariable=self.encode_message_var, width=60).pack(fill='x', padx=5, pady=5)
        
        # Encode button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.encode_button = ttk.Button(button_frame, text="Encode Watermark", command=self.encode_watermark)
        self.encode_button.pack()
        
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.encode_results = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.encode_results.pack(fill='both', expand=True)
    
    def create_decode_tab(self, parent):
        """Create the decode tab widgets."""
        # Input file selection
        input_frame = ttk.LabelFrame(parent, text="Watermarked Audio", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.decode_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.decode_input_var, width=50).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_decode_input).pack(side='left')
        
        # Decode button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.decode_button = ttk.Button(button_frame, text="Decode Watermark", command=self.decode_watermark)
        self.decode_button.pack()
        
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.decode_results = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD)
        self.decode_results.pack(fill='both', expand=True)
    
    def browse_encode_input(self):
        """Browse for input audio file for encoding."""
        filename = filedialog.askopenfilename(
            title="Select Input Audio File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.encode_input_var.set(filename)
    
    def browse_encode_output(self):
        """Browse for output audio file for encoding."""
        filename = filedialog.asksaveasfilename(
            title="Save Watermarked Audio As",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.encode_output_var.set(filename)
    
    def browse_decode_input(self):
        """Browse for input audio file for decoding."""
        filename = filedialog.askopenfilename(
            title="Select Watermarked Audio File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.decode_input_var.set(filename)
    
    def encode_watermark(self):
        """Execute the encoding workflow in a separate thread."""
        # Validate inputs
        input_file = self.encode_input_var.get()
        output_file = self.encode_output_var.get()
        message = self.encode_message_var.get()
        format_type = self.encode_format_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input audio file")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output file path")
            return
        
        if not message:
            messagebox.showerror("Error", "Please enter a message to embed")
            return
        
        # Disable button during processing
        self.encode_button.config(state='disabled')
        self.encode_results.delete(1.0, tk.END)
        self.encode_results.insert(tk.END, "Encoding in progress...\n")
        
        # Run encoding in separate thread to avoid blocking GUI
        thread = threading.Thread(
            target=self._encode_thread,
            args=(input_file, output_file, message, format_type)
        )
        thread.daemon = True
        thread.start()
    
    def _encode_thread(self, input_file, output_file, message, format_type):
        """Execute encoding in a separate thread."""
        try:
            # Load audio
            self._update_results(self.encode_results, "Loading audio...\n")
            audio_data, sample_rate = self.audio_processor.load_audio(input_file)
            
            # Validate audio
            metadata = self.audio_processor.get_metadata(audio_data, sample_rate)
            
            # Check duration
            if metadata['duration'] < 3.0:
                raise ValueError(
                    f"Audio too short ({metadata['duration']:.2f}s). "
                    f"SilentCipher requires at least 3 seconds of audio for reliable watermarking."
                )
            
            # Check sample rate
            if sample_rate not in [16000, 44100]:
                self._update_results(
                    self.encode_results,
                    f"⚠ Warning: Sample rate is {sample_rate}Hz. "
                    f"SilentCipher works best with 16kHz or 44.1kHz.\n"
                    f"Audio will be resampled automatically.\n"
                )
            
            # Convert message
            self._update_results(self.encode_results, f"Converting message (format: {format_type})...\n")
            if format_type == 'numeric':
                message_values = [int(p.strip()) for p in message.split(',')]
            elif format_type == 'text':
                message_values = self.message_converter.text_to_numeric(message)
            elif format_type == 'binary':
                message_values = self.message_converter.binary_to_numeric(message)
            
            self._update_results(self.encode_results, f"Message (numeric): {message_values}\n")
            
            # Encode watermark
            self._update_results(self.encode_results, "Encoding watermark...\n")
            watermarked_audio, sdr = self.silentcipher_service.encode_audio(
                audio_data, sample_rate, message_values
            )
            
            # Save audio
            self._update_results(self.encode_results, "Saving watermarked audio...\n")
            self.audio_processor.save_audio(watermarked_audio, sample_rate, output_file)
            
            # Display results
            self._update_results(
                self.encode_results,
                f"\n{'='*50}\n"
                f"Encoding Complete!\n"
                f"{'='*50}\n"
                f"Output file: {output_file}\n"
                f"SDR value: {sdr:.2f} dB\n"
                f"Message: {message_values}\n"
                f"{'='*50}\n"
            )
            
            messagebox.showinfo("Success", f"Watermark encoded successfully!\nSDR: {sdr:.2f} dB")
            
        except Exception as e:
            self._update_results(self.encode_results, f"\nError: {e}\n")
            messagebox.showerror("Error", f"Encoding failed: {e}")
        
        finally:
            # Re-enable button
            self.encode_button.config(state='normal')
    
    def decode_watermark(self):
        """Execute the decoding workflow in a separate thread."""
        # Validate inputs
        input_file = self.decode_input_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select a watermarked audio file")
            return
        
        # Disable button during processing
        self.decode_button.config(state='disabled')
        self.decode_results.delete(1.0, tk.END)
        self.decode_results.insert(tk.END, "Decoding in progress...\n")
        
        # Run decoding in separate thread to avoid blocking GUI
        thread = threading.Thread(
            target=self._decode_thread,
            args=(input_file,)
        )
        thread.daemon = True
        thread.start()
    
    def _decode_thread(self, input_file):
        """Execute decoding in a separate thread."""
        try:
            # Load audio
            self._update_results(self.decode_results, "Loading audio...\n")
            audio_data, sample_rate = self.audio_processor.load_audio(input_file)
            
            # Decode watermark
            self._update_results(self.decode_results, "Decoding watermark...\n")
            result = self.silentcipher_service.decode_audio(audio_data, sample_rate)
            
            if not result['detected']:
                self._update_results(
                    self.decode_results,
                    f"\n{'='*50}\n"
                    f"No Watermark Detected\n"
                    f"{'='*50}\n"
                    f"The audio file does not contain a detectable watermark.\n"
                )
                messagebox.showwarning("No Watermark", "No watermark detected in the audio file")
                return
            
            # Convert message to other formats
            message_values = result['message']
            text_message = self.message_converter.numeric_to_text(message_values)
            binary_message = self.message_converter.numeric_to_binary(message_values)
            
            # Display results
            confidence = result.get('confidence', 'N/A')
            self._update_results(
                self.decode_results,
                f"\n{'='*50}\n"
                f"Watermark Detected!\n"
                f"{'='*50}\n"
                f"Numeric:  {message_values}\n"
                f"Text:     '{text_message}'\n"
                f"Binary:   {binary_message}\n"
                f"Confidence: {confidence}\n"
                f"{'='*50}\n"
            )
            
            messagebox.showinfo("Success", f"Watermark decoded successfully!\nMessage: {message_values}")
            
        except Exception as e:
            self._update_results(self.decode_results, f"\nError: {e}\n")
            messagebox.showerror("Error", f"Decoding failed: {e}")
        
        finally:
            # Re-enable button
            self.decode_button.config(state='normal')
    
    def _update_results(self, text_widget, message):
        """
        Update results text widget from a thread.
        
        Args:
            text_widget: ScrolledText widget to update
            message: Message to append
        """
        text_widget.insert(tk.END, message)
        text_widget.see(tk.END)
        text_widget.update()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = WatermarkingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
