# 📥 PDF Download Guide - Conflict-Free Class Scheduling System

## 🎯 **Quick Start: Generate & Download PDF**

### **Option 1: Automatic PDF Generation (Recommended)**
```bash
# Generate schedule with automatic PDF conversion
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database

# The system will automatically:
# 1. Generate HTML schedule
# 2. Convert HTML to PDF using Chrome
# 3. Open the PDF file
```

### **Option 2: Manual PDF Generation**
```bash
# Generate HTML first
./bin/scheduler --input data/sample_courses.txt --algorithm graph-coloring --pdf --no-database

# Then convert manually using the script
./scripts/html_to_pdf.sh graph-coloring.html my_schedule.pdf
```

## 📋 **Complete Step-by-Step Process**

### **Step 1: Generate Schedule Data**
```bash
# Choose your input method:

# Method A: Use sample data
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database

# Method B: Use simple schedule
./bin/scheduler --input data/simple_schedule.txt --algorithm backtracking --pdf --no-database

# Method C: Create your own input file
cat > my_courses.txt << EOF
Data Structures,9,11,50
Algorithms,10,12,45
Database Systems,13,15,40
Computer Networks,14,16,35
Software Engineering,16,18,30
EOF

./bin/scheduler --input my_courses.txt --algorithm genetic --pdf --no-database
```

### **Step 2: PDF Files Are Generated Automatically**
After running the command, you'll see:
```
✅ PDF generated successfully: dynamic-prog.pdf
📊 File size: 252 KB
PDF generated successfully! Opening in browser...
```

### **Step 3: Find Your PDF Files**
All PDF files are saved in the project root directory:
```
📁 ConflictFreeScheduling/
├── dynamic-prog.pdf      ← Dynamic Programming result
├── graph-coloring.pdf    ← Graph Coloring result  
├── backtracking.pdf      ← Backtracking result
├── genetic.pdf           ← Genetic Algorithm result
└── schedule.pdf          ← Custom named PDF
```

## 🔧 **Advanced PDF Options**

### **Custom Output Names**
```bash
# Generate PDF with custom name
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database
./scripts/html_to_pdf.sh dynamic-prog.html "CSE_Spring_2025_Schedule.pdf"
```

### **Multiple Algorithm Comparison**
```bash
# Generate PDFs for all algorithms
./bin/scheduler --input data/sample_courses.txt --algorithm graph-coloring --pdf --no-database
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database  
./bin/scheduler --input data/sample_courses.txt --algorithm backtracking --pdf --no-database
./bin/scheduler --input data/sample_courses.txt --algorithm genetic --pdf --no-database

# Now you have 4 PDFs to compare different approaches!
```

### **High-Quality PDF Settings**
```bash
# For presentation-quality PDFs, modify the HTML and regenerate:
# The system automatically uses high-DPI settings for crisp output
```

## 🌐 **Browser-Based PDF Generation (Fallback)**

If automatic conversion fails, the system opens HTML in your browser:

### **macOS (Safari/Chrome)**
1. HTML file opens automatically in browser
2. Press `Cmd + P` 
3. Select "Save as PDF" from destination dropdown
4. Choose save location and filename
5. Click "Save"

### **Alternative Browsers**
- **Chrome**: `Cmd + P` → "Save as PDF"
- **Firefox**: `Cmd + P` → "Save to PDF"
- **Safari**: `Cmd + P` → "PDF" dropdown → "Save as PDF"

## 📊 **PDF Content Overview**

Each generated PDF includes:

### **Header Section**
- 🎓 Bangladesh University of Professionals branding
- 🏢 Computer Science & Engineering Department
- 📅 Schedule title and algorithm used

### **Statistics Dashboard**
- 📈 Number of courses scheduled
- 👥 Total students served  
- ⚡ Scheduling efficiency metrics
- 🔍 Algorithm performance data

### **Schedule Table**
- 📋 Course ID, Name, Start/End times
- ⏱️ Duration and student count
- ✅ Scheduling status indicators

### **Timeline Visualization**
- 📅 Daily timeline with time slots
- 🎨 Color-coded course blocks
- 📐 Visual conflict representation

### **Footer Information**
- 🔧 System version and generation timestamp
- 📄 Print instructions for physical copies

## 🚀 **Production Use Cases**

### **Academic Administration**
```bash
# Generate semester schedule
./bin/scheduler --input semester_courses.txt --algorithm dynamic-prog --pdf --no-database
# → Share PDF with department heads

# Generate room allocation reports  
./bin/scheduler --input room_data.txt --algorithm graph-coloring --pdf --no-database
# → Print for faculty distribution
```

### **Student Distribution**
```bash
# Create student-friendly schedules
./bin/scheduler --input student_courses.txt --algorithm backtracking --pdf --no-database
# → Email PDF to students

# Generate mobile-optimized versions
# PDFs are responsive and mobile-friendly for viewing on phones
```

## 🛠️ **Troubleshooting PDF Generation**

### **Problem: "Chrome not found" error**
**Solution:**
```bash
# Install Chrome (if needed)
# macOS: Download from google.com/chrome
# Or use Homebrew:
brew install --cask google-chrome

# Verify installation
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

### **Problem: PDF is blank or corrupted**
**Solution:**
```bash
# Regenerate HTML first
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --no-database
# Then convert manually
./scripts/html_to_pdf.sh dynamic-prog.html fixed_schedule.pdf
```

### **Problem: PDF doesn't open automatically**
**Solution:**
```bash
# Open PDF manually
open backtracking.pdf  # macOS
# or
xdg-open backtracking.pdf  # Linux
```

### **Problem: Need higher quality PDF**
**Solution:**
```bash
# Use Chrome with custom DPI settings
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --print-to-pdf=high_quality.pdf \
  --print-to-pdf-no-header --virtual-time-budget=5000 \
  "file://$(pwd)/dynamic-prog.html"
```

## 📱 **Mobile & Sharing**

### **Email Distribution**
- PDF files are optimized for email (typically 200-300 KB)
- Professional layout suitable for institutional communication
- Mobile-responsive design for smartphone viewing

### **Print Quality**
- PDFs include print-specific CSS optimizations
- Page breaks prevent content splitting
- High contrast for clear printing

### **Digital Sharing**
- Web-optimized file sizes
- Cross-platform compatibility (Windows, macOS, Linux)
- Professional appearance for presentations

## 🎉 **Success Examples**

Your PDF generation is working perfectly when you see:
```
✅ PDF generated successfully: dynamic-prog.pdf
📊 File size: 252 KB
PDF generated successfully! Opening in browser...
```

The system now provides a complete **Text Input → Algorithm Processing → Professional PDF Output** workflow!

---

**🔗 For more help**: Check `USER_GUIDE.md` for comprehensive system documentation.
