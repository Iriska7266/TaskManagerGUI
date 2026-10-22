--
-- PostgreSQL database dump
--

\restrict aaQsqW4s45iDAbSeR1Nkwg9HK3DEHmEP8OQgVKAdWTRWGzfu0bmwlIB4vta0cua

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: action_checker(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.action_checker() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	f_details text;
BEGIN
	CASE TG_TABLE_NAME
		WHEN 'accounts' THEN
			CASE TG_OP
				WHEN 'INSERT' THEN f_details := format('New user account. ID: %L; login: %L', NEW.u_id, NEW.u_login);
				WHEN 'UPDATE' THEN f_details := format('Updated information for user %L', OLD.u_login);
				WHEN 'DELETE' THEN f_details := format('Deleted user %L', OLD.u_login);
			END CASE;
		WHEN 'tasks' THEN
			CASE TG_OP
				WHEN 'INSERT' THEN f_details := format('New task. ID: %L; title: %L', NEW.t_id, NEW.title);
				WHEN 'UPDATE' THEN f_details := format('Updated task %L', OLD.t_id);
				WHEN 'DELETE' THEN f_details := format('Deleted task. ID: %L; title: %L', OLD.t_id, OLD.title);
			END CASE;
	END CASE;

	INSERT INTO actions_log(action_type, tname, details)
	VALUES (TG_OP, TG_TABLE_NAME, f_details);

	RETURN NULL;
END;
$$;


ALTER FUNCTION public.action_checker() OWNER TO postgres;

--
-- Name: add_task(integer, text, text, timestamp with time zone, timestamp with time zone, boolean); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.add_task(f_user_id integer, f_title text, f_content text, f_created_at timestamp with time zone, f_expires_at timestamp with time zone, f_status boolean) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	f_t_id integer;
BEGIN
	-- Task
	INSERT INTO tasks(title, t_content, created_at, expires_at, status)
	VALUES (f_title, f_content, f_created_at, f_expires_at, f_status)
	RETURNING t_id INTO f_t_id;

	-- User-task
	INSERT INTO user_tasks
	VALUES (f_user_id, f_t_id);

	RETURN f_t_id;
EXCEPTION
	WHEN foreign_key_violation THEN
		RETURN -1;
END;
$$;


ALTER FUNCTION public.add_task(f_user_id integer, f_title text, f_content text, f_created_at timestamp with time zone, f_expires_at timestamp with time zone, f_status boolean) OWNER TO postgres;

--
-- Name: add_user(text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.add_user(f_u_login text, f_u_password_hash text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	f_u_id integer;
BEGIN
	INSERT INTO accounts(u_login, u_password_hash)
	VALUES (f_u_login, f_u_password_hash)
	RETURNING u_id INTO f_u_id;

	RETURN f_u_id;
EXCEPTION
	WHEN unique_violation THEN
		RETURN -1;
END;
$$;


ALTER FUNCTION public.add_user(f_u_login text, f_u_password_hash text) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    u_id integer NOT NULL,
    u_login text NOT NULL,
    u_password_hash text NOT NULL,
    created_at timestamp(0) with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_u_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts ALTER COLUMN u_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.accounts_u_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: actions_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actions_log (
    action_id integer NOT NULL,
    action_type character varying(6) NOT NULL,
    tname character varying(50) CONSTRAINT actions_log_table_name_not_null NOT NULL,
    action_time timestamp(0) with time zone DEFAULT now() NOT NULL,
    details text NOT NULL
);


ALTER TABLE public.actions_log OWNER TO postgres;

--
-- Name: actions_log_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.actions_log ALTER COLUMN action_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.actions_log_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    t_id integer NOT NULL,
    title text NOT NULL,
    t_content text CONSTRAINT tasks_content_not_null NOT NULL,
    created_at timestamp(0) with time zone DEFAULT now() NOT NULL,
    expires_at timestamp(0) with time zone NOT NULL,
    status boolean DEFAULT false NOT NULL
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_t_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tasks ALTER COLUMN t_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.tasks_t_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_tasks (
    u_id integer NOT NULL,
    t_id integer NOT NULL
);


ALTER TABLE public.user_tasks OWNER TO postgres;

--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (u_id, u_login, u_password_hash, created_at) FROM stdin;
1	Test	Test	2026-07-28 13:35:01+05
\.


--
-- Data for Name: actions_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actions_log (action_id, action_type, tname, action_time, details) FROM stdin;
1	INSERT	accounts	2026-07-28 13:35:01+05	New user account. ID: '1'; login: 'Test'
2	INSERT	tasks	2026-07-28 13:37:23+05	New task. ID: '1'; title: 'Learn SQLAlchemy'
3	INSERT	tasks	2026-07-28 13:39:01+05	New task. ID: '2'; title: 'Practice with MVC pattern'
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (t_id, title, t_content, created_at, expires_at, status) FROM stdin;
1	Learn SQLAlchemy	1. Google; 2. Read documentation; 3. Code; 4. Solve the problems	2026-07-28 13:37:23+05	2026-09-01 09:00:00+05	f
2	Practice with MVC pattern	1. Read articles & presentations; 2. Code; 3. Solve the problems; 4. Profit	2026-07-28 13:39:01+05	2026-09-01 09:00:00+05	f
\.


--
-- Data for Name: user_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_tasks (u_id, t_id) FROM stdin;
1	1
1	2
\.


--
-- Name: accounts_u_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_u_id_seq', 1, true);


--
-- Name: actions_log_action_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actions_log_action_id_seq', 3, true);


--
-- Name: tasks_t_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_t_id_seq', 2, true);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (u_id);


--
-- Name: actions_log actions_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions_log
    ADD CONSTRAINT actions_log_pkey PRIMARY KEY (action_id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (t_id);


--
-- Name: accounts unique_u_login; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT unique_u_login UNIQUE (u_login);


--
-- Name: user_tasks user_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT user_tasks_pkey PRIMARY KEY (u_id, t_id);


--
-- Name: accounts tg_action_checker; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tg_action_checker AFTER INSERT OR DELETE OR UPDATE ON public.accounts FOR EACH ROW EXECUTE FUNCTION public.action_checker();


--
-- Name: tasks tg_action_checker; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tg_action_checker AFTER INSERT OR DELETE OR UPDATE ON public.tasks FOR EACH ROW EXECUTE FUNCTION public.action_checker();


--
-- Name: user_tasks t_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT t_id_fk FOREIGN KEY (t_id) REFERENCES public.tasks(t_id) NOT VALID;


--
-- Name: user_tasks u_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT u_id_fk FOREIGN KEY (u_id) REFERENCES public.accounts(u_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

\unrestrict aaQsqW4s45iDAbSeR1Nkwg9HK3DEHmEP8OQgVKAdWTRWGzfu0bmwlIB4vta0cua

