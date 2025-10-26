# Tkinter GUI Walkthrough

## Overview

The standalone GUI provides a user-friendly graphical interface for audio watermarking operations without requiring command-line knowledge.

## Launch Instructions

```bash
cd backend
python standalone_demo_gui.py
```

## GUI Architecture

### Window Structure
```
┌─────────────────────────────────────────────────────────┐
│  Audio Watermarking Demo                          [_][□][X]│
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Encode] [Decode]                               │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [Tab Content Area - See below for details]            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Encode Tab Layout

```
┌─────────────────────────────────────────────────────────┐
│ Input Audio                                             │
│ ┌─────────────────────────────────────┐ [Browse...]    │
│ │ /path/to/input.wav                  │                │
│ └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Output Audio                                            │
│ ┌─────────────────────────────────────┐ [Browse...]    │
│ │ /path/to/output.wav                 │                │
│ └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Message                                                 │
│ Format: (•) Text  ( ) Numeric  ( ) Binary              │
│                                                         │
│ Message:                                                │
│ ┌─────────────────────────────────────────────────────┐│
│ │ Hello World                                         ││
│ └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘

              [Encode Watermark]

┌─────────────────────────────────────────────────────────┐
│ Results                                                 │
│ ┌─────────────────────────────────────────────────────┐│
│ │ Loading audio...                                    ││
│ │ Converting message (format: text)...                ││
│ │ Message (numeric): [72, 101, 108, 108, 111]        ││
│ │ Encoding watermark...                               ││
│ │ Saving watermarked audio...                         ││
│ │                                                     ││
│ │ ==================================================  ││
│ │ Encoding Complete!                                  ││
│ │ ==================================================  ││
│ │ Output file: /path/to/output.wav                    ││
│ │ SDR value: 50.14 dB                                 ││
│ │ Message: [72, 101, 108, 108, 111]                  ││
│ │ ==================================================  ││
│ └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Decode Tab Layout

```
┌─────────────────────────────────────────────────────────┐
│ Watermarked Audio                                       │
│ ┌─────────────────────────────────────┐ [Browse...]    │
│ │ /path/to/watermarked.wav            │                │
│ └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘

              [Decode Watermark]

┌─────────────────────────────────────────────────────────┐
│ Results                                                 │
│ ┌─────────────────────────────────────────────────────┐│
│ │ Loading audio...                                    ││
│ │ Decoding watermark...                               ││
│ │                                                     ││
│ │ ==================================================  ││
│ │ Watermark Detected!                                 ││
│ │ ==================================================  ││
│ │ Numeric:  [72, 101, 108, 108, 111]                 ││
│ │ Text:     'Hello'                                   ││
│ │ Binary:   0100100001100101011011000110110001101111  ││
│ │ Confidence: 0.9937                                  ││
│ │ ==================================================  ││
│ └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## User Workflow

### Encoding Workflow

1. **Select Input File**
   - Click "Browse..." button in Input Audio section
   - Navigate to your audio file (WAV format)
   - Select the file and click "Open"
   - File path appears in the text field

2. **Select Output File**
   - Click "Browse..." button in Output Audio section
   - Choose location and filename for watermarked audio
   - Click "Save"
   - File path appears in the text field

3. **Choose Message Format**
   - Select one of three radio buttons:
     - **Text**: For string messages (e.g., "Hello")
     - **Numeric**: For 5 comma-separated integers (e.g., "100,150,200,50,75")
     - **Binary**: For 40-bit binary strings (e.g., "1010...")

4. **Enter Message**
   - Type your message in the Message field
   - Format depends on selected format type

5. **Encode**
   - Click "Encode Watermark" button
   - Button becomes disabled during processing
   - Progress updates appear in Results area
   - Success dialog appears when complete

### Decoding Workflow

1. **Select Watermarked File**
   - Switch to "Decode" tab
   - Click "Browse..." button
   - Select watermarked audio file
   - File path appears in text field

2. **Decode**
   - Click "Decode Watermark" button
   - Button becomes disabled during processing
   - Progress updates appear in Results area
   - Results show message in all three formats
   - Success dialog appears when complete

## Features

### ✅ User-Friendly Interface
- No command-line knowledge required
- Visual file selection dialogs
- Clear labels and instructions
- Intuitive tab-based navigation

### ✅ Real-Time Feedback
- Progress updates during processing
- Results displayed in scrollable text area
- Success/error dialogs for important events
- Button states indicate processing status

### ✅ Non-Blocking Operations
- Threading prevents GUI freezing
- Can interact with window during processing
- Smooth user experience

### ✅ Comprehensive Results
- Encoding: Shows SDR value and message
- Decoding: Shows message in all formats
- Confidence scores for decoded messages
- Formatted output for readability

### ✅ Error Handling
- Validation before processing
- Clear error messages
- Graceful failure handling
- Helpful error dialogs

## Message Format Examples

### Text Format
```
Input:  "Hello"
Output: [72, 101, 108, 108, 111]
```

### Numeric Format
```
Input:  "123,234,111,222,11"
Output: [123, 234, 111, 222, 11]
```

### Binary Format
```
Input:  "1010101010101010101010101010101010101010"
Output: [170, 170, 170, 170, 170]
```

## Dialog Boxes

### Success Dialog (Encoding)
```
┌─────────────────────────────────┐
│ Success                    [X]  │
├─────────────────────────────────┤
│                                 │
│  Watermark encoded successfully!│
│  SDR: 50.14 dB                  │
│                                 │
│           [OK]                  │
└─────────────────────────────────┘
```

### Success Dialog (Decoding)
```
┌─────────────────────────────────┐
│ Success                    [X]  │
├─────────────────────────────────┤
│                                 │
│  Watermark decoded successfully!│
│  Message: [72, 101, 108, 108, 111]│
│                                 │
│           [OK]                  │
└─────────────────────────────────┘
```

### Error Dialog
```
┌─────────────────────────────────┐
│ Error                      [X]  │
├─────────────────────────────────┤
│                                 │
│  Please select an input audio   │
│  file                           │
│                                 │
│           [OK]                  │
└─────────────────────────────────┘
```

### Warning Dialog (No Watermark)
```
┌─────────────────────────────────┐
│ No Watermark               [X]  │
├─────────────────────────────────┤
│                                 │
│  No watermark detected in the   │
│  audio file                     │
│                                 │
│           [OK]                  │
└─────────────────────────────────┘
```

## Technical Details

### Threading Model
- Main thread: GUI event loop
- Worker threads: Encoding/decoding operations
- Thread-safe result updates
- Daemon threads for automatic cleanup

### Service Integration
- **AudioProcessor**: Load/save audio files
- **SilentCipherService**: Encode/decode watermarks
- **MessageConverter**: Format conversions

### State Management
- Button states prevent double-clicks
- Input validation before processing
- Results cleared on new operations
- File paths persisted in variables

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Activate focused button
- **Escape**: Close dialogs
- **Ctrl+A**: Select all in text fields

## Troubleshooting

### GUI Won't Launch
**Problem**: Window doesn't appear
**Solution**: 
- Ensure Tkinter is installed (comes with Python)
- Check SilentCipher is installed: `pip install silentcipher`
- Run from command line to see error messages

### Processing Takes Long Time
**Problem**: Encoding/decoding seems stuck
**Solution**:
- This is normal for longer audio files
- Wait for completion (can take 10-30 seconds)
- Check Results area for progress updates
- Don't close window during processing

### File Selection Issues
**Problem**: Can't select files
**Solution**:
- Ensure files are WAV format
- Check file permissions
- Use absolute paths if relative paths fail

### Error Messages
**Problem**: "Please select an input audio file"
**Solution**: Click Browse button and select a file

**Problem**: "Please enter a message to embed"
**Solution**: Type a message in the Message field

**Problem**: "Encoding failed: ..."
**Solution**: Check audio file format and message format

## Comparison: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| **Ease of Use** | Requires command knowledge | Point and click |
| **File Selection** | Type paths manually | Visual file browser |
| **Message Input** | Command-line argument | Text field with format selector |
| **Progress Feedback** | Text output | Real-time updates + dialogs |
| **Results Display** | Terminal output | Formatted scrollable text |
| **Automation** | Easy to script | Manual operation |
| **Learning Curve** | Steeper | Gentler |
| **Speed** | Faster for batch | Better for single files |

## Best Use Cases

### Use GUI When:
- ✅ Learning the system
- ✅ Processing single files
- ✅ Testing different messages
- ✅ Demonstrating to others
- ✅ Prefer visual interface

### Use CLI When:
- ✅ Automating workflows
- ✅ Batch processing
- ✅ Scripting operations
- ✅ Remote server access
- ✅ Integration with other tools

## Performance

- **Startup Time**: ~2-3 seconds
- **Encoding Time**: 5-15 seconds (depends on audio length)
- **Decoding Time**: 5-15 seconds (depends on audio length)
- **Memory Usage**: ~200-500 MB (includes model loading)
- **GUI Responsiveness**: Non-blocking, smooth interaction

## Accessibility

- Clear labels for all controls
- Logical tab order
- Keyboard navigation support
- High contrast text
- Scrollable results area
- Resizable window

## Future Enhancements (Potential)

- [ ] Progress bar for encoding/decoding
- [ ] Audio preview/playback
- [ ] Batch file processing
- [ ] Recent files list
- [ ] Drag-and-drop file support
- [ ] Settings/preferences dialog
- [ ] Export results to file
- [ ] Waveform visualization

## Conclusion

The Tkinter GUI provides an accessible, user-friendly interface for audio watermarking operations. It's ideal for users who prefer graphical interfaces over command-line tools, while maintaining all the functionality of the CLI version.

For automation and batch processing, use the CLI version (`standalone_demo.py`).
For interactive, single-file operations, use the GUI version (`standalone_demo_gui.py`).
