import sqlite3

class DatabaseManager:
    def __init__(self , db_path="recordings.db"):
        self.db_path = db_path
        self.setup_db()


    def connect(self):
        return sqlite3.connect(self.db_path)


    # Create the tables
    def setup_db(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """DROP TABLE IF EXISTS recordings"""
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recordings (
                recording_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                folder TEXT,
                sound_file TEXT,
                transcript_file TEXT,
                analysis_file TEXT,
                transcript TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # ai_analysis table
        cursor.execute(
            """DROP TABLE IF EXISTS ai_analysis""")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_analysis (
                analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                recording_id INTEGER,
                analysis_type TEXT,
                model TEXT,
                temp FLOAT,
                analysis_file TEXT,
                analysis_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recording_id) REFERENCES recordings(recording_id)
            );
        """
            )
        conn.commit()
        conn.close()
        #print("SQL is set")

    def save_recording(self, timestamp, folder, sound_file, transcript_file=None, analysis_file=None, transcript=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recordings (timestamp, folder, sound_file, transcript_file, analysis_file, transcript)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, folder, sound_file, transcript_file, analysis_file, transcript))
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    def update_transcript(self, recording_id, transcript_file, transcript):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE recordings
            SET transcript_file = ?, transcript = ?
            WHERE recording_id = ?
        """, (transcript_file, transcript, recording_id))
        conn.commit()
        conn.close()


    def save_analysis(self , recording_id , analysis_type , model , temp , analysis_file):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ai_analysis (recording_id, analysis_type, model, temp, analysis_file)
            VALUES (?, ?, ?, ?, ?)
        """ , (recording_id , analysis_type , model , temp , analysis_file)
            )
        conn.commit()
        conn.close()

