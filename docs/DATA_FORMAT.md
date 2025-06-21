# Data Format Specification

This document describes the data formats used by the Conflict-Free Scheduling System for input and output.

## Activity Data Format

Activities are the core data structure used by the scheduling system. Each activity represents a task or event that needs to be scheduled, such as a class session, meeting, or exam.

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `id`     | Integer | Unique identifier for the activity |
| `start`  | Integer | Start time (in minutes from reference point) |
| `end`    | Integer | End time (in minutes from reference point) |
| `weight` | Float | Priority/importance of the activity (e.g., credit hours) |
| `name`   | String | Name or description of the activity |
| `room`   | String | Location where the activity will take place |

### CSV Format

When using CSV files for input/output, use the following format:

```csv
id,start,end,weight,name,room
1,0,90,3.0,Programming Fundamentals,Room 101
2,100,190,3.0,Data Structures,Room 102
```

Header row is required, and all fields should be included even if some values are empty.

### JSON Format

When using JSON files for input/output, use the following format:

```json
[
  {
    "id": 1,
    "start": 0,
    "end": 90,
    "weight": 3.0,
    "name": "Programming Fundamentals",
    "room": "Room 101"
  },
  {
    "id": 2,
    "start": 100,
    "end": 190,
    "weight": 3.0,
    "name": "Data Structures",
    "room": "Room 102"
  }
]
```

### Time Representation

Times are represented as integers indicating minutes from a reference point (usually the start of the day or week). 

For example:
- 0 might represent 8:00 AM
- 60 would represent 9:00 AM (60 minutes after the reference point)
- 90 would represent 9:30 AM (90 minutes after the reference point)

## Database Schema

When using the database, the following tables are used:

### Batches Table
- `batch_id`: Primary key
- `batch_code`: Unique identifier (e.g., "BCSE24")
- `batch_name`: Descriptive name
- `year_level`: Current year level (1-4)
- `semester`: Current semester (1-8)
- `total_sections`: Number of sections (default: 2)
- `status`: Batch status (ACTIVE/INACTIVE/GRADUATED)

### Teachers Table
- `teacher_id`: Primary key
- `teacher_code`: Unique identifier
- `full_name`: Teacher's full name
- `designation`: Position or title
- `department`: Department (default: "CSE")
- `email`: Contact email
- `phone`: Contact phone number
- `availability_*`: Availability constraints
- `status`: Teacher status (ACTIVE/INACTIVE/ON_LEAVE)

### Courses Table
- `course_id`: Primary key
- `course_code`: Unique identifier (e.g., "CSE101")
- `course_title`: Course name
- `credit_hours`: Credit hours (e.g., 3.0)
- `class_type`: Type (THEORY/LAB)
- `session_duration`: Duration in minutes (default: 90)
- `sessions_per_week`: Number of sessions per week
- `batch_id`: Foreign key to Batches
- `teacher_id`: Foreign key to Teachers

### Classrooms Table
- `room_id`: Primary key
- `room_code`: Unique identifier (e.g., "Room101")
- `capacity`: Maximum capacity
- `room_type`: Type (THEORY/LAB/BOTH)
- `building`: Building name
- `floor_number`: Floor number
- `status`: Room status (AVAILABLE/MAINTENANCE/UNAVAILABLE)

## Generated Output

The system generates output in the following formats:

### HTML Schedule
An HTML file with a styled table showing the scheduled activities, including:
- Activity name
- Time slot (start and end times)
- Room assignment
- Weight/credit hours

### Academic PDF Schedule
An enhanced HTML file with university branding, including:
- University and department headers
- Batch and section information
- Tabular schedule layout
- Summary statistics
- Date and timestamp

## Sample Files

See the following files for examples:
- `data/demo_activities.csv` - Sample CSV input
- `data/demo_activities.json` - Sample JSON input
- `output/schedule_*.html` - Generated schedule HTML
- `output/academic_schedule_*.html` - Generated academic schedule HTML
