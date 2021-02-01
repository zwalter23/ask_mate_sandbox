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
    image text
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
    edited_count integer
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
    image text
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
    registration_time timestamp with time zone
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

COPY public.answer (id, submission_time, vote_number, question_id, message, image) FROM stdin;
11	2021-01-21 23:12:05	0	10	There are three different implementations: pseudo-elements, pseudo-classes, and nothing.\r\n\r\nWebKit, Blink (Safari, Google Chrome, Opera 15+) and Microsoft Edge are using a pseudo-element: ::-webkit-input-placeholder. [Ref]\r\nMozilla Firefox 4 to 18 is using a pseudo-class: :-moz-placeholder (one colon). [Ref]\r\nMozilla Firefox 19+ is using a pseudo-element: ::-moz-placeholder, but the old selector will still work for a while. [Ref]\r\nInternet Explorer 10 and 11 are using a pseudo-class: :-ms-input-placeholder. [Ref]\r\nApril 2017: Most modern browsers support the simple pseudo-element ::placeholder [Ref]	
12	2021-01-21 23:13:43	0	10	CSS selectors\r\nUser agents are required to ignore a rule with an unknown selector. See Selectors Level 3:\r\n\r\na group of selectors containing an invalid selector is invalid.\r\n\r\nSo we need separate rules for each browser. Otherwise the whole group would be ignored by all browsers.\r\n\r\n	
13	2021-01-21 23:24:46	0	10		id<built-in function id>wallhaven-nev69l.jpg
15	2021-01-22 00:04:14	1	14	It’s a holdover from the Netscape days:\r\n\r\nMissing digits are treated as 0[...]. An incorrect digit is simply interpreted as 0. For example the values #F0F0F0, F0F0F0, F0F0F, #FxFxFx and FxFxFx are all the same.\r\n\r\nIt is from the blog post A little rant about Microsoft Internet Explorer's color parsing which covers it in great detail, including varying lengths of color values, etc.	
17	2021-01-22 09:45:33	0	15	Answer of anything to anything	
19	2021-01-22 16:36:35	0	2	Noice	id<built-in function id>wallhaven-4222l6.jpg
8	2021-01-21 19:51:30	2	7	Egestas purus viverra accumsan in nisl nisi scelerisque eu ultrices. Morbi tristique senectus et netus. Lacinia quis vel eros donec ac.	id<built-in function id>wallhaven-0wgv7r.jpg
9	2021-01-21 20:07:59	0	2	I had the same extreme irritating problem myself since the script did not take any notice of my styelsheet. So I wrote:\r\n\r\n<ul style="list-style-type: none;">\r\nThat did not work. So, in addition, I wrote:\r\n\r\n<li style="list-style-type: none;">\r\nVoila! it worked!	
7	2021-01-21 19:48:32	2	7	Elit sed vulputate mi sit amet mauris commodo. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Vitae congue eu consequat ac felis. Eu tincidunt tortor aliquam nulla facilisi. Purus semper eget duis at tellus at. Nec sagittis aliquam malesuada bibendum arcu vitae. Nunc scelerisque viverra mauris in aliquam sem fringilla. Mauris a diam maecenas sed enim.	
10	2021-01-21 23:07:32	2	8	According to Can I use, the user-select is currently supported in all browsers except Internet Explorer 9 and its earlier versions (but sadly still needs a vendor prefix).\r\n\r\n	
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count) FROM stdin;
1	0	\N	Please clarify the question as it is too vague!	2017-05-01 05:49:00	\N
7	2	\N	Elit sed vulputate mi sit amet mauris commodo. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Vitae congue eu consequat ac felis. Eu tincidunt tortor aliquam nulla facilisi. Purus semper eget duis at tellus at. Nec sagittis aliquam malesuada bibendum arcu vitae. Nunc scelerisque viverra mauris in aliquam sem fringilla. 	2021-01-21 19:03:37	0
8	2	\N	Elit sed vulputate mi sit amet mauris commodo. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Vitae congue eu consequat ac felis. Eu tincidunt tortor aliquam nulla facilisi. Purus semper eget duis at tellus at. Nec sagittis aliquam malesuada bibendum arcu vitae. Nunc scelerisque viverra mauris in aliquam sem fringilla. 	2021-01-21 19:28:44	0
9	7	\N	Aliquam nulla facilisi cras fermentum odio eu. Nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque.	2021-01-21 19:46:09	0
10	\N	7	Amet consectetur adipiscing elit ut aliquam purus sit.	2021-01-21 19:48:56	0
11	7	\N	Id donec ultrices tincidunt arcu non sodales neque sodales. Gravida rutrum quisque non tellus orci ac auctor augue mauris. Eu mi bibendum neque egestas congue.	2021-01-21 19:50:38	0
12	\N	7	Aliquam purus sit amet luctus venenatis. Pellentesque id nibh tortor id aliquet lectus proin nibh. Amet tellus cras adipiscing enim eu turpis egestas pretium.	2021-01-21 19:51:01	0
13	8	\N	Note that user-select is in standardization process (currently in a W3C working draft). It is not guaranteed to work everywhere and there might be differences in implementation among browsers. Also browsers can drop support for it in the future.	2021-01-21 23:09:36	0
14	9	\N	Of those great answers, I just want to highlight that you must give "#inner" a "width", or it will be "100%", and you can't tell if it's already centered. 	2021-01-21 23:10:48	0
15	10	\N	Quick heads-up (not a solution, just a FYI): if I recall correctly, input[placeholder] just matches <input> tags that have a placeholder attribute, it doesn't match the placeholder attribute itself.	2021-01-21 23:12:25	0
16	10	\N	Yah, the thought crossed my mind that this may be like trying to style an element's "title" attribute. So +1 for thinking alike!	2021-01-21 23:12:39	0
17	10	\N	It’s not like the input selector because that selects all input elements. :placeholder-shown only selects input elements that are currently showing the placeholder, allowing you to style those elements only, and effectively style the placeholder text. What are you trying to say? 	2021-01-21 23:12:57	0
18	\N	13	Nice picture	2021-01-21 23:25:07	0
20	\N	15	As a side note: dont use bgcolor. Use CSS background!	2021-01-22 00:05:05	0
22	13	\N	dsftzuio	2021-01-22 12:34:44	0
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image) FROM stdin;
1	2017-04-29 09:19:00	28	2	Wordpress loading multiple jQuery Versions	I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)	images/image1.png
2	2017-05-01 10:41:00	1384	9	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\r\n	\N
0	2017-04-28 08:29:00	37	8	How to make lists in Python?	I am totally new to this, any hints?	\N
9	2021-01-21 23:10:20	4	6	How to horizontally center an element	How can I horizontally center a <div> within another <div> using CSS?\r\n\r\n<div id="outer">\r\n  <div id="inner">Foo foo</div>\r\n</div>	
14	2021-01-22 00:03:47	3	3	Why does HTML think “chucknorris” is a color?	How come certain random strings produce colors when entered as background colors in HTML? For example:\r\n\r\n<body bgcolor="chucknorris"> test </body>\r\nExpand snippet\r\n...produces a document with a red background across all browsers and platforms.\r\n\r\nInterestingly, while chucknorri produces a red background as well, chucknorr produces a yellow background.\r\n\r\n	
15	2021-01-22 09:18:36	9	6	How do I disable the resizable property of a textarea?	I want to disable the resizable property of a textarea.\r\n\r\nCurrently, I can resize a textarea by clicking on the bottom right corner of the textarea and dragging the mouse. How can I disable this?	
8	2021-01-21 23:07:12	0	1	How to disable text selection highlighting	For anchors that act like buttons (for example Questions, Tags, Users, etc. which are located on the top of the Stack Overflow page) or tabs, is there a CSS standard way to disable the highlighting effect if the user accidentally selects the text?\r\n\r\nI realize that this could be done with JavaScript and a little googling yielded the Mozilla-only -moz-user-select option.\r\n\r\nIs there a standard-compliant way to accomplish this with CSS, and if not, what is the "best practice" approach?	
10	2021-01-21 23:11:35	2	2	Change an HTML5 input's placeholder color with CSS	Chrome supports the placeholder attribute on input[type=text] elements (others probably do too).\r\n\r\nBut the following CSS doesn't do anything to the placeholder's value:\r\n\r\ninput[placeholder], [placeholder], *[placeholder] {\r\n    color: red !important;\r\n}\r\n<input type="text" placeholder="Value">	
7	2021-01-21 19:37:17	8	2	Aliquam nulla facilisi cras fermentum odio eu. Nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque.	Elit sed vulputate mi sit amet mauris commodo. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Vitae congue eu consequat ac felis. Eu tincidunt tortor aliquam nulla facilisi. Purus semper eget duis at tellus at. Nec sagittis aliquam malesuada bibendum arcu vitae. Nunc scelerisque viverra mauris in aliquam sem fringilla. 	
13	2021-01-21 23:32:32	3	1	Set cellpadding and cellspacing in CSS?	In an HTML table, the cellpadding and cellspacing can be set like this:\r\n\r\n<table cellspacing="1" cellpadding="1">\r\nHow can the same be accomplished using CSS?	id<built-in function id>wallhaven-4222l6.jpg
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
7	3
13	3
13	5
14	6
15	6
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
4	jquery
5	html
6	chucknorris
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: zwalter23
--

COPY public.users (id, email, password_hash, registration_time) FROM stdin;
1	dummy1@something.com	$2b$12$AkIqqWzfVKZvw3nOgxAV1..Lhig7VOEkbVOAYP7BKTZd1NAEwmwO6	2021-02-01 23:15:28+01
2	user1@domain.com	$2b$12$DSQVlSlytb9UhZdPkWEJsOmaC00l3gdZChgojQeSfxpb5v90EcvOa	2021-02-01 23:15:52+01
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.answer_id_seq', 19, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.comment_id_seq', 23, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.question_id_seq', 15, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.tag_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zwalter23
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: zwalter23
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- PostgreSQL database dump complete
--

