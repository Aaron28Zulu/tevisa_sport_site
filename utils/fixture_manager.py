from .database_connection import DatabaseConnection

class FixtureManager:
    @classmethod
    def list_fixtures(cls):
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("""
                        SELECT f.fixture_id, f.fixture_date, f.tournament_id, 
                               team1.team_name AS team1_name, team2.team_name AS team2_name, 
                               t.tournament_name AS tournament_name
                        FROM fixtures f
                        JOIN tournament t ON f.tournament_id = t.tournament_id
                        JOIN teams team1 ON f.team1_id = team1.team_id
                        JOIN teams team2 ON f.team2_id = team2.team_id
                    """)

            return [
                        {
                            'id': row[0],
                            'date': row[1],
                            'tournament_name': row[2],
                            'team1_name': row[3],
                            'team2_name': row[4],
                        }
                        for row in cur.fetchall()
                    ]


    @classmethod
    def add_fixture(cls, fixture_date, team1_id, team2_id, tournament_id):
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM fixtures")
            if not cur.fetchall():
                cur.execute("ALTER SEQUENCE public.fixtures_fixture_id_seq RESTART WITH 1")
            else:
                cur.execute("""
                            SELECT setval('public.fixtures_fixture_id_seq', 
                            (SELECT COALESCE(MAX(fixture_id), 1) FROM fixtures))
                            """)
            query = """
                    INSERT INTO fixtures (fixture_date, tournament_id, team1_id, team2_id)
                    VALUES (%s, %s, %s, %s)
                """
            cur.execute(query, (fixture_date, tournament_id, team1_id, team2_id))


            # Regiter fixture to scores_results table
            cur.execute("SELECT fixture_id FROM fixtures WHERE fixture_date=%s", (fixture_date,))

            fixture_id = cur.fetchall()[0]
            cur.execute("SELECT * FROM scores_results")

            if cur.fetchall():
                cur.execute("""
                            SELECT setval('public.scores_results_score_id_seq', 
                            (SELECT COALESCE(MAX(score_id), 1) FROM scores_results))
                            """)
            else:
                cur.execute("ALTER SEQUENCE public.scores_results_score_id_seq RESTART WITH 1")
            cur.execute("INSERT INTO scores_results(fixture_id, team1_score, team2_score) VALUES (%s, %s, %s)", (fixture_id, 0, 0))


    @classmethod
    def delete_fixture(cls, fixture_id):
        with DatabaseConnection() as conn:
            cur = conn.cursor()

            query = "DELETE FROM fixtures WHERE fixture_id=%s"
            cur.execute(query, fixture_id)
