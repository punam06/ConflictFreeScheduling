#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Generator for Conflict-Free Scheduling System

This module provides PDF generation capabilities for academic schedules.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0
    name: str = ""
    room: str = ""


class PDFGenerator:
    """Basic PDF Generator for scheduling output"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_schedule_html(self, activities: List[Activity], 
                              title: str = "Schedule", 
                              filename: str = None) -> str:
        """
        Generate HTML schedule that can be converted to PDF
        
        Args:
            activities: List of scheduled activities
            title: Title for the schedule
            filename: Output filename (optional)
            
        Returns:
            Path to generated HTML file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"schedule_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Generate HTML content
        html_content = self._generate_html_content(activities, title)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML schedule generated: {filepath}")
        return filepath
    
    def _generate_html_content(self, activities: List[Activity], title: str) -> str:
        """Generate HTML content for the schedule"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            color: #7f8c8d;
            font-size: 1.1em;
            margin: 10px 0;
        }}
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .schedule-table th {{
            background-color: #3498db;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }}
        .schedule-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        .schedule-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .schedule-table tr:hover {{
            background-color: #e8f4f8;
        }}
        .summary {{
            margin-top: 30px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 8px;
        }}
        .summary h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .stat-item {{
            text-align: center;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .timestamp {{
            text-align: center;
            color: #95a5a6;
            font-size: 0.9em;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Conflict-Free Scheduling System</p>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    
    <table class="schedule-table">
        <thead>
            <tr>
                <th>Activity ID</th>
                <th>Activity Name</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Duration</th>
                <th>Weight/Credits</th>
                <th>Room</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add activity rows
        for activity in activities:
            duration = activity.end - activity.start
            room = activity.room if activity.room else "TBD"
            name = activity.name if activity.name else f"Activity {activity.id}"
            
            html += f"""
            <tr>
                <td>{activity.id}</td>
                <td>{name}</td>
                <td>{self._format_time(activity.start)}</td>
                <td>{self._format_time(activity.end)}</td>
                <td>{duration} min</td>
                <td>{activity.weight:.1f}</td>
                <td>{room}</td>
            </tr>
"""
        
        # Calculate statistics
        total_activities = len(activities)
        total_weight = sum(activity.weight for activity in activities)
        total_duration = sum(activity.end - activity.start for activity in activities)
        avg_duration = total_duration / total_activities if total_activities > 0 else 0
        
        html += f"""
        </tbody>
    </table>
    
    <div class="summary">
        <h3>Schedule Summary</h3>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{total_activities}</div>
                <div class="stat-label">Total Activities</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_weight:.1f}</div>
                <div class="stat-label">Total Credits/Weight</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_duration}</div>
                <div class="stat-label">Total Duration (min)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{avg_duration:.0f}</div>
                <div class="stat-label">Avg Duration (min)</div>
            </div>
        </div>
    </div>
    
    <div class="timestamp">
        Generated by Conflict-Free Scheduling System
    </div>
</body>
</html>
"""
        
        return html
    
    def _format_time(self, time_slot: int) -> str:
        """Convert time slot to readable format"""
        # Simple conversion - assumes each slot is 30 minutes starting from 8:00 AM
        base_hour = 8
        base_minute = 0
        
        total_minutes = base_minute + (time_slot * 30)
        hours = base_hour + (total_minutes // 60)
        minutes = total_minutes % 60
        
        # Handle 24-hour overflow
        hours = hours % 24
        
        # Convert to 12-hour format
        if hours == 0:
            hour_12 = 12
            am_pm = "AM"
        elif hours < 12:
            hour_12 = hours
            am_pm = "AM"
        elif hours == 12:
            hour_12 = 12
            am_pm = "PM"
        else:
            hour_12 = hours - 12
            am_pm = "PM"
        
        return f"{hour_12}:{minutes:02d} {am_pm}"


class AcademicPDFGenerator(PDFGenerator):
    """Enhanced PDF Generator for Academic Schedules"""
    
    def __init__(self):
        super().__init__()
        self.university_name = "Bangladesh University of Professionals"
        self.department_name = "Department of Computer Science & Engineering"
    
    def generate_academic_schedule(self, activities: List[Activity], 
                                  batch_code: str = "BCSE24",
                                  section: str = "A",
                                  semester: str = "Spring 2025") -> str:
        """
        Generate academic schedule with university branding
        
        Args:
            activities: List of scheduled activities
            batch_code: Batch code (e.g., BCSE24)
            section: Section name (A or B)
            semester: Semester information
            
        Returns:
            Path to generated HTML file
        """
        title = f"{batch_code} Section {section} - {semester} Schedule"
        html_filename = f"academic_schedule_{batch_code}_{section}.html"
        pdf_filename = f"academic_schedule_{batch_code}_{section}.pdf"
        
        # Generate enhanced HTML with academic styling
        html_filepath = os.path.join(self.output_dir, html_filename)
        pdf_filepath = os.path.join(self.output_dir, pdf_filename)
        
        html_content = self._generate_academic_html(activities, title, batch_code, section, semester)
        
        # Save HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Academic schedule generated: {html_filepath}")
        
        # Try to generate PDF using WeasyPrint
        try:
            import weasyprint
            html_doc = weasyprint.HTML(string=html_content, base_url='.')
            html_doc.write_pdf(pdf_filepath)
            print(f"✅ Academic PDF schedule generated: {pdf_filepath}")
            return pdf_filepath
        except ImportError:
            print("⚠️ WeasyPrint not available - trying ReportLab...")
        except Exception as e:
            print(f"⚠️ WeasyPrint PDF generation failed: {e} - trying ReportLab...")
        
        # Try ReportLab as fallback
        if self.generate_pdf_with_reportlab(activities, pdf_filepath, title, batch_code, section):
            print(f"✅ Academic PDF schedule generated with ReportLab: {pdf_filepath}")
            return pdf_filepath
        else:
            print("⚠️ PDF generation failed - HTML version available")
            return html_filepath
    
    def _generate_academic_html(self, activities: List[Activity], title: str, 
                               batch_code: str, section: str, semester: str) -> str:
        """Generate academic HTML with university branding"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            margin: 30px;
            line-height: 1.6;
            color: #2c3e50;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #27ae60;
            padding-bottom: 20px;
        }}
        .university-name {{
            font-size: 1.8em;
            font-weight: bold;
            color: #27ae60;
            margin: 0;
        }}
        .department-name {{
            font-size: 1.2em;
            color: #34495e;
            margin: 5px 0;
        }}
        .schedule-title {{
            font-size: 1.5em;
            color: #2c3e50;
            margin: 20px 0 10px 0;
            font-weight: bold;
        }}
        .schedule-info {{
            color: #7f8c8d;
            font-size: 1em;
        }}
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            font-size: 0.9em;
        }}
        .schedule-table th {{
            background-color: #27ae60;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #ddd;
        }}
        .schedule-table td {{
            padding: 10px 8px;
            border: 1px solid #ddd;
            text-align: center;
        }}
        .schedule-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .course-code {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .course-title {{
            color: #34495e;
        }}
        .credit-hours {{
            font-weight: bold;
            color: #27ae60;
        }}
        .footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 0.8em;
            color: #95a5a6;
            border-top: 1px solid #ecf0f1;
            padding-top: 20px;
        }}
        .signature-section {{
            margin-top: 40px;
            display: flex;
            justify-content: space-between;
        }}
        .signature-box {{
            text-align: center;
            width: 200px;
        }}
        .signature-line {{
            border-bottom: 1px solid #2c3e50;
            margin-bottom: 5px;
            height: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="university-name">{self.university_name}</div>
        <div class="department-name">{self.department_name}</div>
        <div class="schedule-title">{title}</div>
        <div class="schedule-info">Academic Year: 2024-25 | Generated: {datetime.now().strftime('%B %d, %Y')}</div>
    </div>
    
    <table class="schedule-table">
        <thead>
            <tr>
                <th>Course Code</th>
                <th>Course Title</th>
                <th>Credit Hours</th>
                <th>Class Type</th>
                <th>Time Slot</th>
                <th>Duration</th>
                <th>Room</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add activity rows
        for activity in activities:
            duration = activity.end - activity.start
            room = activity.room if activity.room else "TBD"
            course_code = f"CSE{activity.id:03d}"
            course_title = activity.name if activity.name else f"Course {activity.id}"
            class_type = "Lab" if activity.weight < 2 else "Theory"
            
            html += f"""
            <tr>
                <td class="course-code">{course_code}</td>
                <td class="course-title">{course_title}</td>
                <td class="credit-hours">{activity.weight:.1f}</td>
                <td>{class_type}</td>
                <td>{self._format_time(activity.start)} - {self._format_time(activity.end)}</td>
                <td>{duration} min</td>
                <td>{room}</td>
            </tr>
"""
        
        total_credits = sum(activity.weight for activity in activities)
        
        html += f"""
        </tbody>
    </table>
    
    <div style="margin-top: 30px;">
        <strong>Total Credit Hours: {total_credits:.1f}</strong>
    </div>
    
    <div class="signature-section">
        <div class="signature-box">
            <div class="signature-line"></div>
            <div>Course Coordinator</div>
        </div>
        <div class="signature-box">
            <div class="signature-line"></div>
            <div>Head of Department</div>
        </div>
        <div class="signature-box">
            <div class="signature-line"></div>
            <div>Dean, Faculty of Engineering</div>
        </div>
    </div>
    
    <div class="footer">
        <p>This is a computer-generated schedule. For any discrepancies, please contact the CSE Department office.</p>
        <p>Bangladesh University of Professionals | Mirpur Cantonment, Dhaka-1216</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_pdf_with_reportlab(self, activities: List[Activity], 
                                   pdf_filepath: str, title: str, 
                                   batch_code: str, section: str) -> bool:
        """
        Generate PDF using ReportLab as fallback
        
        Args:
            activities: List of scheduled activities
            pdf_filepath: Output PDF file path
            title: Schedule title
            batch_code: Batch code
            section: Section name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            
            # Create PDF document
            doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.darkblue,
                alignment=1,  # Center alignment
                spaceAfter=20
            )
            
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.black,
                alignment=1,
                spaceAfter=10
            )
            
            # Add title and header
            story.append(Paragraph("Bangladesh University of Professionals", title_style))
            story.append(Paragraph("Department of Computer Science & Engineering", header_style))
            story.append(Paragraph(f"Academic Schedule - {batch_code} Section {section}", header_style))
            story.append(Spacer(1, 20))
            
            # Create table data
            data = [['ID', 'Course Name', 'Start Time', 'End Time', 'Duration', 'Credits', 'Room']]
            
            for activity in activities:
                start_hours = activity.start // 60
                start_mins = activity.start % 60
                end_hours = activity.end // 60
                end_mins = activity.end % 60
                duration = activity.end - activity.start
                
                data.append([
                    str(activity.id),
                    activity.name or 'N/A',
                    f"{start_hours:02d}:{start_mins:02d}",
                    f"{end_hours:02d}:{end_mins:02d}",
                    f"{duration} min",
                    str(activity.weight),
                    activity.room or 'TBD'
                ])
            
            # Create and style table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
            
            # Add summary
            total_activities = len(activities)
            total_weight = sum(activity.weight for activity in activities)
            story.append(Paragraph(f"Total Activities: {total_activities}", styles['Normal']))
            story.append(Paragraph(f"Total Credits: {total_weight}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except ImportError:
            print("❌ ReportLab not available")
            return False
        except Exception as e:
            print(f"❌ ReportLab PDF generation failed: {e}")
            return False
