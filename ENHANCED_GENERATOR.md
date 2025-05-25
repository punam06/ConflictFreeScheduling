# Enhanced Routine Generator

This update adds a comprehensive academic scheduling system for the BUP CSE Department. The enhanced routine generator improves on the previous conflict resolution algorithms with specific focus on the academic requirements:

## Features

- **Specialized for BUP CSE Department**: Handles 4 batches with correct course distributions:
  - BCSE22 (5 theory, 5 lab)
  - BCSE23 (5 theory, 4 lab) 
  - BCSE24 (5 theory, 4 lab)
  - BCSE25 (6 theory, 3 lab)

- **Comprehensive Room Management**: Schedules across 5 classrooms (CR302, CR303, CR304, CR504, LAB1003)

- **Advanced Time Slot Handling**: Supports specific time slots (8:30 AM - 5:00 PM) with lunch breaks (1:30-2:00 PM)

- **Course Credit Management**:
  - Theory: 1.5 hours (2 sessions/week, 3.0 credit)
  - Labs: 3 hours (1 session/week, 1.5 credit) or (1 session/2 weeks, 0.75 credit)

- **Faculty Constraints**: Handles faculty preferences and availability constraints

- **Conflict Resolution**: Intelligent scheduling with priority-based algorithm

## How to Use

The enhanced generator is available as a command-line option:

```
./scheduler --enhanced-generator
```

### Additional options:

```
./scheduler --enhanced-generator --comprehensive-routine  # Generate day-based PDF routine
./scheduler --enhanced-generator --init-db               # Initialize DB with fresh data first
./scheduler --enhanced-generator --batch BCSE23          # Generate for specific batch
```

## Quick Start

A convenience script is provided to quickly generate a comprehensive schedule:

```
./scripts/run_enhanced_generator.sh
```

This will initialize the database with sample data and generate a comprehensive routine with the enhanced generator.

## Implementation

The enhanced generator is implemented in:
- `src/algorithms/enhanced_routine_generator.h`: Data structures and class definition
- `src/algorithms/enhanced_routine_generator.cpp`: Algorithm implementation

The generator uses a priority-based scheduling approach:
1. External faculty are scheduled first
2. Higher credit courses have higher priority
3. Lab courses are prioritized due to room constraints
4. Newer batches (lower years) are prioritized
