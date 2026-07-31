"""
Lesson data and management
"""

LESSONS_DATA = {
    'A1': {
        'level_name': 'Beginner',
        'total_lessons': 20,
        'lessons': [
            {
                'lesson_number': 1,
                'title': 'Greetings (Salomlashish)',
                'content': 'Hello, Hi, Good morning, Good afternoon, Good evening',
                'examples': [
                    'Hello! My name is John.',
                    'Hi! How are you?',
                    'Good morning!'
                ],
                'vocabulary': [
                    {'word': 'Hello', 'uzbek': 'Salom', 'pronunciation': 'hə-ˈlō'},
                    {'word': 'Hi', 'uzbek': 'Salom', 'pronunciation': 'hī'},
                    {'word': 'Good', 'uzbek': 'Yaxshi', 'pronunciation': 'ɡo͝od'}
                ]
            },
            {
                'lesson_number': 2,
                'title': 'Personal Information (Shaxsiy ma\'lumot)',
                'content': 'Name, age, nationality, occupation',
                'examples': [
                    'My name is Sarah.',
                    'I am 25 years old.',
                    'I am from Uzbekistan.'
                ],
                'vocabulary': [
                    {'word': 'Name', 'uzbek': 'Ism', 'pronunciation': 'nām'},
                    {'word': 'Age', 'uzbek': 'Yosh', 'pronunciation': 'āj'},
                    {'word': 'From', 'uzbek': 'Dan', 'pronunciation': 'frəm'}
                ]
            }
        ]
    },
    'A2': {
        'level_name': 'Elementary',
        'total_lessons': 20,
        'lessons': []
    },
    'B1': {
        'level_name': 'Intermediate',
        'total_lessons': 20,
        'lessons': []
    },
    'B2': {
        'level_name': 'Upper-Intermediate',
        'total_lessons': 20,
        'lessons': []
    },
    'C1': {
        'level_name': 'Advanced',
        'total_lessons': 20,
        'lessons': []
    }
}


def get_lessons_by_level(level: str) -> Dict:
    """Get all lessons for a specific level"""
    return LESSONS_DATA.get(level, {})


def get_lesson(level: str, lesson_number: int) -> Optional[Dict]:
    """Get specific lesson"""
    lessons = get_lessons_by_level(level)
    for lesson in lessons.get('lessons', []):
        if lesson['lesson_number'] == lesson_number:
            return lesson
    return None
