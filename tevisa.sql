PGDMP       &            
    |            tevisa    16.4 (Debian 16.4-1)    16.4 (Debian 16.4-1) \    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16517    tevisa    DATABASE     n   CREATE DATABASE tevisa WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';
    DROP DATABASE tevisa;
                postgres    false            �            1259    16723    admins    TABLE     ,  CREATE TABLE public.admins (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_admin boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.admins;
       public         heap    postgres    false            �            1259    16722    admins_id_seq    SEQUENCE     �   CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.admins_id_seq;
       public          postgres    false    234            �           0    0    admins_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;
          public          postgres    false    233            �            1259    16552    coach    TABLE     m   CREATE TABLE public.coach (
    coach_id integer NOT NULL,
    coach_name character varying(100) NOT NULL
);
    DROP TABLE public.coach;
       public         heap    postgres    false            �            1259    16551    coach_coach_id_seq    SEQUENCE     �   CREATE SEQUENCE public.coach_coach_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.coach_coach_id_seq;
       public          postgres    false    222            �           0    0    coach_coach_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.coach_coach_id_seq OWNED BY public.coach.coach_id;
          public          postgres    false    221            �            1259    16598    fixtures    TABLE     �   CREATE TABLE public.fixtures (
    fixture_id integer NOT NULL,
    fixture_date date NOT NULL,
    team1_id integer,
    team2_id integer,
    tournament_id integer
);
    DROP TABLE public.fixtures;
       public         heap    postgres    false            �            1259    16597    fixtures_fixture_id_seq    SEQUENCE     �   CREATE SEQUENCE public.fixtures_fixture_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.fixtures_fixture_id_seq;
       public          postgres    false    228            �           0    0    fixtures_fixture_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.fixtures_fixture_id_seq OWNED BY public.fixtures.fixture_id;
          public          postgres    false    227            �            1259    16637    group_standings    TABLE     �   CREATE TABLE public.group_standings (
    standing_id integer NOT NULL,
    group_id integer,
    team_id integer,
    points integer NOT NULL,
    wins integer NOT NULL,
    losses integer NOT NULL,
    draws integer NOT NULL
);
 #   DROP TABLE public.group_standings;
       public         heap    postgres    false            �            1259    16636    group_standings_standing_id_seq    SEQUENCE     �   CREATE SEQUENCE public.group_standings_standing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.group_standings_standing_id_seq;
       public          postgres    false    232            �           0    0    group_standings_standing_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.group_standings_standing_id_seq OWNED BY public.group_standings.standing_id;
          public          postgres    false    231            �            1259    16540    groups    TABLE     �   CREATE TABLE public.groups (
    group_id integer NOT NULL,
    group_name character varying(50) NOT NULL,
    tournament_id integer
);
    DROP TABLE public.groups;
       public         heap    postgres    false            �            1259    16539    groups_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.groups_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.groups_group_id_seq;
       public          postgres    false    220            �           0    0    groups_group_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.groups_group_id_seq OWNED BY public.groups.group_id;
          public          postgres    false    219            �            1259    16526    institution    TABLE     �   CREATE TABLE public.institution (
    institution_id integer NOT NULL,
    institution_name character varying(100) NOT NULL,
    institution_town character varying(25)
);
    DROP TABLE public.institution;
       public         heap    postgres    false            �            1259    16525    institution_institution_id_seq    SEQUENCE     �   CREATE SEQUENCE public.institution_institution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.institution_institution_id_seq;
       public          postgres    false    216            �           0    0    institution_institution_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.institution_institution_id_seq OWNED BY public.institution.institution_id;
          public          postgres    false    215            �            1259    16586    players    TABLE     �   CREATE TABLE public.players (
    player_id integer NOT NULL,
    player_name character varying(100) NOT NULL,
    team_id integer,
    player_gender character varying(1),
    age integer
);
    DROP TABLE public.players;
       public         heap    postgres    false            �            1259    16585    players_player_id_seq    SEQUENCE     �   CREATE SEQUENCE public.players_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.players_player_id_seq;
       public          postgres    false    226            �           0    0    players_player_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.players_player_id_seq OWNED BY public.players.player_id;
          public          postgres    false    225            �            1259    16620    scores_results    TABLE     �   CREATE TABLE public.scores_results (
    score_id integer NOT NULL,
    fixture_id integer,
    team1_score integer NOT NULL,
    team2_score integer NOT NULL,
    winning_team_id integer
);
 "   DROP TABLE public.scores_results;
       public         heap    postgres    false            �            1259    16619    scores_results_score_id_seq    SEQUENCE     �   CREATE SEQUENCE public.scores_results_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.scores_results_score_id_seq;
       public          postgres    false    230            �           0    0    scores_results_score_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.scores_results_score_id_seq OWNED BY public.scores_results.score_id;
          public          postgres    false    229            �            1259    16559    teams    TABLE     �   CREATE TABLE public.teams (
    team_id integer NOT NULL,
    team_name character varying(100) NOT NULL,
    institution_id integer,
    coach_id integer,
    group_id integer,
    tournament_id integer
);
    DROP TABLE public.teams;
       public         heap    postgres    false            �            1259    16558    teams_team_id_seq    SEQUENCE     �   CREATE SEQUENCE public.teams_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.teams_team_id_seq;
       public          postgres    false    224            �           0    0    teams_team_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.teams_team_id_seq OWNED BY public.teams.team_id;
          public          postgres    false    223            �            1259    16533 
   tournament    TABLE     �   CREATE TABLE public.tournament (
    tournament_id integer NOT NULL,
    tournament_name character varying(100) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);
    DROP TABLE public.tournament;
       public         heap    postgres    false            �            1259    16532    tournament_tournament_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tournament_tournament_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.tournament_tournament_id_seq;
       public          postgres    false    218            �           0    0    tournament_tournament_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.tournament_tournament_id_seq OWNED BY public.tournament.tournament_id;
          public          postgres    false    217            �           2604    16726 	   admins id    DEFAULT     f   ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);
 8   ALTER TABLE public.admins ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    233    234    234            �           2604    16555    coach coach_id    DEFAULT     p   ALTER TABLE ONLY public.coach ALTER COLUMN coach_id SET DEFAULT nextval('public.coach_coach_id_seq'::regclass);
 =   ALTER TABLE public.coach ALTER COLUMN coach_id DROP DEFAULT;
       public          postgres    false    221    222    222            �           2604    16601    fixtures fixture_id    DEFAULT     z   ALTER TABLE ONLY public.fixtures ALTER COLUMN fixture_id SET DEFAULT nextval('public.fixtures_fixture_id_seq'::regclass);
 B   ALTER TABLE public.fixtures ALTER COLUMN fixture_id DROP DEFAULT;
       public          postgres    false    228    227    228            �           2604    16640    group_standings standing_id    DEFAULT     �   ALTER TABLE ONLY public.group_standings ALTER COLUMN standing_id SET DEFAULT nextval('public.group_standings_standing_id_seq'::regclass);
 J   ALTER TABLE public.group_standings ALTER COLUMN standing_id DROP DEFAULT;
       public          postgres    false    232    231    232            �           2604    16543    groups group_id    DEFAULT     r   ALTER TABLE ONLY public.groups ALTER COLUMN group_id SET DEFAULT nextval('public.groups_group_id_seq'::regclass);
 >   ALTER TABLE public.groups ALTER COLUMN group_id DROP DEFAULT;
       public          postgres    false    220    219    220            �           2604    16529    institution institution_id    DEFAULT     �   ALTER TABLE ONLY public.institution ALTER COLUMN institution_id SET DEFAULT nextval('public.institution_institution_id_seq'::regclass);
 I   ALTER TABLE public.institution ALTER COLUMN institution_id DROP DEFAULT;
       public          postgres    false    215    216    216            �           2604    16589    players player_id    DEFAULT     v   ALTER TABLE ONLY public.players ALTER COLUMN player_id SET DEFAULT nextval('public.players_player_id_seq'::regclass);
 @   ALTER TABLE public.players ALTER COLUMN player_id DROP DEFAULT;
       public          postgres    false    225    226    226            �           2604    16623    scores_results score_id    DEFAULT     �   ALTER TABLE ONLY public.scores_results ALTER COLUMN score_id SET DEFAULT nextval('public.scores_results_score_id_seq'::regclass);
 F   ALTER TABLE public.scores_results ALTER COLUMN score_id DROP DEFAULT;
       public          postgres    false    229    230    230            �           2604    16562    teams team_id    DEFAULT     n   ALTER TABLE ONLY public.teams ALTER COLUMN team_id SET DEFAULT nextval('public.teams_team_id_seq'::regclass);
 <   ALTER TABLE public.teams ALTER COLUMN team_id DROP DEFAULT;
       public          postgres    false    223    224    224            �           2604    16536    tournament tournament_id    DEFAULT     �   ALTER TABLE ONLY public.tournament ALTER COLUMN tournament_id SET DEFAULT nextval('public.tournament_tournament_id_seq'::regclass);
 G   ALTER TABLE public.tournament ALTER COLUMN tournament_id DROP DEFAULT;
       public          postgres    false    217    218    218            �          0    16723    admins 
   TABLE DATA           Z   COPY public.admins (id, username, email, password_hash, is_admin, created_at) FROM stdin;
    public          postgres    false    234   �o       }          0    16552    coach 
   TABLE DATA           5   COPY public.coach (coach_id, coach_name) FROM stdin;
    public          postgres    false    222   Dp       �          0    16598    fixtures 
   TABLE DATA           _   COPY public.fixtures (fixture_id, fixture_date, team1_id, team2_id, tournament_id) FROM stdin;
    public          postgres    false    228   qp       �          0    16637    group_standings 
   TABLE DATA           f   COPY public.group_standings (standing_id, group_id, team_id, points, wins, losses, draws) FROM stdin;
    public          postgres    false    232   �p       {          0    16540    groups 
   TABLE DATA           E   COPY public.groups (group_id, group_name, tournament_id) FROM stdin;
    public          postgres    false    220   �p       w          0    16526    institution 
   TABLE DATA           Y   COPY public.institution (institution_id, institution_name, institution_town) FROM stdin;
    public          postgres    false    216   �p       �          0    16586    players 
   TABLE DATA           V   COPY public.players (player_id, player_name, team_id, player_gender, age) FROM stdin;
    public          postgres    false    226   :q       �          0    16620    scores_results 
   TABLE DATA           i   COPY public.scores_results (score_id, fixture_id, team1_score, team2_score, winning_team_id) FROM stdin;
    public          postgres    false    230   rq                 0    16559    teams 
   TABLE DATA           f   COPY public.teams (team_id, team_name, institution_id, coach_id, group_id, tournament_id) FROM stdin;
    public          postgres    false    224   �q       y          0    16533 
   tournament 
   TABLE DATA           Z   COPY public.tournament (tournament_id, tournament_name, start_date, end_date) FROM stdin;
    public          postgres    false    218   �q       �           0    0    admins_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.admins_id_seq', 2, true);
          public          postgres    false    233            �           0    0    coach_coach_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.coach_coach_id_seq', 3, true);
          public          postgres    false    221            �           0    0    fixtures_fixture_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.fixtures_fixture_id_seq', 1, false);
          public          postgres    false    227            �           0    0    group_standings_standing_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.group_standings_standing_id_seq', 1, false);
          public          postgres    false    231            �           0    0    groups_group_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.groups_group_id_seq', 2, true);
          public          postgres    false    219            �           0    0    institution_institution_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.institution_institution_id_seq', 7, true);
          public          postgres    false    215            �           0    0    players_player_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.players_player_id_seq', 2, true);
          public          postgres    false    225            �           0    0    scores_results_score_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.scores_results_score_id_seq', 1, false);
          public          postgres    false    229            �           0    0    teams_team_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.teams_team_id_seq', 7, true);
          public          postgres    false    223            �           0    0    tournament_tournament_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.tournament_tournament_id_seq', 4, true);
          public          postgres    false    217            �           2606    16734    admins admins_email_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_email_key UNIQUE (email);
 A   ALTER TABLE ONLY public.admins DROP CONSTRAINT admins_email_key;
       public            postgres    false    234            �           2606    16730    admins admins_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.admins DROP CONSTRAINT admins_pkey;
       public            postgres    false    234            �           2606    16732    admins admins_username_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_username_key UNIQUE (username);
 D   ALTER TABLE ONLY public.admins DROP CONSTRAINT admins_username_key;
       public            postgres    false    234            �           2606    16667    coach coach_coach_name_key 
   CONSTRAINT     [   ALTER TABLE ONLY public.coach
    ADD CONSTRAINT coach_coach_name_key UNIQUE (coach_name);
 D   ALTER TABLE ONLY public.coach DROP CONSTRAINT coach_coach_name_key;
       public            postgres    false    222            �           2606    16557    coach coach_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.coach
    ADD CONSTRAINT coach_pkey PRIMARY KEY (coach_id);
 :   ALTER TABLE ONLY public.coach DROP CONSTRAINT coach_pkey;
       public            postgres    false    222            �           2606    16603    fixtures fixtures_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_pkey PRIMARY KEY (fixture_id);
 @   ALTER TABLE ONLY public.fixtures DROP CONSTRAINT fixtures_pkey;
       public            postgres    false    228            �           2606    16642 $   group_standings group_standings_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.group_standings
    ADD CONSTRAINT group_standings_pkey PRIMARY KEY (standing_id);
 N   ALTER TABLE ONLY public.group_standings DROP CONSTRAINT group_standings_pkey;
       public            postgres    false    232            �           2606    16545    groups groups_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);
 <   ALTER TABLE ONLY public.groups DROP CONSTRAINT groups_pkey;
       public            postgres    false    220            �           2606    16654 ,   institution institution_institution_name_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.institution
    ADD CONSTRAINT institution_institution_name_key UNIQUE (institution_name);
 V   ALTER TABLE ONLY public.institution DROP CONSTRAINT institution_institution_name_key;
       public            postgres    false    216            �           2606    16531    institution institution_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.institution
    ADD CONSTRAINT institution_pkey PRIMARY KEY (institution_id);
 F   ALTER TABLE ONLY public.institution DROP CONSTRAINT institution_pkey;
       public            postgres    false    216            �           2606    16591    players players_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);
 >   ALTER TABLE ONLY public.players DROP CONSTRAINT players_pkey;
       public            postgres    false    226            �           2606    16625 "   scores_results scores_results_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.scores_results
    ADD CONSTRAINT scores_results_pkey PRIMARY KEY (score_id);
 L   ALTER TABLE ONLY public.scores_results DROP CONSTRAINT scores_results_pkey;
       public            postgres    false    230            �           2606    16564    teams teams_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);
 :   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_pkey;
       public            postgres    false    224            �           2606    16685    teams teams_team_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_team_name_key UNIQUE (team_name);
 C   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_team_name_key;
       public            postgres    false    224            �           2606    16538    tournament tournament_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT tournament_pkey PRIMARY KEY (tournament_id);
 D   ALTER TABLE ONLY public.tournament DROP CONSTRAINT tournament_pkey;
       public            postgres    false    218            �           2606    16604    fixtures fixtures_team1_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_team1_id_fkey FOREIGN KEY (team1_id) REFERENCES public.teams(team_id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.fixtures DROP CONSTRAINT fixtures_team1_id_fkey;
       public          postgres    false    228    3273    224            �           2606    16609    fixtures fixtures_team2_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_team2_id_fkey FOREIGN KEY (team2_id) REFERENCES public.teams(team_id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.fixtures DROP CONSTRAINT fixtures_team2_id_fkey;
       public          postgres    false    3273    228    224            �           2606    16614 $   fixtures fixtures_tournament_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.fixtures DROP CONSTRAINT fixtures_tournament_id_fkey;
       public          postgres    false    228    218    3265            �           2606    16643 -   group_standings group_standings_group_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.group_standings
    ADD CONSTRAINT group_standings_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.group_standings DROP CONSTRAINT group_standings_group_id_fkey;
       public          postgres    false    220    232    3267            �           2606    16648 ,   group_standings group_standings_team_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.group_standings
    ADD CONSTRAINT group_standings_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id) ON DELETE CASCADE;
 V   ALTER TABLE ONLY public.group_standings DROP CONSTRAINT group_standings_team_id_fkey;
       public          postgres    false    224    3273    232            �           2606    16546     groups groups_tournament_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.groups DROP CONSTRAINT groups_tournament_id_fkey;
       public          postgres    false    218    220    3265            �           2606    16592    players players_team_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id) ON DELETE CASCADE;
 F   ALTER TABLE ONLY public.players DROP CONSTRAINT players_team_id_fkey;
       public          postgres    false    224    226    3273            �           2606    16626 -   scores_results scores_results_fixture_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.scores_results
    ADD CONSTRAINT scores_results_fixture_id_fkey FOREIGN KEY (fixture_id) REFERENCES public.fixtures(fixture_id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.scores_results DROP CONSTRAINT scores_results_fixture_id_fkey;
       public          postgres    false    230    228    3279            �           2606    16631 2   scores_results scores_results_winning_team_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.scores_results
    ADD CONSTRAINT scores_results_winning_team_id_fkey FOREIGN KEY (winning_team_id) REFERENCES public.teams(team_id) ON DELETE SET NULL;
 \   ALTER TABLE ONLY public.scores_results DROP CONSTRAINT scores_results_winning_team_id_fkey;
       public          postgres    false    3273    230    224            �           2606    16570    teams teams_coach_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_coach_id_fkey FOREIGN KEY (coach_id) REFERENCES public.coach(coach_id) ON DELETE SET NULL;
 C   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_coach_id_fkey;
       public          postgres    false    3271    224    222            �           2606    16575    teams teams_group_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id) ON DELETE SET NULL;
 C   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_group_id_fkey;
       public          postgres    false    224    220    3267            �           2606    16565    teams teams_institution_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution(institution_id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_institution_id_fkey;
       public          postgres    false    224    216    3263            �           2606    16580    teams teams_tournament_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_tournament_id_fkey;
       public          postgres    false    3265    218    224            �   {   x�3�LL��̃�%�e�ŉz����*FI*�F*��žA��e�Y�z��nNyn>�������!ɕ�%���%�偁�^U������%�FF&���Ɔ
F�V&&VƖzfFƆFf\1z\\\ �"�      }      x�3�t��2���s�2������� (Zs      �      x������ � �      �      x������ � �      {      x�3�t�Pp�4�2���8��b���� [��      w   P   x�3�
��K��I�2�r��)-N�N�2�t�qr����K/�2��u	���M�+N�2�t� �32K�b���� ���      �   (   x�3�t��,�H�4���41�R���y)C#�=... ��]      �      x������ � �         ?   x�3�qu�Up�4�?N#.c��3�1�E9CRs�j����ĝ���"�0&F��� /��      y   C   x�3�qQ��s�u��4202�54�50�3���9�B���|a
�t��L#.B
b���� 3�o     