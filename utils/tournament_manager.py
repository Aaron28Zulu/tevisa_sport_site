from .database_connection import DatabaseConnection

class TournamentManager:
    @classmethod
    def add_tournament(cls, tournament_name, start_date, end_date) -> None:
        """
        Registers a tournament by taking in: tournament_name, start date, end_date | a tuple | i.e (Youth Tournament, 2024-12-16, 2024-12-28)
        :param tournament_name:
        :param start_date:
        :param end_date:
        :return:
        """

        with DatabaseConnection() as connection:
            cur = connection.cursor()

            cur.execute('select * from tournament')

            if cur.fetchall():
                cur.execute("""
                            SELECT setval('public.tournament_tournament_id_seq', 
                            (SELECT COALESCE(MAX(tournament_id), 1) FROM tournament))
                            """)
            else:
                cur.execute("""
                            ALTER SEQUENCE public.tournament_tournament_id_seq RESTART WITH 1
                            """)
                        # public.tournament_tournament_id_seq
            query = "INSERT INTO tournament(tournament_name, start_date, end_date) VALUES (%s, %s, %s);"
            cur.execute(query, (tournament_name, start_date, end_date))


    @classmethod
    def delete_tournament(cls, tournament_id): # lambda x: x['tournament'] == tournament_id
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            query = "DELETE FROM tournament WHERE tournament_id=%s;"
            cur.execute(query, (tournament_id,))


    @classmethod
    def mark_tournament_as_read(cls, tournament_name):
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            query = "UPDATE tournaments SET is_ended = TRUE WHERE tournament_name = %s;"
            cur.execute(query, (tournament_name,))


    @classmethod
    def update_tournament(cls, tournament_name, start_date, end_date, tournament_id):
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("""
                        UPDATE tournament
                        SET tournament_name = %s, start_date = %s, end_date = %s
                        WHERE tournament_id = %s
                    """, (tournament_name, start_date, end_date, tournament_id))



    @classmethod
    def list_tournaments(cls) -> []:
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM tournament")

            return [{'id': row[0], 'name': row[1], 'start_date': row[2], 'end_date': row[3]} for row in cur.fetchall()]

