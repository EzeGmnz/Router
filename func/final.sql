CREATE OR REPLACE FUNCTION nearestGeo(lat float, lon float) RETURNS bigint AS 
$$
	DECLARE output bigint;
	BEGIN
			SELECT target INTO output
			FROM ways
			ORDER BY st_distance(the_geom, ST_SetSRID(ST_MakePoint($2, $1), 4326)) LIMIT 1;

			return output;
	END;
$$ 
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION route_between(source bigint, target bigint) RETURNS TABLE (
		node bigint,
		length double precision
) AS
$$
	BEGIN
		RETURN QUERY SELECT node, length_m as length
		FROM pgr_dijkstra('SELECT gid AS id, source, target, cost, reverse_cost FROM ways', source, target, true) AS r 
		LEFT JOIN ways AS w ON r.edge = w.gid; 
	END;
$$ 
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION getMatrixSQL(FLOAT[], FLOAT[]) RETURNS text AS
$$
	WITH coords (lat, lon) AS (
		select *
		from unnest($1, $2)
	)
	select ('SELECT * 
			FROM pgr_dijkstraCostMatrix(
										''SELECT gid AS id, source, target, cost, reverse_cost FROM ways'',
										(SELECT array_agg(nearestGeo(lat, lon)) FROM (select * from unnest(' 
													|| (select 	concat('ARRAY[', string_agg(lat::text, ','), ']', ',', 
																concat('ARRAY[', string_agg(lon::text, ','), ']'))
														from coords) ||')) as x(lat, lon)),
										directed := false)');
$$
LANGUAGE SQL;

/*
	Requires arrays to be of the same length. Will be matched index to index
	input: $1 latitudes, $2 longitudes. 
*/

CREATE OR REPLACE FUNCTION routeBetweenShell(FLOAT[], FLOAT[]) RETURNS TABLE(lat numeric, lon numeric, length float, o_lat float, o_lon float) AS
$$
	
	WITH 
	coords (lat, lon) AS (
		select *
		from unnest($1, $2)
	),
	coordsMap AS(
		select coords.lat as o_lat, coords.lon as o_lon, p.lat, p.lon
		from coords
		join public.ways_vertices_pgr as p on p.id = (select nearestGeo(coords.lat, coords.lon)) 
	),
	routeseq AS (
		SELECT * FROM pgr_TSP(	getMatrixSQL($1, $2),
							  	/* ARRAY INDEXES START AT 1 WTF*/
								start_id := (select nearestGeo($1[1], $2[1])),
								/*end_id := (select nearestGeo($1[5], $2[5])),*/
								randomize := false)
	),
	tuples AS (
		SELECT r1.node AS source, r2.node AS target
		FROM routeseq AS r1
		JOIN routeseq AS r2 on r2.seq = r1.seq + 1
		WHERE r2.seq < (SELECT MAX(seq) FROM routeseq)
	),
	route as(
		SELECT (routeBetween(source, target)).* from tuples
	)
	
	select p.lat, p.lon, length, c.o_lat, c.o_lon
	from route
	join public.ways_vertices_pgr as p on p.id = node
	left join coordsMap as c on p.lat = c.lat and p.lon = c.lon;
$$
LANGUAGE SQL;

select * from routeBetweenShell(ARRAY[-38.7062835877551, -38.7126883, -38.7035629, -38.7082947, -38.7126117, -38.7126117, -38.7126117, -38.71545756938776, -38.71077422653061, -38.72334768571429, -38.71331744285715], 
					ARRAY[-62.265117114285715, -62.2636853, -62.2771608, -62.2686823, -62.2615503, -62.2615503, -62.2615503, -62.27026347346939, -62.2722308755102, -62.2686434, -62.26512135510204])
