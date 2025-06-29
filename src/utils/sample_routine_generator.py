#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Academic Routine Generator
Generates comprehensive academic routines based on sample PDF format
with faculty preferences and optimal scheduling to minimize class gaps
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


class SampleRoutineGenerator:
    """Generate academic routines based on sample PDF format with enhanced UI"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            spaceAfter=25,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        self.section_style = ParagraphStyle(
            'SectionStyle',
            parent=self.styles['Heading3'],
            fontSize=16,
            spaceAfter=15,
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

    def create_routine_table_for_section(self, section_name, section_data, time_slots):
        """Create routine table for a specific section with enhanced styling"""
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
        
        # Calculate column widths
        col_width = 2.2 * inch
        day_col_width = 1.3 * inch
        table = Table(table_data, colWidths=[day_col_width] + [col_width] * len(time_slots))
        
        # Enhanced table styling matching sample PDF
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.7)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            
            # Days column styling
            ('BACKGROUND', (0, 1), (0, -1), colors.Color(0.8, 0.9, 1.0)),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.Color(0.2, 0.3, 0.7)),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 10),
            ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),
            
            # Data cells styling
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1.5, colors.Color(0.3, 0.3, 0.3)),
            
            # Alternating row colors for better readability
            ('BACKGROUND', (1, 1), (-1, 1), colors.Color(0.95, 0.98, 1.0)),
            ('BACKGROUND', (1, 3), (-1, 3), colors.Color(0.95, 0.98, 1.0)),
            ('BACKGROUND', (1, 5), (-1, 5), colors.Color(0.95, 0.98, 1.0)),
            
            # Special styling for filled cells
            ('TEXTCOLOR', (1, 1), (-1, -1), colors.Color(0.1, 0.1, 0.1)),
        ]))
        
        return table

    def create_enhanced_html_routine(self, data_file, output_file):
        """Create comprehensive HTML routine with enhanced UI design"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        metadata = data.get('metadata', {})
        schedule_config = data.get('schedule_config', {})
        time_slots = schedule_config.get('time_slots', [])
        routine_data = data.get('routine', {})
        
        # Enhanced HTML template with modern UI
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Academic Class Routine - {metadata.get('semester', 'Spring 2025')}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #2c3e50;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1500px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.98);
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                    backdrop-filter: blur(10px);
                }}
                
                .header {{
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    color: white;
                    padding: 40px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                
                .header::before {{
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                    transform: rotate(45deg);
                    animation: shine 3s infinite;
                }}
                
                @keyframes shine {{
                    0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
                    100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
                }}
                
                .header h1 {{
                    font-size: 2.8em;
                    margin-bottom: 15px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
                    font-weight: 700;
                }}
                
                .header .subtitle {{
                    font-size: 1.4em;
                    opacity: 0.95;
                    font-weight: 300;
                    margin-bottom: 10px;
                }}
                
                .header .semester {{
                    font-size: 1.1em;
                    background: rgba(255,255,255,0.2);
                    padding: 8px 20px;
                    border-radius: 25px;
                    display: inline-block;
                    margin-top: 10px;
                }}
                
                .content {{
                    padding: 40px;
                }}
                
                .info-section {{
                    background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
                    padding: 25px;
                    border-radius: 15px;
                    margin-bottom: 35px;
                    border-left: 6px solid #4caf50;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                }}
                
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                
                .info-item {{
                    background: white;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                
                .info-item:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                }}
                
                .info-label {{
                    font-weight: bold;
                    color: #2e7d32;
                    margin-bottom: 8px;
                    font-size: 1.1em;
                }}
                
                .section-container {{
                    margin-bottom: 50px;
                    background: linear-gradient(135deg, #f8f9fa, #ffffff);
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    position: relative;
                    overflow: hidden;
                }}
                
                .section-container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                }}
                
                .section-title {{
                    color: #1e3c72;
                    font-size: 2.2em;
                    margin-bottom: 25px;
                    text-align: center;
                    font-weight: 700;
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
                }}
                
                .table-container {{
                    overflow-x: auto;
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    background: white;
                }}
                
                .routine-table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border-radius: 15px;
                    overflow: hidden;
                    font-size: 0.95em;
                }}
                
                .header-row {{
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    color: white;
                }}
                
                .day-header, .time-header {{
                    padding: 18px 12px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 1em;
                    border: none;
                    position: relative;
                }}
                
                .day-header {{
                    background: linear-gradient(45deg, #1a237e, #3949ab);
                    min-width: 130px;
                    font-size: 1.1em;
                }}
                
                .time-header {{
                    min-width: 200px;
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                }}
                
                .day-cell {{
                    background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
                    color: #1565c0;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px 15px;
                    border: 2px solid #e0e0e0;
                    vertical-align: middle;
                    min-width: 130px;
                    font-size: 1.05em;
                }}
                
                .schedule-cell {{
                    padding: 15px 10px;
                    text-align: center;
                    vertical-align: middle;
                    border: 2px solid #e0e0e0;
                    min-width: 200px;
                    max-width: 200px;
                    transition: background-color 0.3s ease;
                }}
                
                .schedule-cell:hover {{
                    background-color: #f8f9fa;
                }}
                
                .odd-row {{
                    background: linear-gradient(135deg, #fafafa, #ffffff);
                }}
                
                .even-row {{
                    background: linear-gradient(135deg, #ffffff, #f8f9fa);
                }}
                
                .class-info {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    line-height: 1.5;
                    padding: 5px;
                }}
                
                .course-code {{
                    font-weight: bold;
                    color: #1565c0;
                    font-size: 0.95em;
                    margin-bottom: 4px;
                    background: linear-gradient(45deg, #e3f2fd, #f3e5f5);
                    padding: 3px 8px;
                    border-radius: 8px;
                }}
                
                .course-name {{
                    color: #2e7d32;
                    font-size: 0.88em;
                    margin-bottom: 4px;
                    font-weight: 600;
                }}
                
                .faculty-name {{
                    color: #d32f2f;
                    font-size: 0.85em;
                    margin-bottom: 4px;
                    font-style: italic;
                    font-weight: 500;
                }}
                
                .room-info {{
                    color: #7b1fa2;
                    font-size: 0.85em;
                    font-weight: bold;
                    margin-bottom: 3px;
                    background: linear-gradient(45deg, #f3e5f5, #fff3e0);
                    padding: 2px 6px;
                    border-radius: 6px;
                }}
                
                .class-type {{
                    color: #f57c00;
                    font-size: 0.8em;
                    font-weight: bold;
                    font-style: italic;
                    background: #fff3e0;
                    padding: 2px 6px;
                    border-radius: 6px;
                }}
                
                .no-class {{
                    color: #999;
                    font-size: 1.3em;
                    font-weight: bold;
                    opacity: 0.7;
                }}
                
                .footer {{
                    text-align: center;
                    padding: 30px;
                    background: linear-gradient(45deg, #f5f5f5, #e8e8e8);
                    color: #666;
                    font-size: 0.95em;
                    border-top: 3px solid #667eea;
                }}
                
                .generated-info {{
                    margin-top: 15px;
                    padding: 15px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 10px;
                    border-left: 4px solid #667eea;
                }}
                
                @media (max-width: 768px) {{
                    body {{
                        padding: 10px;
                    }}
                    
                    .header h1 {{
                        font-size: 2.2em;
                    }}
                    
                    .content {{
                        padding: 25px;
                    }}
                    
                    .section-container {{
                        padding: 20px;
                        margin-bottom: 30px;
                    }}
                    
                    .routine-table {{
                        font-size: 0.85em;
                    }}
                    
                    .schedule-cell {{
                        min-width: 160px;
                        max-width: 160px;
                        padding: 10px 8px;
                    }}
                    
                    .day-cell {{
                        min-width: 100px;
                        padding: 15px 10px;
                    }}
                }}
                
                .print-button {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: bold;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    transition: transform 0.3s ease;
                }}
                
                .print-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
                }}
                
                @media print {{
                    .print-button {{
                        display: none;
                    }}
                    
                    body {{
                        background: white;
                        padding: 0;
                    }}
                    
                    .container {{
                        box-shadow: none;
                        border-radius: 0;
                    }}
                }}
            </style>
        </head>
        <body>
            <button class="print-button" onclick="window.print()">🖨️ Print</button>
            
            <div class="container">
                <div class="header">
                    <h1>{metadata.get('university', 'Bangladesh University of Professionals')}</h1>
                    <div class="subtitle">{metadata.get('department', 'Computer Science & Engineering')}</div>
                    <div class="semester">Academic Class Routine - {metadata.get('semester', 'Spring 2025')}</div>
                </div>
                
                <div class="content">
                    <div class="info-section">
                        <h3 style="color: #2e7d32; margin-bottom: 20px; font-size: 1.5em;">📋 Schedule Information</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">🏫 Available Rooms:</div>
                                <div>{', '.join(data.get('available_rooms', []))}</div>
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
                                <div class="info-label">⏰ Break Time:</div>
                                <div>{schedule_config.get('break_time', '13:30 - 14:00')}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">📝 Last Updated:</div>
                                <div>{datetime.now().strftime('%B %d, %Y')}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">👨‍🏫 Total Faculty:</div>
                                <div>{len(data.get('faculty', []))} Professors</div>
                            </div>
                        </div>
                    </div>
        """
        
        # Add routine tables for each section (only process section-level data with dashes)
        for section_name, section_data in routine_data.items():
            # Skip batch-level data that doesn't contain '-'
            if '-' not in section_name:
                continue
                
            batch, section = section_name.split('-')
            html_content += f"""
                    <div class="section-container">
                        <h2 class="section-title">{batch} Section {section} - Class Routine</h2>
                        <div class="table-container">
                            <table class="routine-table">
                                <thead>
                                    <tr class="header-row">
                                        <th class="day-header">Days</th>
            """
            
            # Add time slot headers
            for slot in time_slots:
                html_content += f'<th class="time-header">{slot["slot"]}</th>'
            
            html_content += """
                                    </tr>
                                </thead>
                                <tbody>
            """
            
            # Add day rows
            days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
            for i, day in enumerate(days):
                row_class = "odd-row" if i % 2 == 0 else "even-row"
                html_content += f'<tr class="{row_class}">'
                html_content += f'<td class="day-cell">{day}</td>'
                
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
                    
                    html_content += f'<td class="schedule-cell">{cell_content}</td>'
                
                html_content += '</tr>'
            
            html_content += """
                                </tbody>
                            </table>
                        </div>
                    </div>
            """
        
        html_content += f"""
                </div>
                
                <div class="footer">
                    <div class="generated-info">
                        <p><strong>🎓 Enhanced Conflict-Free Scheduling System</strong></p>
                        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p>All classes scheduled considering faculty preferences and minimal gaps between classes</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write HTML file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Enhanced HTML routine generated successfully: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error generating HTML routine: {e}")
            return False

    def generate_enhanced_pdf(self, data_file, output_file):
        """Generate enhanced PDF routine with professional styling"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        try:
            doc = SimpleDocTemplate(output_file, pagesize=landscape(A4), 
                                   rightMargin=15, leftMargin=15, 
                                   topMargin=25, bottomMargin=25)
            
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
                               f"Academic Class Routine - {metadata.get('semester', 'Spring 2025')}", 
                               self.subtitle_style)
            story.append(subtitle)
            story.append(Spacer(1, 25))
            
            # Add routine tables for each section (only process section-level data with dashes)
            for section_name, section_data in routine_data.items():
                # Skip batch-level data that doesn't contain '-'
                if '-' not in section_name:
                    continue
                    
                batch, section = section_name.split('-')
                section_title = Paragraph(f"{batch} Section {section} - Class Routine", self.section_style)
                story.append(section_title)
                story.append(Spacer(1, 15))
                
                table = self.create_routine_table_for_section(section_name, section_data, time_slots)
                story.append(table)
                story.append(Spacer(1, 25))
                
                # Add page break except for the last section
                section_only_data = {k: v for k, v in routine_data.items() if '-' in k}
                sections = list(section_only_data.keys())
                if section_name != sections[-1]:
                    story.append(PageBreak())
            
            # Footer info
            footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | " \
                         f"Available Rooms: {', '.join(data.get('available_rooms', []))} | " \
                         f"Enhanced Conflict-Free Scheduling System"
            footer = Paragraph(footer_text, self.styles['Normal'])
            story.append(Spacer(1, 20))
            story.append(footer)
            
            doc.build(story)
            print(f"✅ Enhanced PDF routine generated successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF routine: {e}")
            return False

    def generate_all_formats(self, data_file, base_output_name):
        """Generate both HTML and PDF formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        html_file = f"{base_output_name}_{timestamp}.html"
        pdf_file = f"{base_output_name}_{timestamp}.pdf"
        
        html_success = self.create_enhanced_html_routine(data_file, html_file)
        pdf_success = self.generate_enhanced_pdf(data_file, pdf_file)
        
        if html_success and pdf_success:
            print(f"\n🎉 All formats generated successfully!")
            print(f"🌐 HTML: {html_file}")
            print(f"📄 PDF: {pdf_file}")
            return html_file, pdf_file
        else:
            print(f"\n⚠️ Some formats failed to generate")
            return None, None


def main():
    """Main function to demonstrate the generator"""
    generator = SampleRoutineGenerator()
    
    # Input and output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    data_file = os.path.join(project_root, "data", "sample_routine_data.json")
    output_dir = os.path.join(project_root, "output")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    base_output = os.path.join(output_dir, "enhanced_sample_routine")
    
    print("🚀 Generating Enhanced Sample-Based Academic Routine...")
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
