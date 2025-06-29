#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive Single Table Routine Generator
Generates a single comprehensive table showing all batches and sections together
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER


class ComprehensiveSingleTableGenerator:
    """Generate comprehensive routine with all batches/sections in a single table"""
    
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

    def load_routine_data(self, data_file):
        """Load routine data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading routine data: {e}")
            return None

    def create_comprehensive_html_table(self, data_file, output_file):
        """Create comprehensive HTML with single table for all batches/sections"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        metadata = data.get('metadata', {})
        schedule_config = data.get('schedule_config', {})
        time_slots = schedule_config.get('time_slots', [])
        routine_data = data.get('routine', {})
        
        # Filter only section-level data (contains '-')
        section_data = {k: v for k, v in routine_data.items() if '-' in k}
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Comprehensive Class Routine - {metadata.get('semester', 'Spring 2025')}</title>
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
                    max-width: 1800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.98);
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
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
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
                }}
                
                .header .subtitle {{
                    font-size: 1.3em;
                    opacity: 0.95;
                }}
                
                .content {{
                    padding: 30px;
                }}
                
                .comprehensive-table-container {{
                    overflow-x: auto;
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    background: white;
                    margin: 20px 0;
                }}
                
                .comprehensive-table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    font-size: 0.85em;
                }}
                
                .header-row {{
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    color: white;
                }}
                
                .time-header {{
                    padding: 15px 8px;
                    text-align: center;
                    font-weight: bold;
                    border: 1px solid #ddd;
                    min-width: 120px;
                }}
                
                .day-header {{
                    background: linear-gradient(45deg, #1a237e, #3949ab);
                    padding: 15px 10px;
                    text-align: center;
                    font-weight: bold;
                    min-width: 100px;
                }}
                
                .day-cell {{
                    background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
                    color: #1565c0;
                    font-weight: bold;
                    text-align: center;
                    padding: 15px 10px;
                    border: 1px solid #ddd;
                    vertical-align: top;
                }}
                
                .schedule-cell {{
                    padding: 8px 6px;
                    text-align: left;
                    vertical-align: top;
                    border: 1px solid #ddd;
                    min-width: 120px;
                    font-size: 0.8em;
                }}
                
                .batch-section {{
                    margin-bottom: 8px;
                    padding: 6px;
                    background: linear-gradient(135deg, #f0f8f0, #e8f5e8);
                    border-radius: 6px;
                    border-left: 3px solid #4caf50;
                }}
                
                .batch-name {{
                    font-weight: bold;
                    color: #1565c0;
                    font-size: 0.9em;
                    margin-bottom: 3px;
                }}
                
                .course-code {{
                    font-weight: bold;
                    color: #2e7d32;
                    font-size: 0.85em;
                }}
                
                .course-name {{
                    color: #424242;
                    font-size: 0.8em;
                    margin: 2px 0;
                }}
                
                .faculty-name {{
                    color: #d32f2f;
                    font-size: 0.75em;
                    font-style: italic;
                }}
                
                .room-info {{
                    color: #7b1fa2;
                    font-size: 0.75em;
                    font-weight: bold;
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
                    <div class="subtitle">Comprehensive Class Routine - {metadata.get('semester', 'Spring 2025')}</div>
                </div>
                
                <div class="content">
                    <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">
                        📋 All Batches & Sections Combined Schedule
                    </h2>
                    
                    <div class="comprehensive-table-container">
                        <table class="comprehensive-table">
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
        
        # Add day rows with all sections combined
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        for day in days:
            html_content += f'<tr><td class="day-cell">{day}</td>'
            
            for slot in time_slots:
                slot_time = slot["slot"]
                cell_content = ""
                
                # Collect all classes for this day/time across all sections
                for section_name, section_schedule in section_data.items():
                    day_schedule = section_schedule.get(day, {})
                    class_info = day_schedule.get(slot_time, {})
                    
                    if class_info:
                        batch, section = section_name.split('-')
                        course_code = class_info.get('course', '')
                        course_name = class_info.get('name', '')
                        faculty = class_info.get('faculty', '')
                        room = class_info.get('room', '')
                        
                        cell_content += f"""
                            <div class="batch-section">
                                <div class="batch-name">{batch} Sec {section}</div>
                                <div class="course-code">{course_code}</div>
                                <div class="course-name">{course_name}</div>
                                <div class="faculty-name">{faculty}</div>
                                <div class="room-info">Room: {room}</div>
                            </div>
                        """
                
                if not cell_content:
                    cell_content = '<div style="text-align: center; color: #999;">-</div>'
                
                html_content += f'<td class="schedule-cell">{cell_content}</td>'
            
            html_content += '</tr>'
        
        html_content += f"""
                            </tbody>
                        </table>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
                        <p><strong>🎓 Enhanced Conflict-Free Scheduling System</strong></p>
                        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p>Comprehensive schedule showing all {len(section_data)} sections in a single view</p>
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
            print(f"✅ Comprehensive single-table HTML generated: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error generating comprehensive HTML: {e}")
            return False

    def create_comprehensive_pdf(self, data_file, output_file):
        """Create comprehensive PDF with single table"""
        data = self.load_routine_data(data_file)
        if not data:
            return False
        
        try:
            doc = SimpleDocTemplate(output_file, pagesize=landscape(A4), 
                                   rightMargin=10, leftMargin=10, 
                                   topMargin=20, bottomMargin=20)
            
            story = []
            metadata = data.get('metadata', {})
            schedule_config = data.get('schedule_config', {})
            time_slots = schedule_config.get('time_slots', [])
            routine_data = data.get('routine', {})
            
            # Filter only section-level data
            section_data = {k: v for k, v in routine_data.items() if '-' in k}
            
            # Title
            title = Paragraph(f"{metadata.get('university', 'Bangladesh University of Professionals')}", 
                            self.title_style)
            story.append(title)
            
            subtitle = Paragraph(f"{metadata.get('department', 'Computer Science & Engineering')}<br/>"
                               f"Comprehensive Class Routine - {metadata.get('semester', 'Spring 2025')}", 
                               self.subtitle_style)
            story.append(subtitle)
            story.append(Spacer(1, 20))
            
            # Create comprehensive table
            header = ["Days"] + [slot["slot"] for slot in time_slots]
            table_data = [header]
            
            days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
            for day in days:
                row = [day]
                
                for slot in time_slots:
                    slot_time = slot["slot"]
                    cell_content = []
                    
                    # Collect all classes for this day/time
                    for section_name, section_schedule in section_data.items():
                        day_schedule = section_schedule.get(day, {})
                        class_info = day_schedule.get(slot_time, {})
                        
                        if class_info:
                            batch, section = section_name.split('-')
                            course_code = class_info.get('course', '')
                            course_name = class_info.get('name', '')
                            faculty = class_info.get('faculty', '')
                            room = class_info.get('room', '')
                            
                            cell_text = f"{batch} Sec {section}\n{course_code}\n{course_name}\n{faculty}\nRoom: {room}"
                            cell_content.append(cell_text)
                    
                    if cell_content:
                        row.append("\n\n".join(cell_content))
                    else:
                        row.append("-")
                
                table_data.append(row)
            
            # Create table with dynamic column widths
            col_width = 1.8 * inch
            day_col_width = 1.0 * inch
            table = Table(table_data, colWidths=[day_col_width] + [col_width] * len(time_slots))
            
            # Enhanced table styling
            table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.7)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                
                # Days column styling
                ('BACKGROUND', (0, 1), (0, -1), colors.Color(0.8, 0.9, 1.0)),
                ('TEXTCOLOR', (0, 1), (0, -1), colors.Color(0.2, 0.3, 0.7)),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (0, -1), 9),
                ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),
                
                # Data cells styling
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 1), (-1, -1), 7),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.3, 0.3, 0.3)),
                
                # Alternating row colors
                ('BACKGROUND', (1, 1), (-1, 1), colors.Color(0.95, 0.98, 1.0)),
                ('BACKGROUND', (1, 3), (-1, 3), colors.Color(0.95, 0.98, 1.0)),
                ('BACKGROUND', (1, 5), (-1, 5), colors.Color(0.95, 0.98, 1.0)),
            ]))
            
            story.append(table)
            
            # Footer
            footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | " \
                         f"Total Sections: {len(section_data)} | " \
                         f"Enhanced Conflict-Free Scheduling System"
            footer = Paragraph(footer_text, self.styles['Normal'])
            story.append(Spacer(1, 15))
            story.append(footer)
            
            doc.build(story)
            print(f"✅ Comprehensive single-table PDF generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating comprehensive PDF: {e}")
            return False

    def generate_comprehensive_routine(self, data_file, base_output_name):
        """Generate comprehensive routine with single table containing all batches/sections"""
        return self.generate_all_formats(data_file, base_output_name)

    def generate_all_formats(self, data_file, base_output_name):
        """Generate both HTML and PDF formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        html_file = f"{base_output_name}_{timestamp}.html"
        pdf_file = f"{base_output_name}_{timestamp}.pdf"
        
        html_success = self.create_comprehensive_html_table(data_file, html_file)
        pdf_success = self.create_comprehensive_pdf(data_file, pdf_file)
        
        if html_success and pdf_success:
            print(f"\n🎉 Comprehensive single-table formats generated!")
            print(f"🌐 HTML: {html_file}")
            print(f"📄 PDF: {pdf_file}")
            return html_file, pdf_file
        else:
            print(f"\n⚠️ Some comprehensive formats failed to generate")
            return None, None
