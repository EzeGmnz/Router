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

/*
	Requires arrays to be of the same length. Will be matched index to index
	input: $1 latitudes, $2 lonitudes. 
*/

CREATE OR REPLACE FUNCTION routeBetweenShell(FLOAT[], FLOAT[]) RETURNS TABLE(lat numeric, lon numeric, length float) AS
$$
	WITH 
	coords AS (
		SELECT *
		FROM unnest($1, $2)
	), 
	routeseq AS (
		SELECT * FROM pgr_TSP(
			'
				SELECT * 
				FROM pgr_dijkstraCostMatrix(''SELECT gid AS id, source, target, cost, reverse_cost FROM ways'',
											(SELECT array_agg(nearestGeo(lat, lon)) FROM coords),
											directed := false)
			'
		,
		start_id := (select nearestGeo($1[0], $2[0])),
		/*end_id :=  (select nearestGeo($1[5], $2[5])),*/
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
	select lat, lon, length
	from route
	join public.ways_vertices_pgr on id = node
$$
LANGUAGE SQL;