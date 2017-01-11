PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "asociacion_banner" ("id" integer NOT NULL PRIMARY KEY, "imagen" varchar(500) NOT NULL, "pagina" varchar(10) NULL);
INSERT INTO "asociacion_banner" VALUES(1,'banners/banner_agenda.png','agenda');
INSERT INTO "asociacion_banner" VALUES(2,'banners/banner-convenios.jpg','convenios');
COMMIT;
