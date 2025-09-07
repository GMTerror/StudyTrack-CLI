# StudyTrack CLI

A lightweight command-line academic progress tracker built with Python and MySQL. Manage your studies, assignments, and exam schedules efficiently through simple terminal commands.

## Features

### 📚 Study Session Management
- Log study sessions with subject, topic, duration, and date
- Add detailed notes for each study session
- Mark study sessions as complete or incomplete
- View study session history filtered by subject or date range
- Calculate and display total study hours per subject
- Track which topics have been covered for each subject

### 📝 Assignment and Task Tracking
- Create assignments with titles, descriptions, and due dates
- Set assignment status as pending or completed
- View upcoming assignments sorted by due date
- Display overdue assignments with highlighted warnings

### 📊 Progress Tracking and Reporting
- Generate study time distribution reports by subject
- Display assignment completion rates and statistics
- Show study consistency through activity logs
- Create semester summaries with total hours and completed tasks
- Track study streaks over time
- Compare progress across different subjects

### 🎯 Planning and Suggestions
- List upcoming exams in chronological order
- Display subjects needing attention based on exam proximity
- Show study hour totals to identify under-studied subjects
- Generate simple text-based study schedule templates
- Suggest daily study focus based on pending work
- Recommend time allocation across subjects

### 💾 Data Management
- Persistent storage of all data in MySQL database
- Multi-semester support with easy term switching
- Data backup and restore capabilities
- Import/export functionality for data portability
- Database integrity checks and maintenance tools

### ⌨️ Command-Line Interface
- Simple, intuitive command syntax
- Quick data entry through structured prompts
- Formatted table displays for easy reading
- Search and filter commands for data retrieval
- Help system with command documentation
- Configuration management through settings file

## Tech Stack

- **Python 3.x** - Core application logic
- **MySQL** - Data persistence and storage
- **CLI Interface** - Terminal-based user interaction

## Requirements

- Python 3.6+
- MySQL 5.7+ or MariaDB
- Terminal/Command Prompt access

## Installation

```bash
# Clone the repository
git clone https://github.com/GMTerror/studytrack-cli.git
cd studytrack-cli

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py
```

## Use Cases

- Track daily study sessions across multiple subjects
- Monitor assignment deadlines and completion status
- Plan study schedules based on upcoming exams
- Generate academic progress reports
- Maintain organized records of academic activities

Perfect for students who prefer terminal-based tools and want a distraction-free way to manage their academic workload.

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

*Keep your studies organized, one command at a time.* 
