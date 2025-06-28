#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference-Based Academic Routine Generator
Generates academic routines matching the exact format of the reference PDF
with Days as first column and time slots as column headers
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ReferencePDFRoutineGenerator:
    """Generate academic routines matching the reference PDF format exactly"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        self.section_style = ParagraphStyle(
            'SectionStyle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.darkred,
            fontName='Helvetica-Bold'
        )

    def load_routine_data(self, data_file):
        """Load routine data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading routine data: {e}")
            return None

    def format_class_info(self, class_data):
        """Format class information for display in table cell"""
        if not class_data:
            return ""
        
        course_code = class_data.get('course', '')
        course_name = class_data.get('name', '')
        faculty = class_data.get('faculty', '')
        room = class_data.get('room', '')
        class_type = class_data.get('type', '')
        
        # Format: CSE 241\nData Structures\nDr. Dip Nandi\nRoom: 302
        formatted = f"{course_code}\n{course_name}\n{faculty}\nRoom: {room}"
        if class_type == "Lab":
            formatted += f"\n({class_type})"
        
        return formatted

    def create_routine_table_for_section(self, section_data, time_slots):
        """Create routine table for a specific section"""
        # Header row: Days as first column, then time slots
        header = ["Days"] + [slot["slot"] for slot in time_slots]
        
        # Data rows
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        table_data = [header]
        
        for day in days:
            row = [day]
            day_schedule = section_data.get(day, {})
            
            for slot in time_slots:
                slot_time = slot["slot"]
                class_info = day_schedule.get(slot_time, {})
                formatted_info = self.format_class_info(class_info)
                row.append(formatted_info)
            
            table_data.append(row)
        
        # Create table
        table = Table(table_data, colWidths=[1.2*inch] + [2*inch] * len(time_slots))
        
        # Table styling
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Days column styling
            ('BACKGROUND', (0, 1), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.darkblue),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 9),
            
            # Data cells styling
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Alternating row colors for better readability
            ('BACKGROUND', (1, 1), (-1, 1), colors.lightgrey),
            ('BACKGROUND', (1, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (1, 5), (-1, 5), colors.lightgrey),
        ]))
        
        return table

    def create_html_routine_for_section(self, section_name, section_data, time_slots, metadata):
        """Create HTML routine table for a specific section"""
        html = f"""
        <div class="section-container">
            <h2 class="section-title">{section_name} - Class Routine</h2>
            <div class="table-container">
                <table class="routine-table">
                    <thead>
                        <tr class="header-row">
                            <th class="day-header">Days</th>
        """
        
        # Add time slot headers
        for slot in time_slots:
            html += f'<th class="time-header">{slot["slot"]}</th>'
        
        html += """
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add day rows
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        for i, day in enumerate(days):
            row_class = "odd-row" if i % 2 == 0 else "even-row"
            html += f'<tr class="{row_class}">'
            html += f'<td class="day-cell">{day}</td>'
            
            day_schedule = section_data.get(day, {})
            for slot in time_slots:
                slot_time = slot["slot"]
                class_info = day_schedule.get(slot_time, {})
                
                if class_info:
                    course_code = class_info.get('course', '')
                    course_name = class_info.get('name', '')
                    faculty = class_info.get('faculty', '')
                    room = class_info.get('room', '')
                    class_type = class_info.get('type', '')
                    
                    cell_content = f"""
                        <div class="class-info">
                            <div class="course-code">{course_code}</div>
                            <div class="course-name">{course_name}</div>
                            <div class="faculty-name">{faculty}</div>
                            <div class="room-info">Room: {room}</div>
                            {f'<div class="class-type">({class_type})</div>' if class_type == "Lab" else ""}
                        </div>
                    """
                else:
                    cell_content = '<div class="no-class">-</div>'
                
                html += f'<td class="schedule-cell">{cell_content}</td>'
            
            html += '</tr>'
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html

    def generate_comprehensive_html(self, data_file, output_file):
        """Generate comprehensive HTML routine for all sections"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        metadata = data.get('metadata', {})
        schedule_config = data.get('schedule_config', {})
        time_slots = schedule_config.get('time_slots', [])
        routine_data = data.get('routine', {})
        
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Academic Routine - {metadata.get('semester', 'Spring 2025')}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                
                .header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                
                .header .subtitle {{
                    font-size: 1.2em;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                
                .content {{
                    padding: 30px;
                }}
                
                .section-container {{
                    margin-bottom: 40px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 25px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                
                .section-title {{
                    color: #1e3c72;
                    font-size: 1.8em;
                    margin-bottom: 20px;
                    text-align: center;
                    border-bottom: 3px solid #2a5298;
                    padding-bottom: 10px;
                }}
                
                .table-container {{
                    overflow-x: auto;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                
                .routine-table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                }}
                
                .header-row {{
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    color: white;
                }}
                
                .day-header, .time-header {{
                    padding: 15px 10px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 0.95em;
                    border: 1px solid #ddd;
                }}
                
                .day-header {{
                    background: #1a237e;
                    min-width: 120px;
                }}
                
                .time-header {{
                    min-width: 180px;
                }}
                
                .day-cell {{
                    background: #e3f2fd;
                    color: #1565c0;
                    font-weight: bold;
                    text-align: center;
                    padding: 15px 10px;
                    border: 1px solid #ddd;
                    vertical-align: middle;
                    min-width: 120px;
                }}
                
                .schedule-cell {{
                    padding: 12px 8px;
                    text-align: center;
                    vertical-align: middle;
                    border: 1px solid #ddd;
                    min-width: 180px;
                    max-width: 180px;
                }}
                
                .odd-row {{
                    background: #fafafa;
                }}
                
                .even-row {{
                    background: #ffffff;
                }}
                
                .class-info {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    line-height: 1.4;
                }}
                
                .course-code {{
                    font-weight: bold;
                    color: #1565c0;
                    font-size: 0.9em;
                    margin-bottom: 3px;
                }}
                
                .course-name {{
                    color: #2e7d32;
                    font-size: 0.85em;
                    margin-bottom: 3px;
                    font-weight: 500;
                }}
                
                .faculty-name {{
                    color: #d32f2f;
                    font-size: 0.8em;
                    margin-bottom: 3px;
                    font-style: italic;
                }}
                
                .room-info {{
                    color: #7b1fa2;
                    font-size: 0.8em;
                    font-weight: bold;
                    margin-bottom: 2px;
                }}
                
                .class-type {{
                    color: #f57c00;
                    font-size: 0.75em;
                    font-weight: bold;
                    font-style: italic;
                }}
                
                .no-class {{
                    color: #999;
                    font-size: 1.2em;
                    font-weight: bold;
                }}
                
                .info-section {{
                    background: #e8f5e8;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    border-left: 5px solid #4caf50;
                }}
                
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                
                .info-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 6px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .info-label {{
                    font-weight: bold;
                    color: #2e7d32;
                    margin-bottom: 5px;
                }}
                
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background: #f5f5f5;
                    color: #666;
                    font-size: 0.9em;
                }}
                
                @media (max-width: 768px) {{
                    body {{
                        padding: 10px;
                    }}
                    
                    .header h1 {{
                        font-size: 2em;
                    }}
                    
                    .content {{
                        padding: 20px;
                    }}
                    
                    .section-container {{
                        padding: 15px;
                    }}
                    
                    .routine-table {{
                        font-size: 0.85em;
                    }}
                    
                    .schedule-cell {{
                        min-width: 140px;
                        max-width: 140px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{metadata.get('university', 'Bangladesh University of Professionals')}</h1>
                    <div class="subtitle">
                        {metadata.get('department', 'Computer Science & Engineering')}<br>
                        Academic Routine - {metadata.get('semester', 'Spring 2025')}
                    </div>
                </div>
                
                <div class="content">
                    <div class="info-section">
                        <h3 style="color: #2e7d32; margin-bottom: 15px;">📋 Schedule Information</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">🏫 Available Rooms:</div>
                                <div>{', '.join(data.get('rooms', []))}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">📅 Academic Year:</div>
                                <div>{metadata.get('academic_year', '2024-2025')}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">🕐 Class Duration:</div>
                                <div>90 minutes per session</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">📝 Last Updated:</div>
                                <div>{datetime.now().strftime('%B %d, %Y')}</div>
                            </div>
                        </div>
                    </div>
        """
        
        # Add routine tables for each section
        for section_name, section_data in routine_data.items():
            html_content += self.create_html_routine_for_section(section_name, section_data, time_slots, metadata)
        
        html_content += f"""
                </div>
                
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>Enhanced Conflict-Free Scheduling System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write HTML file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML routine generated successfully: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error generating HTML routine: {e}")
            return False

    def generate_comprehensive_pdf(self, data_file, output_file):
        """Generate comprehensive PDF routine for all sections"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        try:
            doc = SimpleDocTemplate(output_file, pagesize=landscape(A4), 
                                   rightMargin=20, leftMargin=20, 
                                   topMargin=30, bottomMargin=30)
            
            story = []
            metadata = data.get('metadata', {})
            schedule_config = data.get('schedule_config', {})
            time_slots = schedule_config.get('time_slots', [])
            routine_data = data.get('routine', {})
            
            # Title
            title = Paragraph(f"{metadata.get('university', 'Bangladesh University of Professionals')}", 
                            self.title_style)
            story.append(title)
            
            subtitle = Paragraph(f"{metadata.get('department', 'Computer Science & Engineering')}<br/>"
                               f"Academic Routine - {metadata.get('semester', 'Spring 2025')}", 
                               self.subtitle_style)
            story.append(subtitle)
            story.append(Spacer(1, 20))
            
            # Add routine tables for each section
            for section_name, section_data in routine_data.items():
                section_title = Paragraph(f"{section_name} - Class Routine", self.section_style)
                story.append(section_title)
                story.append(Spacer(1, 10))
                
                table = self.create_routine_table_for_section(section_data, time_slots)
                story.append(table)
                story.append(Spacer(1, 20))
                
                # Add page break except for the last section
                sections = list(routine_data.keys())
                if section_name != sections[-1]:
                    story.append(PageBreak())
            
            # Footer info
            footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | " \
                         f"Available Rooms: {', '.join(data.get('rooms', []))}"
            footer = Paragraph(footer_text, self.styles['Normal'])
            story.append(Spacer(1, 20))
            story.append(footer)
            
            doc.build(story)
            print(f"✅ PDF routine generated successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF routine: {e}")
            return False

    def generate_all_formats(self, data_file, base_output_name):
        """Generate both HTML and PDF formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        html_file = f"{base_output_name}_{timestamp}.html"
        pdf_file = f"{base_output_name}_{timestamp}.pdf"
        
        html_success = self.generate_comprehensive_html(data_file, html_file)
        pdf_success = self.generate_comprehensive_pdf(data_file, pdf_file)
        
        if html_success and pdf_success:
            print(f"\n🎉 All formats generated successfully!")
            print(f"📄 HTML: {html_file}")
            print(f"📄 PDF: {pdf_file}")
            return html_file, pdf_file
        else:
            print(f"\n⚠️ Some formats failed to generate")
            return None, None


def main():
    """Main function to demonstrate the generator"""
    generator = ReferencePDFRoutineGenerator()
    
    # Input and output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    data_file = os.path.join(project_root, "data", "reference_based_routine_data.json")
    output_dir = os.path.join(project_root, "output")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    base_output = os.path.join(output_dir, "reference_based_comprehensive_routine")
    
    print("🚀 Generating Reference-Based Academic Routine...")
    print(f"📁 Data file: {data_file}")
    print(f"📁 Output directory: {output_dir}")
    
    html_file, pdf_file = generator.generate_all_formats(data_file, base_output)
    
    if html_file and pdf_file:
        print(f"\n✨ Generation completed successfully!")
        print(f"🌐 Open HTML file: file://{os.path.abspath(html_file)}")
        print(f"📋 PDF file: {os.path.abspath(pdf_file)}")
    else:
        print(f"\n❌ Generation failed!")


if __name__ == "__main__":
    main()
