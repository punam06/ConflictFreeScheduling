#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced PDF Generator for Conflict-Free Scheduling System

This module provides enhanced PDF generation capabilities for academic schedules.
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
    faculty: str = ""
    course_code: str = ""


@dataclass
class Faculty:
    """Class representing faculty information"""
    name: str
    department: str = ""
    email: str = ""
    available_times: List[int] = None
    courses: List[str] = None


class EnhancedPDFGenerator:
    """Enhanced PDF Generator with comprehensive routine options"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.university_name = "Bangladesh University of Professionals"
        self.department_name = "Department of Computer Science & Engineering"
        self.faculties = []
        self.rooms = ["CSE-401", "CSE-402", "CSE-403", "CSE-404", "CSE-405", "CSE-Lab1", "CSE-Lab2"]
    
    def add_faculty(self, faculty: Faculty):
        """Add faculty member"""
        self.faculties.append(faculty)
    
    def allocate_room(self, activities: List[Activity]) -> List[Activity]:
        """Automatically allocate rooms to activities"""
        room_schedule = {room: [] for room in self.rooms}
        
        for activity in activities:
            if not activity.room:
                # Find available room
                for room in self.rooms:
                    room_busy = False
                    for scheduled_time in room_schedule[room]:
                        if not (activity.end <= scheduled_time[0] or activity.start >= scheduled_time[1]):
                            room_busy = True
                            break
                    
                    if not room_busy:
                        activity.room = room
                        room_schedule[room].append((activity.start, activity.end))
                        break
        
        return activities
    
    def generate_comprehensive_routine(self, all_activities: Dict[str, List[Activity]], 
                                     semester: str = "Spring 2025") -> str:
        """Generate comprehensive routine for all batches and sections"""
        
        title = f"Comprehensive Academic Routine - {semester}"
        html_filename = f"comprehensive_routine_{semester.replace(' ', '_').lower()}.html"
        pdf_filename = f"comprehensive_routine_{semester.replace(' ', '_').lower()}.pdf"
        
        html_filepath = os.path.join(self.output_dir, html_filename)
        pdf_filepath = os.path.join(self.output_dir, pdf_filename)
        
        html_content = self._generate_comprehensive_html(all_activities, title, semester)
        
        # Save HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Comprehensive routine generated: {html_filepath}")
        
        # Try to generate PDF
        return self._generate_pdf_from_html(html_content, pdf_filepath, html_filepath)
    
    def generate_batch_routine(self, activities: List[Activity], batch_code: str,
                              semester: str = "Spring 2025") -> str:
        """Generate routine for specific batch (all sections)"""
        
        title = f"{batch_code} Batch Routine - {semester}"
        html_filename = f"batch_routine_{batch_code}_{semester.replace(' ', '_').lower()}.html"
        pdf_filename = f"batch_routine_{batch_code}_{semester.replace(' ', '_').lower()}.pdf"
        
        html_filepath = os.path.join(self.output_dir, html_filename)
        pdf_filepath = os.path.join(self.output_dir, pdf_filename)
        
        html_content = self._generate_enhanced_html(activities, title, batch_code, "All Sections", semester)
        
        # Save HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Batch routine generated: {html_filepath}")
        
        # Try to generate PDF
        return self._generate_pdf_from_html(html_content, pdf_filepath, html_filepath)
    
    def generate_section_routine(self, activities: List[Activity], batch_code: str,
                               section: str, semester: str = "Spring 2025") -> str:
        """Generate routine for specific section"""
        
        title = f"{batch_code} Section {section} - {semester}"
        html_filename = f"section_routine_{batch_code}_{section}_{semester.replace(' ', '_').lower()}.html"
        pdf_filename = f"section_routine_{batch_code}_{section}_{semester.replace(' ', '_').lower()}.pdf"
        
        html_filepath = os.path.join(self.output_dir, html_filename)
        pdf_filepath = os.path.join(self.output_dir, pdf_filename)
        
        html_content = self._generate_enhanced_html(activities, title, batch_code, section, semester)
        
        # Save HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Section routine generated: {html_filepath}")
        
        # Try to generate PDF
        return self._generate_pdf_from_html(html_content, pdf_filepath, html_filepath)
    
    def _generate_enhanced_html(self, activities: List[Activity], title: str, 
                               batch_code: str, section: str, semester: str) -> str:
        """Generate enhanced HTML with eye-catching design"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Playfair+Display:wght@400;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 25px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            text-align: center;
            padding: 50px 30px;
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
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite alternate;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(0.8); opacity: 0.5; }}
            100% {{ transform: scale(1.2); opacity: 0.8; }}
        }}
        
        .university-logo {{
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            border-radius: 50%;
            margin: 0 auto 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5em;
            font-weight: bold;
            position: relative;
            z-index: 2;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .university-name {{
            font-family: 'Playfair Display', serif;
            font-size: 2.8em;
            font-weight: 700;
            margin: 0;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            position: relative;
            z-index: 2;
        }}
        
        .department-name {{
            font-size: 1.4em;
            margin: 15px 0;
            opacity: 0.95;
            font-weight: 300;
            position: relative;
            z-index: 2;
        }}
        
        .schedule-title {{
            font-size: 2.2em;
            margin: 25px 0 15px 0;
            font-weight: 600;
            background: rgba(255,255,255,0.15);
            padding: 20px 40px;
            border-radius: 60px;
            display: inline-block;
            position: relative;
            z-index: 2;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        .schedule-info {{
            font-size: 1.2em;
            opacity: 0.9;
            position: relative;
            z-index: 2;
        }}
        
        .print-date {{
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            display: inline-block;
            margin: 25px 0;
            font-weight: 600;
            font-size: 1.1em;
            position: relative;
            z-index: 2;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        .content {{
            padding: 50px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transform: translateY(0);
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            font-size: 1em;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }}
        
        .schedule-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 20px;
            text-align: center;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.9em;
            border: none;
        }}
        
        .schedule-table td {{
            padding: 20px 15px;
            text-align: center;
            border-bottom: 1px solid #e8ecf4;
            transition: all 0.3s ease;
            vertical-align: middle;
        }}
        
        .schedule-table tr:nth-child(even) {{
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        }}
        
        .schedule-table tr:hover {{
            background: linear-gradient(135deg, #e8f2ff 0%, #dae8ff 100%);
            transform: scale(1.02);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .course-code {{
            font-weight: 700;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.2em;
        }}
        
        .course-title {{
            color: #34495e;
            font-weight: 500;
            font-size: 1.1em;
        }}
        
        .faculty-name {{
            color: #8e44ad;
            font-weight: 600;
            font-style: italic;
            background: #f3e5f5;
            padding: 10px 15px;
            border-radius: 25px;
            display: inline-block;
        }}
        
        .credit-hours {{
            font-weight: 700;
            color: #27ae60;
            background: linear-gradient(135deg, #a8e6cf, #88d8a3);
            padding: 12px 18px;
            border-radius: 25px;
            display: inline-block;
            font-size: 1.1em;
        }}
        
        .time-slot {{
            background: linear-gradient(135deg, #ffeaa7, #fab1a0);
            padding: 12px 18px;
            border-radius: 25px;
            font-weight: 600;
            color: #2d3436;
            font-size: 1.1em;
        }}
        
        .room-info {{
            background: linear-gradient(135deg, #81ecec, #74b9ff);
            color: #2d3436;
            padding: 12px 18px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .class-type {{
            background: linear-gradient(135deg, #fd79a8, #fdcb6e);
            color: #2d3436;
            padding: 12px 18px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .summary-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            border-radius: 25px;
            margin-top: 50px;
            text-align: center;
        }}
        
        .total-credits {{
            font-size: 2.5em;
            font-weight: 700;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }}
        
        .signature-section {{
            margin-top: 60px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            padding: 40px 0;
        }}
        
        .signature-box {{
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .signature-box:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }}
        
        .signature-line {{
            border-bottom: 3px solid rgba(255,255,255,0.8);
            margin-bottom: 20px;
            height: 50px;
        }}
        
        .signature-title {{
            font-weight: 600;
            font-size: 1.2em;
        }}
        
        .footer {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            text-align: center;
            padding: 40px;
            font-size: 1em;
        }}
        
        .footer p {{
            margin: 8px 0;
            opacity: 0.9;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
            .header::before {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="university-logo">BUP</div>
            <div class="university-name">{self.university_name}</div>
            <div class="department-name">{self.department_name}</div>
            <div class="schedule-title">{title}</div>
            <div class="schedule-info">Academic Year: 2024-25</div>
            <div class="print-date">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="content">"""
        
        # Add statistics
        total_activities = len(activities)
        total_credits = sum(activity.weight for activity in activities)
        unique_faculties = len(set(activity.faculty for activity in activities if activity.faculty))
        unique_rooms = len(set(activity.room for activity in activities if activity.room))
        
        html += f"""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_activities}</div>
                    <div class="stat-label">Total Courses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_credits:.1f}</div>
                    <div class="stat-label">Total Credits</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{unique_faculties}</div>
                    <div class="stat-label">Faculty Members</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{unique_rooms}</div>
                    <div class="stat-label">Rooms Assigned</div>
                </div>
            </div>
            
            <table class="schedule-table">
                <thead>
                    <tr>
                        <th>Course Code</th>
                        <th>Course Title</th>
                        <th>Faculty Name</th>
                        <th>Credit Hours</th>
                        <th>Class Type</th>
                        <th>Time Slot</th>
                        <th>Duration</th>
                        <th>Room</th>
                    </tr>
                </thead>
                <tbody>"""
        
        # Add activity rows
        for activity in activities:
            duration = activity.end - activity.start
            room = activity.room if activity.room else "TBD"
            course_code = activity.course_code if activity.course_code else f"CSE{activity.id:03d}"
            course_title = activity.name if activity.name else f"Course {activity.id}"
            faculty_name = activity.faculty if activity.faculty else "TBA"
            class_type = "Lab" if activity.weight < 2 else "Theory"
            
            html += f"""
                <tr>
                    <td><span class="course-code">{course_code}</span></td>
                    <td><span class="course-title">{course_title}</span></td>
                    <td><span class="faculty-name">{faculty_name}</span></td>
                    <td><span class="credit-hours">{activity.weight:.1f}</span></td>
                    <td><span class="class-type">{class_type}</span></td>
                    <td><span class="time-slot">{self._format_time(activity.start)} - {self._format_time(activity.end)}</span></td>
                    <td>{duration} min</td>
                    <td><span class="room-info">{room}</span></td>
                </tr>"""
        
        html += f"""
                </tbody>
            </table>
            
            <div class="summary-section">
                <div class="total-credits">{total_credits:.1f} Total Credit Hours</div>
                <p>Successfully scheduled {total_activities} courses with {unique_faculties} faculty members across {unique_rooms} rooms</p>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-title">Course Coordinator</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-title">Head of Department</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-title">Dean, Faculty of Engineering</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-title">Registrar</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>This is a computer-generated schedule. For any discrepancies, please contact the CSE Department office.</strong></p>
            <p>{self.university_name} | Mirpur Cantonment, Dhaka-1216</p>
            <p>Email: cse@bup.edu.bd | Phone: +880-2-8000-1234</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_comprehensive_html(self, all_activities: Dict[str, List[Activity]], 
                                   title: str, semester: str) -> str:
        """Generate comprehensive HTML for all batches"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Playfair+Display:wght@400;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 25px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            text-align: center;
            padding: 60px 30px;
            position: relative;
        }}
        
        .university-name {{
            font-family: 'Playfair Display', serif;
            font-size: 3.2em;
            font-weight: 700;
            margin: 20px 0;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        }}
        
        .title {{
            font-size: 2.5em;
            font-weight: 600;
            background: rgba(255,255,255,0.15);
            padding: 25px 50px;
            border-radius: 60px;
            display: inline-block;
            margin: 25px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        .content {{
            padding: 50px;
        }}
        
        .batch-section {{
            margin-bottom: 60px;
            background: linear-gradient(135deg, #f8f9ff, #e8f2ff);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }}
        
        .batch-title {{
            font-size: 2.2em;
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .schedule-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 15px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .schedule-table td {{
            padding: 15px 12px;
            text-align: center;
            border-bottom: 1px solid #e8ecf4;
        }}
        
        .schedule-table tr:nth-child(even) {{
            background: #f8f9ff;
        }}
        
        .course-code {{
            font-weight: 700;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .faculty-name {{
            color: #8e44ad;
            font-weight: 600;
            font-style: italic;
        }}
        
        .time-slot {{
            background: linear-gradient(135deg, #ffeaa7, #fab1a0);
            padding: 8px 12px;
            border-radius: 15px;
            font-weight: 600;
            color: #2d3436;
        }}
        
        .room-info {{
            background: linear-gradient(135deg, #81ecec, #74b9ff);
            color: #2d3436;
            padding: 8px 12px;
            border-radius: 15px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="university-name">{self.university_name}</div>
            <div class="title">{title}</div>
        </div>
        
        <div class="content">"""
        
        for batch_section, activities in all_activities.items():
            html += f"""
            <div class="batch-section">
                <h2 class="batch-title">{batch_section}</h2>
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Course Code</th>
                            <th>Course Title</th>
                            <th>Faculty Name</th>
                            <th>Credits</th>
                            <th>Time Slot</th>
                            <th>Room</th>
                        </tr>
                    </thead>
                    <tbody>"""
            
            for activity in activities:
                course_code = activity.course_code if activity.course_code else f"CSE{activity.id:03d}"
                course_title = activity.name if activity.name else f"Course {activity.id}"
                faculty_name = activity.faculty if activity.faculty else "TBA"
                room = activity.room if activity.room else "TBD"
                
                html += f"""
                        <tr>
                            <td><span class="course-code">{course_code}</span></td>
                            <td>{course_title}</td>
                            <td><span class="faculty-name">{faculty_name}</span></td>
                            <td>{activity.weight:.1f}</td>
                            <td><span class="time-slot">{self._format_time(activity.start)} - {self._format_time(activity.end)}</span></td>
                            <td><span class="room-info">{room}</span></td>
                        </tr>"""
            
            html += """
                    </tbody>
                </table>
            </div>"""
        
        html += """
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_pdf_from_html(self, html_content: str, pdf_filepath: str, html_filepath: str) -> str:
        """Generate PDF from HTML content"""
        
        # Try to generate PDF using WeasyPrint
        try:
            import weasyprint
            html_doc = weasyprint.HTML(string=html_content, base_url='.')
            html_doc.write_pdf(pdf_filepath)
            print(f"✅ Enhanced PDF generated: {pdf_filepath}")
            return pdf_filepath
        except ImportError:
            print("ℹ️ WeasyPrint not available - using ReportLab for PDF generation...")
        except Exception as e:
            if "libgobject" in str(e) or "GTK" in str(e):
                print("ℹ️ WeasyPrint requires GTK libraries (complex on Windows) - using ReportLab instead...")
            else:
                print(f"⚠️ WeasyPrint PDF generation failed: {e} - using ReportLab...")
        
        # Try ReportLab as fallback
        if self._generate_pdf_with_reportlab(html_content, pdf_filepath):
            print(f"✅ Enhanced PDF generated with ReportLab: {pdf_filepath}")
            return pdf_filepath
        else:
            print("⚠️ PDF generation failed - HTML version available")
            return html_filepath
    
    def _generate_pdf_with_reportlab(self, html_content: str, pdf_filepath: str) -> bool:
        """Generate PDF using ReportLab with comprehensive schedule content"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            import re
            
            # Create PDF document with landscape orientation for better table display
            doc = SimpleDocTemplate(pdf_filepath, pagesize=landscape(A4), 
                                   rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=20)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.darkblue,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.darkgreen,
                alignment=TA_CENTER,
                spaceAfter=15
            )
            
            section_style = ParagraphStyle(
                'SectionStyle',
                parent=styles['Heading3'],
                fontSize=14,
                textColor=colors.darkred,
                alignment=TA_CENTER,
                spaceAfter=10
            )
            
            # Extract title from HTML
            title_match = re.search(r'<title>(.*?)</title>', html_content)
            title = title_match.group(1) if title_match else "Academic Schedule"
            
            # Add header
            story.append(Paragraph("Bangladesh University of Professionals", title_style))
            story.append(Paragraph("Department of Computer Science & Engineering", subtitle_style))
            story.append(Paragraph(title, section_style))
            story.append(Spacer(1, 20))
            
            # Add generation info
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Extract schedule tables from HTML and convert to ReportLab tables
            # Look for table patterns in HTML
            table_pattern = r'<table[^>]*>(.*?)</table>'
            tables = re.findall(table_pattern, html_content, re.DOTALL | re.IGNORECASE)
            
            for i, table_html in enumerate(tables):
                # Extract table title if present
                title_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
                title_match = re.search(title_pattern, table_html, re.IGNORECASE)
                if title_match:
                    table_title = re.sub(r'<[^>]+>', '', title_match.group(1))
                    story.append(Paragraph(table_title, section_style))
                    story.append(Spacer(1, 10))
                
                # Extract table rows
                row_pattern = r'<tr[^>]*>(.*?)</tr>'
                rows = re.findall(row_pattern, table_html, re.DOTALL | re.IGNORECASE)
                
                if rows:
                    table_data = []
                    for row in rows:
                        # Extract cells
                        cell_pattern = r'<t[hd][^>]*>(.*?)</t[hd]>'
                        cells = re.findall(cell_pattern, row, re.DOTALL | re.IGNORECASE)
                        # Clean HTML tags from cells
                        clean_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
                        if clean_cells:
                            table_data.append(clean_cells)
                    
                    if table_data:
                        # Create ReportLab table
                        table = Table(table_data)
                        
                        # Apply table style
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 10),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 6),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                        ]))
                        
                        story.append(table)
                        story.append(Spacer(1, 20))
                
                # Add page break between major sections
                if i < len(tables) - 1:
                    story.append(PageBreak())
            
            # If no tables found, add a simple message
            if not tables:
                story.append(Paragraph("Schedule information processed and available.", styles['Normal']))
                story.append(Spacer(1, 10))
                story.append(Paragraph("For detailed view, please refer to the HTML version.", styles['Normal']))
            
            # Add footer
            story.append(Spacer(1, 30))
            story.append(Paragraph("This schedule is generated by the Enhanced Conflict-Free Scheduling System", 
                                 styles['Italic']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"❌ ReportLab PDF generation failed: {e}")
            return False
    
    def _format_time(self, time_slot: int) -> str:
        """Convert time slot to readable format"""
        base_hour = 8
        base_minute = 0
        
        total_minutes = base_minute + (time_slot * 30)
        hours = base_hour + (total_minutes // 60)
        minutes = total_minutes % 60
        
        hours = hours % 24
        
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


# Maintain backward compatibility
class PDFGenerator(EnhancedPDFGenerator):
    """Backward compatible PDF Generator"""
    pass


class AcademicPDFGenerator(EnhancedPDFGenerator):
    """Backward compatible Academic PDF Generator"""
    
    def generate_academic_schedule(self, activities: List[Activity], 
                                  batch_code: str = "BCSE24",
                                  section: str = "A",
                                  semester: str = "Spring 2025") -> str:
        """Generate academic schedule with enhanced design"""
        # Allocate rooms automatically
        activities = self.allocate_room(activities)
        
        return self.generate_section_routine(activities, batch_code, section, semester)
