--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    email character varying(70)
);


ALTER TABLE public.answer OWNER TO zwalter23;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: zwalter23
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO zwalter23;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zwalter23
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    email character varying(70)
);


ALTER TABLE public.comment OWNER TO zwalter23;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: zwalter23
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO zwalter23;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zwalter23
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    email character varying(70)
);


ALTER TABLE public.question OWNER TO zwalter23;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: zwalter23
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO zwalter23;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zwalter23
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO zwalter23;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO zwalter23;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: zwalter23
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO zwalter23;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zwalter23
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email text,
    password_hash text,
    registration_time timestamp with time zone,
    question_count integer DEFAULT 0,
    answer_count integer DEFAULT 0,
    comment_count integer DEFAULT 0,
    reputation integer DEFAULT 0
);


ALTER TABLE public.users OWNER TO zwalter23;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: zwalter23
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO zwalter23;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zwalter23
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, email) FROM stdin;
4	2021-02-02 17:14:05	0	2	I am tester		tester@test.com
3	2021-02-02 17:11:56	4	1	Test		valaki@valahol.hu
2	2021-02-02 17:11:23	5	3	Yes		valaki@valahol.hu
1	2021-02-02 16:59:46	3	1	This will be needed to the reputation test		dummy@stg.com
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, email) FROM stdin;
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, email) FROM stdin;
3	2021-02-02 16:58:17	4	1	How can I prevent SQL injection in PHP?	If user input is inserted without modification into an SQL query, then the application becomes vulnerable to SQL injection, like in the following example:\r\n\r\n		user1@domain.org
4	2021-02-02 16:59:03	1	5	Add a column with a default value to an existing table in SQL Server	How can I add a column with a default value to an existing table in SQL Server 2000 / SQL Server 2005?		dummy@stg.com
2	2021-02-02 16:56:51	3	4	What is the difference between “INNER JOIN” and “OUTER JOIN”?	Also how do LEFT JOIN, RIGHT JOIN and FULL JOIN fit in?\r\n\r\n		user1@domain.org
1	2021-02-02 16:54:24	4	3	How do I UPDATE from a SELECT in SQL Server?	In SQL Server, it is possible to insert rows into a table with an INSERT.. SELECT statement:\r\n\r\nINSERT INTO Table (col1, col2, col3)\r\nSELECT col1, col2, col3 \r\nFROM other_table \r\nWHERE sql = cool		valaki@valahol.hu
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.tag (id, name) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.users (id, email, password_hash, registration_time, question_count, answer_count, comment_count, reputation) FROM stdin;
4	tester@tester.test	$2b$12$bJSifxsAvpkLHelfnJ1z4uN85uKDV89LPEhv/eGsT6cPUaXpLVmh.	2021-02-02 17:15:24+01	0	0	0	0
3	user1@domain.org	$2b$12$X2hx.4clyxkFbMjUbl0q..LZ8oZDws3WlQ348P2MMaCC.3trZhblW	2021-02-02 16:55:22+01	0	0	0	5
1	valaki@valahol.hu	$2b$12$DpwM0dQNYFSvwTHvTBLH2uFYalaorQpE1b7V.T/T2bHxS8B0n6M46	2021-02-02 16:53:16+01	0	0	0	12
2	dummy@stg.com	$2b$12$FXQTwGJShnztvaL5Rlo.ve6lrIdx3gNNsW.ZyENwiNyPsRZiXRnHS	2021-02-02 16:54:59+01	0	0	0	7
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.answer_id_seq', 4, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.comment_id_seq', 1, false);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.question_id_seq', 4, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.tag_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

