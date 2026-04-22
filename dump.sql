--
-- PostgreSQL database dump
--

\restrict F3hHpsDafUNnyOjDupLiDw9ZkPuuC1ZHlvXK3dJEOUahmCotzYiQlFgFlFNknuC

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

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
-- Name: status_veiculo_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.status_veiculo_enum AS ENUM (
    'PRONTO',
    'EM_USO',
    'QUEBRADO',
    'IRREGULAR',
    'MANUTENCAO'
);


ALTER TYPE public.status_veiculo_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Documentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Documentos" (
    id integer NOT NULL,
    tipo character varying NOT NULL,
    data_emissao date NOT NULL,
    data_vencimento date NOT NULL,
    veiculo_id integer
);


ALTER TABLE public."Documentos" OWNER TO postgres;

--
-- Name: Documentos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Documentos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Documentos_id_seq" OWNER TO postgres;

--
-- Name: Documentos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Documentos_id_seq" OWNED BY public."Documentos".id;


--
-- Name: Motorista-veiculo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Motorista-veiculo" (
    id integer NOT NULL,
    veiculo_id integer,
    motorista_id integer,
    data_inicio date,
    data_fim date
);


ALTER TABLE public."Motorista-veiculo" OWNER TO postgres;

--
-- Name: Motorista-veiculo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Motorista-veiculo_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Motorista-veiculo_id_seq" OWNER TO postgres;

--
-- Name: Motorista-veiculo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Motorista-veiculo_id_seq" OWNED BY public."Motorista-veiculo".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: manutenções; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."manutenções" (
    id integer NOT NULL,
    valor double precision,
    tipo character varying NOT NULL,
    oficina_responsavel character varying NOT NULL,
    veiculo_id integer
);


ALTER TABLE public."manutenções" OWNER TO postgres;

--
-- Name: manutenções_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."manutenções_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."manutenções_id_seq" OWNER TO postgres;

--
-- Name: manutenções_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."manutenções_id_seq" OWNED BY public."manutenções".id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_tokens (
    id uuid NOT NULL,
    user_id integer,
    token character varying(255) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.password_reset_tokens OWNER TO postgres;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nome character varying NOT NULL,
    senha character varying NOT NULL,
    email character varying NOT NULL,
    telefone character varying NOT NULL,
    "função" character varying NOT NULL,
    ativo boolean,
    admin boolean
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: veiculos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.veiculos (
    id integer NOT NULL,
    modelo character varying NOT NULL,
    marca character varying NOT NULL,
    placa character varying NOT NULL,
    preco double precision,
    motorista_id integer,
    status public.status_veiculo_enum NOT NULL
);


ALTER TABLE public.veiculos OWNER TO postgres;

--
-- Name: veiculos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.veiculos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.veiculos_id_seq OWNER TO postgres;

--
-- Name: veiculos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.veiculos_id_seq OWNED BY public.veiculos.id;


--
-- Name: Documentos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Documentos" ALTER COLUMN id SET DEFAULT nextval('public."Documentos_id_seq"'::regclass);


--
-- Name: Motorista-veiculo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Motorista-veiculo" ALTER COLUMN id SET DEFAULT nextval('public."Motorista-veiculo_id_seq"'::regclass);


--
-- Name: manutenções id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."manutenções" ALTER COLUMN id SET DEFAULT nextval('public."manutenções_id_seq"'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: veiculos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.veiculos ALTER COLUMN id SET DEFAULT nextval('public.veiculos_id_seq'::regclass);


--
-- Data for Name: Documentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Documentos" (id, tipo, data_emissao, data_vencimento, veiculo_id) FROM stdin;
\.


--
-- Data for Name: Motorista-veiculo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Motorista-veiculo" (id, veiculo_id, motorista_id, data_inicio, data_fim) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
97109156b40b
\.


--
-- Data for Name: manutenções; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."manutenções" (id, valor, tipo, oficina_responsavel, veiculo_id) FROM stdin;
\.


--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.password_reset_tokens (id, user_id, token, expires_at, used, created_at) FROM stdin;
8a3acd1e-f4fe-4c4a-93d1-00cf8575b455	1	8d64ed9b9f9a6204047bc7de9caf11e04a2dc9b78969682fa09a7d735ebcc0db	2026-04-22 00:02:17.530217	t	2026-04-21 23:32:17.532565
c822f342-f081-46e3-86da-d4d425956332	1	edf301558a3c3681da77a582872677a32413f77f94b787e6ff206af0f339998a	2026-04-22 00:19:33.104002	t	2026-04-21 23:49:33.106071
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nome, senha, email, telefone, "função", ativo, admin) FROM stdin;
1	teste	$2b$12$fwlz2ZZPuEVlWeG0n5AR../jpYu2MWx.Qmx2FQG82FoPs6cwbY2xW	teste@gmail.com	8899889	true	f	f
\.


--
-- Data for Name: veiculos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.veiculos (id, modelo, marca, placa, preco, motorista_id, status) FROM stdin;
\.


--
-- Name: Documentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Documentos_id_seq"', 1, false);


--
-- Name: Motorista-veiculo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Motorista-veiculo_id_seq"', 1, false);


--
-- Name: manutenções_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."manutenções_id_seq"', 1, false);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);


--
-- Name: veiculos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.veiculos_id_seq', 1, false);


--
-- Name: Documentos Documentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Documentos"
    ADD CONSTRAINT "Documentos_pkey" PRIMARY KEY (id);


--
-- Name: Motorista-veiculo Motorista-veiculo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Motorista-veiculo"
    ADD CONSTRAINT "Motorista-veiculo_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: manutenções manutenções_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."manutenções"
    ADD CONSTRAINT "manutenções_pkey" PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_token_key UNIQUE (token);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: veiculos veiculos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.veiculos
    ADD CONSTRAINT veiculos_pkey PRIMARY KEY (id);


--
-- Name: Documentos Documentos_veiculo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Documentos"
    ADD CONSTRAINT "Documentos_veiculo_id_fkey" FOREIGN KEY (veiculo_id) REFERENCES public.veiculos(id);


--
-- Name: Motorista-veiculo Motorista-veiculo_motorista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Motorista-veiculo"
    ADD CONSTRAINT "Motorista-veiculo_motorista_id_fkey" FOREIGN KEY (motorista_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- Name: Motorista-veiculo Motorista-veiculo_veiculo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Motorista-veiculo"
    ADD CONSTRAINT "Motorista-veiculo_veiculo_id_fkey" FOREIGN KEY (veiculo_id) REFERENCES public.veiculos(id);


--
-- Name: manutenções manutenções_veiculo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."manutenções"
    ADD CONSTRAINT "manutenções_veiculo_id_fkey" FOREIGN KEY (veiculo_id) REFERENCES public.veiculos(id);


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- Name: veiculos veiculos_motorista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.veiculos
    ADD CONSTRAINT veiculos_motorista_id_fkey FOREIGN KEY (motorista_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict F3hHpsDafUNnyOjDupLiDw9ZkPuuC1ZHlvXK3dJEOUahmCotzYiQlFgFlFNknuC

