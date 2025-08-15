from db.db import Database

def run_queries():
    # 1. List of rooms and the number of students in each
    query_1 = """
    SELECT r.id, r.name, COUNT(s.id) AS student_count
    FROM rooms r
    LEFT JOIN students s ON s.room = r.id
    GROUP BY r.id, r.name
    ORDER BY student_count DESC;
    """
    rooms_count = Database.execute(query_1, fetchall=True)
    print("Rooms and student counts:", rooms_count)

    # 2. Top 5 rooms with the smallest average student age
    query_2 = """
    SELECT r.id, r.name, AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
    FROM rooms r
    JOIN students s ON s.room = r.id
    GROUP BY r.id, r.name
    ORDER BY avg_age ASC
    LIMIT 5;
    """
    smallest_avg_age = Database.execute(query_2, fetchall=True)
    print("Top 5 rooms with smallest average age:", smallest_avg_age)

    # 3. Top 5 rooms with the largest age difference among students
    query_3 = """
    SELECT r.id, r.name,
           MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) -
           MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS age_diff
    FROM rooms r
    JOIN students s ON s.room = r.id
    GROUP BY r.id, r.name
    ORDER BY age_diff DESC
    LIMIT 5;
    """
    largest_age_diff = Database.execute(query_3, fetchall=True)
    print("Top 5 rooms with largest age difference:", largest_age_diff)

    # 4. List of rooms where students of different sexes live together
    query_4 = """
    SELECT r.id, r.name
    FROM rooms r
    JOIN students s ON s.room = r.id
    GROUP BY r.id, r.name
    HAVING COUNT(DISTINCT s.sex) > 1;
    """
    mixed_sex_rooms = Database.execute(query_4, fetchall=True)
    print("Rooms with mixed sexes:", mixed_sex_rooms)


def create_indexes():
    # Index on students.room for faster joins
    Database.execute("CREATE INDEX idx_students_room ON students(room);", commit=True)
    # Index on students.birthday for faster age calculations
    Database.execute("CREATE INDEX idx_students_birthday ON students(birthday);", commit=True)
    # Index on students.sex for mixed-sex query optimization
    Database.execute("CREATE INDEX idx_students_sex ON students(sex);", commit=True)
