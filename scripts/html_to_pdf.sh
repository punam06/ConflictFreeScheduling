#!/bin/bash

# HTML to PDF Converter Script
# Usage: ./scripts/html_to_pdf.sh input.html output.pdf

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input.html> <output.pdf>"
    echo "Example: $0 graph-coloring.html schedule.pdf"
    exit 1
fi

INPUT_HTML="$1"
OUTPUT_PDF="$2"

# Check if input file exists
if [ ! -f "$INPUT_HTML" ]; then
    echo "Error: Input file '$INPUT_HTML' not found!"
    exit 1
fi

# Convert to absolute path
INPUT_PATH=$(realpath "$INPUT_HTML")

echo "Converting HTML to PDF..."
echo "Input: $INPUT_PATH"
echo "Output: $OUTPUT_PDF"

# Method 1: Try Chrome/Chromium headless
if command -v google-chrome >/dev/null 2>&1; then
    echo "Using Google Chrome for conversion..."
    google-chrome --headless --disable-gpu --print-to-pdf="$OUTPUT_PDF" "file://$INPUT_PATH"
    echo "✅ PDF generated: $OUTPUT_PDF"
elif command -v chromium >/dev/null 2>&1; then
    echo "Using Chromium for conversion..."
    chromium --headless --disable-gpu --print-to-pdf="$OUTPUT_PDF" "file://$INPUT_PATH"
    echo "✅ PDF generated: $OUTPUT_PDF"
elif command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" >/dev/null 2>&1; then
    echo "Using Google Chrome (macOS) for conversion..."
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --print-to-pdf="$OUTPUT_PDF" "file://$INPUT_PATH"
    echo "✅ PDF generated: $OUTPUT_PDF"
else
    echo "❌ Chrome/Chromium not found!"
    echo ""
    echo "Alternative methods:"
    echo "1. Install Chrome: brew install --cask google-chrome"
    echo "2. Use browser: Open $INPUT_HTML and print to PDF (Cmd+P)"
    echo "3. Use online converter: Upload HTML file to HTML-to-PDF service"
    exit 1
fi

# Check if PDF was created
if [ -f "$OUTPUT_PDF" ]; then
    echo "🎉 Success! PDF created: $OUTPUT_PDF"
    echo "📊 File size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    
    # Open PDF on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "📖 Opening PDF..."
        open "$OUTPUT_PDF"
    fi
else
    echo "❌ PDF generation failed!"
    exit 1
fi
