-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: auction | type: DATABASE --
-- DROP DATABASE IF EXISTS auction;
CREATE DATABASE auction;
-- ddl-end --


-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user" (
	id serial NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
);
-- ddl-end --

-- object: public.auction | type: TABLE --
-- DROP TABLE IF EXISTS public.auction CASCADE;
CREATE TABLE public.auction (
	id serial NOT NULL,
	id_user integer NOT NULL,
	creation_date date,
	CONSTRAINT auction_pk PRIMARY KEY (id)
);
-- ddl-end --

-- object: public.item | type: TABLE --
-- DROP TABLE IF EXISTS public.item CASCADE;
CREATE TABLE public.item (
	id serial NOT NULL,
	id_auction integer NOT NULL,
	CONSTRAINT item_pk PRIMARY KEY (id)
);
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE public.auction DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE public.auction ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES public."user" (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: auction_fk | type: CONSTRAINT --
-- ALTER TABLE public.item DROP CONSTRAINT IF EXISTS auction_fk CASCADE;
ALTER TABLE public.item ADD CONSTRAINT auction_fk FOREIGN KEY (id_auction)
REFERENCES public.auction (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.many_user_has_many_item | type: TABLE --
-- DROP TABLE IF EXISTS public.many_user_has_many_item CASCADE;
CREATE TABLE public.many_user_has_many_item (
	id_user integer NOT NULL,
	id_item integer NOT NULL,
	bid_date date NOT NULL,
	price smallint NOT NULL,
	CONSTRAINT many_user_has_many_item_pk PRIMARY KEY (id_user,id_item)
);
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_user_has_many_item DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE public.many_user_has_many_item ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES public."user" (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: item_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_user_has_many_item DROP CONSTRAINT IF EXISTS item_fk CASCADE;
ALTER TABLE public.many_user_has_many_item ADD CONSTRAINT item_fk FOREIGN KEY (id_item)
REFERENCES public.item (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


