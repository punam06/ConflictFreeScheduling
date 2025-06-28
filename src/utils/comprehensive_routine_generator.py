#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Academic Routine Generator
Generates comprehensive academic routines for all batches and sections
with proper time slots and attractive table formatting
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


class ComprehensiveRoutineGenerator:
    """Generate comprehensive academic routines with attractive table formatting"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        self.batch_style = ParagraphStyle(
            'BatchStyle',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.darkred,
            backColor=colors.lightgrey
        )

    def load_comprehensive_data(self, file_path: str) -> Dict[str, Any]:
        """Load comprehensive routine data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

    def get_faculty_name(self, faculty_id: int, faculty_list: List[Dict]) -> str:
        """Get faculty name by ID"""
        for faculty in faculty_list:
            if faculty['id'] == faculty_id:
                return faculty['name']
        return "TBA"

    def get_time_slot_info(self, slot_id: int, time_slots: List[Dict]) -> Dict:
        """Get time slot information by ID"""
        for slot in time_slots:
            if slot['id'] == slot_id:
                return slot
        return {"start": "TBA", "end": "TBA"}

    def create_weekly_schedule_table(self, batch_data: Dict, faculty_list: List[Dict], 
                                   time_slots: List[Dict], days: List[str]) -> Table:
        """Create a weekly schedule table for a batch and section"""
        
        # Create header row
        header = ['Time'] + days
        
        # Create time slot rows
        data = [header]
        
        for slot in time_slots:
            row = [f"{slot['start']}-{slot['end']}"]
            
            for day in days:
                # Find course for this day and time slot
                course_found = None
                for course in batch_data['courses']:
                    if course['day'] == day and course['time_slot'] == slot['id']:
                        faculty_name = self.get_faculty_name(course['faculty_id'], faculty_list)
                        course_info = f"{course['id']}\n{course['name']}\n{faculty_name}\n{course['room']}"
                        course_found = course_info
                        break
                
                row.append(course_found if course_found else '')
            
            data.append(row)
        
        # Create table with styling
        table = Table(data, colWidths=[1.2*inch] + [1.4*inch]*5)
        
        # Apply table styling
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Time column styling
            ('BACKGROUND', (0, 1), (0, -1), colors.lightblue),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 9),
            
            # Cell styling
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.lightgrey]),
            
            # Border styling
            ('LINEWIDTH', (0, 0), (-1, -1), 0.5),
            ('LINEBEFORE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEAFTER', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        return table

    def generate_comprehensive_routine_pdf(self, data_file: str, output_file: str = None) -> str:
        """Generate comprehensive routine PDF for all batches and sections"""
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/comprehensive_academic_routine_{timestamp}.pdf"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Load data
        data = self.load_comprehensive_data(data_file)
        if not data:
            print("❌ Failed to load routine data")
            return None
            
        # Create PDF document in landscape mode
        doc = SimpleDocTemplate(output_file, pagesize=landscape(A4),
                              rightMargin=0.5*inch, leftMargin=0.5*inch,
                              topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        
        # Add main title
        title = Paragraph(f"<b>{data['metadata']['university']}</b>", self.title_style)
        story.append(title)
        
        subtitle = Paragraph(f"Department of {data['metadata']['department']}", self.subtitle_style)
        story.append(subtitle)
        
        semester_info = Paragraph(f"Academic Routine - {data['metadata']['semester']} ({data['metadata']['academic_year']})", self.subtitle_style)
        story.append(semester_info)
        
        story.append(Spacer(1, 20))
        
        # Group courses by batch and section
        batches_data = {}
        for course_group in data['courses']:
            batch_code = course_group['batch']
            section = course_group['section']
            
            if batch_code not in batches_data:
                batches_data[batch_code] = {}
            
            batches_data[batch_code][section] = course_group
        
        # Generate routine for each batch and section
        for batch_code in sorted(batches_data.keys()):
            for section in sorted(batches_data[batch_code].keys()):
                batch_data = batches_data[batch_code][section]
                
                # Add batch and section header
                batch_header = Paragraph(f"<b>Batch: {batch_code} - Section: {section}</b>", self.batch_style)
                story.append(batch_header)
                story.append(Spacer(1, 10))
                
                # Create and add weekly schedule table
                table = self.create_weekly_schedule_table(
                    batch_data, 
                    data['faculty'], 
                    data['time_slots'], 
                    data['schedule_config']['days']
                )
                story.append(table)
                story.append(Spacer(1, 20))
                
                # Add page break between batches (except for the last one)
                if not (batch_code == max(batches_data.keys()) and section == max(batches_data[batch_code].keys())):
                    story.append(PageBreak())
        
        # Add footer information
        story.append(Spacer(1, 30))
        footer_info = [
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            f"Total Batches: {len(batches_data)}",
            f"Schedule: {data['schedule_config']['start_time']} - {data['schedule_config']['end_time']} (Break: {data['schedule_config']['break_time']['start']} - {data['schedule_config']['break_time']['end']})",
            "Theory Classes: 1.5 hours | Lab Classes: 3 hours"
        ]
        
        for info in footer_info:
            footer_para = Paragraph(f"<i>{info}</i>", self.styles['Normal'])
            story.append(footer_para)
            story.append(Spacer(1, 5))
        
        # Build PDF
        try:
            doc.build(story)
            print(f"✅ Comprehensive routine PDF generated: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return None

    def generate_html_routine(self, data_file: str, output_file: str = None) -> str:
        """Generate comprehensive routine HTML with attractive styling"""
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/comprehensive_academic_routine_{timestamp}.html"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Load data
        data = self.load_comprehensive_data(data_file)
        if not data:
            print("❌ Failed to load routine data")
            return None
        
        # Generate HTML content
        html_content = self.create_html_content(data)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Comprehensive routine HTML generated: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Error generating HTML: {e}")
            return None

    def create_html_content(self, data: Dict[str, Any]) -> str:
        """Create HTML content for the comprehensive routine"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Academic Routine - {data['metadata']['semester']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
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
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header h2 {{
            font-size: 1.5em;
            margin-bottom: 5px;
            opacity: 0.9;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .batch-section {{
            margin-bottom: 40px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .batch-header {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 15px 20px;
            font-size: 1.4em;
            font-weight: bold;
            text-align: center;
        }}
        
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        
        .schedule-table th {{
            background: linear-gradient(135deg, #4834d4 0%, #686de0 100%);
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #ddd;
        }}
        
        .schedule-table td {{
            padding: 10px 8px;
            text-align: center;
            border: 1px solid #ddd;
            vertical-align: middle;
            height: 80px;
        }}
        
        .time-slot {{
            background: linear-gradient(135deg, #3742fa 0%, #2f3542 100%);
            color: white;
            font-weight: bold;
            font-size: 0.95em;
        }}
        
        .course-cell {{
            background: #f8f9fa;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .course-cell:hover {{
            background: #e3f2fd;
            transform: scale(1.02);
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        
        .course-code {{
            font-weight: bold;
            color: #1e3c72;
            font-size: 0.9em;
        }}
        
        .course-name {{
            color: #333;
            font-size: 0.8em;
            margin: 2px 0;
        }}
        
        .faculty-name {{
            color: #666;
            font-size: 0.75em;
            font-style: italic;
        }}
        
        .room-info {{
            color: #e74c3c;
            font-size: 0.7em;
            font-weight: bold;
            margin-top: 2px;
        }}
        
        .empty-cell {{
            background: #fafafa;
            color: #999;
        }}
        
        .schedule-table tr:nth-child(even) .course-cell {{
            background: #ffffff;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
        
        .footer p {{
            margin: 5px 0;
            color: #666;
        }}
        
        .schedule-info {{
            background: linear-gradient(135deg, #00d2d3 0%, #54a0ff 100%);
            color: white;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            text-align: center;
        }}
        
        .break-info {{
            background: #f39c12;
            color: white;
            padding: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 10px;
            }}
            
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .schedule-table {{
                font-size: 0.8em;
            }}
            
            .schedule-table td {{
                height: 60px;
                padding: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{data['metadata']['university']}</h1>
            <h2>Department of {data['metadata']['department']}</h2>
            <p>Academic Routine - {data['metadata']['semester']} ({data['metadata']['academic_year']})</p>
        </div>
        
        <div class="content">
            <div class="schedule-info">
                <p><strong>Class Schedule:</strong> {data['schedule_config']['start_time']} - {data['schedule_config']['end_time']}</p>
                <p><strong>Break Time:</strong> {data['schedule_config']['break_time']['start']} - {data['schedule_config']['break_time']['end']}</p>
                <p><strong>Theory Classes:</strong> 1.5 hours | <strong>Lab Classes:</strong> 3 hours</p>
            </div>
"""
        
        # Group courses by batch and section
        batches_data = {}
        for course_group in data['courses']:
            batch_code = course_group['batch']
            section = course_group['section']
            
            if batch_code not in batches_data:
                batches_data[batch_code] = {}
            
            batches_data[batch_code][section] = course_group
        
        # Generate HTML for each batch and section
        for batch_code in sorted(batches_data.keys()):
            for section in sorted(batches_data[batch_code].keys()):
                batch_data = batches_data[batch_code][section]
                
                html += f"""
            <div class="batch-section">
                <div class="batch-header">
                    Batch: {batch_code} - Section: {section}
                </div>
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Time Slot</th>
"""
                
                # Add day headers
                for day in data['schedule_config']['days']:
                    html += f"<th>{day}</th>"
                
                html += """
                        </tr>
                    </thead>
                    <tbody>
"""
                
                # Add time slot rows
                for slot in data['time_slots']:
                    html += f"""
                        <tr>
                            <td class="time-slot">{slot['start']}<br>{slot['end']}</td>
"""
                    
                    # Add course cells for each day
                    for day in data['schedule_config']['days']:
                        course_found = None
                        for course in batch_data['courses']:
                            if course['day'] == day and course['time_slot'] == slot['id']:
                                faculty_name = self.get_faculty_name(course['faculty_id'], data['faculty'])
                                course_found = course
                                break
                        
                        if course_found:
                            html += f"""
                            <td class="course-cell">
                                <div class="course-code">{course_found['id']}</div>
                                <div class="course-name">{course_found['name']}</div>
                                <div class="faculty-name">{faculty_name}</div>
                                <div class="room-info">{course_found['room']}</div>
                            </td>
"""
                        else:
                            html += '<td class="empty-cell">-</td>'
                    
                    html += "</tr>"
                    
                    # Add break row after slot 3 (13:30)
                    if slot['id'] == 3:
                        html += f"""
                        <tr>
                            <td class="break-info">BREAK</td>
                            <td class="break-info" colspan="{len(data['schedule_config']['days'])}">
                                Lunch Break ({data['schedule_config']['break_time']['start']} - {data['schedule_config']['break_time']['end']})
                            </td>
                        </tr>
"""
                
                html += """
                    </tbody>
                </table>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            <p><strong>Generated on:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p><strong>Total Batches:</strong> {len(batches_data)} | <strong>Days:</strong> {', '.join(data['schedule_config']['days'])}</p>
            <p><em>This is an automatically generated academic routine. For any changes, please contact the academic office.</em></p>
        </div>
    </div>
</body>
</html>
"""
        
        return html


def main():
    """Main function to generate comprehensive routine"""
    generator = ComprehensiveRoutineGenerator()
    
    # Generate both PDF and HTML
    data_file = "data/comprehensive_routine_data.json"
    
    print("🔄 Generating comprehensive academic routine...")
    
    # Generate PDF
    pdf_file = generator.generate_comprehensive_routine_pdf(data_file)
    
    # Generate HTML
    html_file = generator.generate_html_routine(data_file)
    
    if pdf_file and html_file:
        print(f"\n✅ Comprehensive routine generation complete!")
        print(f"📄 PDF: {pdf_file}")
        print(f"🌐 HTML: {html_file}")
    else:
        print("❌ Failed to generate comprehensive routine")


if __name__ == "__main__":
    main()
