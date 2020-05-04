package com.ezequiel.router.classes;

import android.content.Context;
import android.util.Log;

import com.ezequiel.router.exceptions.NotFoundException;
import com.ezequiel.router.interfaces.Backend;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.RoutePoint;
import com.ezequiel.router.interfaces.TSPSolver;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class TSPJson implements TSPSolver {

    private static Backend backend;
    private RouteBuilderListener listener;

    public TSPJson(Context context) {
        backend = FlaskBackend.getInstance(context);
    }

    @Override
    public Route solveTSP(List<String> addresses, RouteBuilderListener listener) {
        this.listener = listener;

        // Building JSONObject for the backend
        JSONObject json = new JSONObject();
        JSONArray jsonArray = new JSONArray();

        for (String a : addresses) {
            jsonArray.put(a);
        }

        try {
            json.put("addresses", jsonArray);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        backend.postJson(json, new Backend.JsonRequestListener() {

            @Override
            public void onResponse(JSONObject json) {
                buildRoute(json);
            }

            @Override
            public void onFailure(Exception e) {
                // TODO
                Log.e("ERROR", e.getMessage() + " ");
            }
        });

        return null;
    }

    /**
     * Building a ListRoute using CoordRoutePoints with the given json
     * json contains: orderedCoords, orderedAddresses and the route with coordinates
     *
     * @param json response from database
     */
    private void buildRoute(JSONObject json) {
        Route r = new ListRoute();

        List<RoutePoint> orderedRoutePoints = new ArrayList<>();
        double length = 0;

        try {
            JSONArray arrayOrderedAddresses = (JSONArray) json.get("orderedAddresses");
            JSONArray arrayOrderedCoords = (JSONArray) json.get("orderedCoords");
            JSONArray arrayRoute = (JSONArray) json.get("route");
            length = Double.parseDouble(json.get("length").toString());

            // Ordered coords and addresses retrieving
            JSONArray aux;
            double[] latlon;
            String address;
            for (int i = 0; i < arrayOrderedCoords.length(); i++) {
                // address
                address = arrayOrderedAddresses.get(i).toString();

                // [lat, lon]
                aux = (JSONArray) arrayOrderedCoords.get(i);
                latlon = new double[]{
                        Double.parseDouble(aux.get(0).toString()),
                        Double.parseDouble(aux.get(1).toString())};

                RoutePoint routePoint = new CoordRoutePoint(
                        address,
                        latlon[0],
                        latlon[1]);

                orderedRoutePoints.add(routePoint);
                r.addRoutePoint(routePoint);
            }

            // Route retrieving and insertion into the Route currently being built
            RoutePoint start = orderedRoutePoints.get(0);
            RoutePoint end = orderedRoutePoints.get(1);
            List<RoutePoint> partialRoute = new ArrayList<>();

            for (int i = 0; i < arrayRoute.length() && end != null; i++) {

                // aux contains [lat, lon]
                aux = (JSONArray) arrayRoute.get(i);
                latlon = new double[]{
                        Double.parseDouble(aux.get(0).toString()),
                        Double.parseDouble(aux.get(1).toString())};
                RoutePoint p = new CoordRoutePoint(null, latlon[0], latlon[1]);

                if (p.equals(end)) {
                    // Reached the partial end
                    // an old partial route is dead and a new one is born ;)
                    partialRoute.add(0, start);
                    partialRoute.add(end);

                    r.addRouteBetween(start, end, partialRoute);

                    partialRoute = new ArrayList<>();
                    start = end;
                    end = r.getNext(end);

                } else {
                    // Simply add the RoutePoint to partial Route
                    partialRoute.add(p);
                }

            }

        } catch (JSONException | NotFoundException e) {
            e.printStackTrace();
        }

        listener.onRouteBuilt(r);
    }
}
