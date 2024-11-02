from .database_connection import DatabaseConnection


class GroupManager:
    def __init__(self):
        pass

    @classmethod
    def add_group(cls, group_name, tournament_id) -> None:
        """
        Adds specified group to table | Usage: \n  add_group('group_name', 'tournament_id')
        :param group_name:
        :param tournament_id:
        :return:
        """
        query = """
        INSERT INTO groups(group_name, tournament_id) VALUES (%s, %s)
        """

        with DatabaseConnection() as connection:
            cur = connection.cursor()

            cur.execute("SELECT * FROM groups")
            if not cur.fetchall():
                cur.execute("""ALTER SEQUENCE public.groups_group_id_seq RESTART WITH 1""")
            else:
                cur.execute("""
                            SELECT setval('public.groups_group_id_seq', 
                            (SELECT COALESCE(MAX(group_id), 1) FROM groups))
                            """) # resets the count to current MAX value

            cur.execute(query, (group_name, tournament_id,)) # Insert new to db


    @classmethod
    def delete_group(cls, group_name: str) -> None:
        """
        Removes the specified group from table
        :param group_name:
        :return:
        """
        with DatabaseConnection() as connection:
            cur = connection.cursor()

            cur.execute("DELETE FROM groups WHERE group_name=%s", (group_name,))


    @classmethod
    def list_groups(cls) -> []:
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            query = """
                        SELECT groups.group_id, groups.group_name, tournament.tournament_name
                        FROM groups
                        JOIN tournament ON groups.tournament_id = tournament.tournament_id
                    """
            cur.execute(query)

            # print("*--------------*\n*----GROUPS----*\n*--------------*")
            # if not group_list:
            #     print("No groups formed")
            # for group in group_list:
            #     print(f"  \t{group[1]}")

            return [{'id': row[0], 'name': row[1], 'tournament': row[2]} for row in cur.fetchall()]


    @classmethod
    def add_team_to_group(cls, team_name, to_group):
        """
            Assigns a team to a specified group in the database.

            This method updates the `group_id` of a team in the `teams` table,
            associating it with a given group.

            Parameters:
                team_name (str): The name of the team to assign to a group.
                to_group (int, Any): The ID of the group to which the team should be assigned.

            Returns:
                None

            Raises:
                DatabaseError: If an error occurs during the database operation.

            Example:
                >> add_team_to_group("Tigers", 2)
                Successfully added Tigers to group
            """
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            query = "UPDATE teams SET group_id = %s WHERE team_name=%s"

            cur.execute(query, (to_group, team_name))


    @classmethod
    def list_teams(cls):
        with DatabaseConnection() as connection:
            cur = connection.cursor()
            query = """
                        SELECT  teams.team_id, teams.team_name, teams.group_id FROM teams
                    """
            cur.execute(query)

            # print("*--------------*\n*----GROUPS----*\n*--------------*")
            # if not group_list:
            #     print("No groups formed")
            # for group in group_list:
            #     print(f"  \t{group[1]}")

            return [{'team_id': row[0], 'name': row[1], 'group_id': row[2]} for row in cur.fetchall()]


    @classmethod
    def list_teams_with_groups(cls):
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            query = """
                    SELECT teams.team_id, teams.team_name, COALESCE(groups.group_name, 'Not Assigned') AS group_name
                    FROM teams
                    LEFT JOIN groups ON teams.group_id = groups.group_id
                """
            cur.execute(query)

            return [{'id': row[0], 'name': row[1], 'group': row[2]} for row in cur.fetchall()]



test = GroupManager()

# TESTING API

"""
Add Group To Tournament Table
# test.add_group('GROUP C', 2)
Remove Group From Table
test.delete_group('GROUP C')
List Groups
test.list_groups()
Add Team To Group Table
test.add_team_to_group(team_name='Team A', to_group=1)
"""





