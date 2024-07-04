from __init__ import CURSOR, CONN




# department.py
class Department:
    # Dictionary to cache instances
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Creates the departments table."""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the departments table."""
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()
        cls.all.clear()

    def save(self):
        """Saves or updates the Department instance in the database."""
        if self.id:
            CURSOR.execute('''
                UPDATE departments SET name=?, location=? WHERE id=?
            ''', (self.name, self.location, self.id))
        else:
            CURSOR.execute('''
                INSERT INTO departments (name, location) VALUES (?, ?)
            ''', (self.name, self.location))
            self.id = CURSOR.lastrowid
            Department.all[self.id] = self
        CONN.commit()

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance."""
        if self.id:
            CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))
            CONN.commit()
            del Department.all[self.id] 
            self.id = None 
    @classmethod
    def create(cls, name, location):
        """Creates a new Department instance and saves it to the database."""
        department = cls(name, location)
        department.save()
        return department


    @classmethod
    def instance_from_db(cls, row):
        """Creates or updates a Department instance from a database row."""
        id, name, location = row
        if id in cls.all:
            department = cls.all[id]
            department.name, department.location = name, location
        else:
            department = cls(name, location, id)
            cls.all[id] = department
        return department

    @classmethod
    def get_all(cls):
        """Returns all departments from the database as instances."""
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Finds a department by its ID."""
        row = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Finds the first department by its name."""
        row = CURSOR.execute("SELECT * FROM departments WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row) if row else None


        CURSOR.execute(sql, (self.id,))
        CONN.commit()
