CREATE OR REPLACE FUNCTION nearestGeo(p geometry) RETURNS integer AS 
$$
	DECLARE output bigint;
	BEGIN
			select target INTO output
			from ways
			order by st_distance(the_geom, p) limit 1;

			return output;
	END;
$$ 
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION routeBetween(source bigint, target bigint) RETURNS TABLE(g geometry) AS
$$ 		
	SELECT the_geom
	FROM pgr_dijkstra('SELECT gid AS id, source, target, cost, reverse_cost FROM ways', source, target, true) AS r 
	LEFT JOIN ways AS w ON r.edge = w.gid; 
$$
LANGUAGE SQL;

with routeseq as (SELECT * FROM pgr_TSP(
    $$
    	SELECT * 
		FROM pgr_dijkstraCostMatrix('SELECT gid as id, source, target, cost, reverse_cost FROM ways',
        							(select array_agg(nearestGeo(ST_SetSRID(ST_MakePoint(lon, lat), 4326))) from coords),
        							directed := false)
    $$,
	start_id := 339,
    randomize := false)),
tuples as (
		select r1.node as source, r2.node as target
	  	from routeseq as r1
	  	join routeseq as r2 on r2.seq = r1.seq + 1
	  	where r2.seq < (select MAX(seq) from routeseq))
		
select routeBetween(source, target) from tuples;
