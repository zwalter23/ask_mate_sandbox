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


DROP TABLE IF EXISTS public.answer;
DROP TABLE IF EXISTS public.comment;
DROP TABLE IF EXISTS public.question;
DROP TABLE IF EXISTS public.users;


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
-- Name: users; Type: TABLE; Schema: public; Owner: zwalter23
--

CREATE TABLE public.users (
    id serial NOT NULL,
    email text,
    password_hash text,
    registration_time timestamp with time zone,
    question_count integer DEFAULT '0',
    answer_count integer DEFAULT '0',
    comment_count integer DEFAULT '0',
    reputation integer DEFAULT '0'
);


ALTER TABLE public.users OWNER TO zwalter23;

--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, email) FROM stdin;
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
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.users (id, email, password_hash, registration_time, question_count, answer_count, comment_count, reputation) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

