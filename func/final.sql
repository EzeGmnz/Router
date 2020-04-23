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
DROP FUNCTION routebetween(bigint,bigint);
CREATE OR REPLACE FUNCTION routeBetween(source bigint, target bigint) RETURNS TABLE(g geometry, length float) AS
$$ 		
	SELECT the_geom, length_m
	FROM pgr_dijkstra('SELECT gid AS id, source, target, cost, reverse_cost FROM ways', source, target, true) AS r 
	LEFT JOIN ways AS w ON r.edge = w.gid; 
$$
LANGUAGE SQL;

/*
	Requires arrays to be of the same length. Will be matched index to index
	input: $1 latitudes, $2 lonitudes. 
*/
CREATE OR REPLACE FUNCTION routeBetweenShell(FLOAT[], FLOAT[]) RETURNS TABLE(g geometry) AS
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
		start_id := (select nearestGeo($1[6], $2[6])),
		end_id :=  (select nearestGeo($1[5], $2[5])),
		randomize := false)
	),
	tuples AS (
			SELECT r1.node AS source, r2.node AS target
			FROM routeseq AS r1
			JOIN routeseq AS r2 on r2.seq = r1.seq + 1
			WHERE r2.seq < (SELECT MAX(seq) FROM routeseq))

	select routebetween(source, target) from tuples
$$
LANGUAGE SQL;

/* SAMPLE USAGE .9 excecution time*/
select * from routebetweenshell(ARRAY[-38.704577,-38.706225, -38.704718, -38.706823, -38.712674, -38.719969, -38.719758, -38.710612, -38.716506, -38.695943, -38.780062, -38.710363, -38.750126], 
								ARRAY[-62.272677,-62.265388, -62.27653, -62.271098, -62.270221, -62.268381, -62.25299, -62.255185, -62.272909, -62.215489, -62.267788, -62.325136, -62.178358]);