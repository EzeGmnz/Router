package com.ezequiel.router.classes;

import com.ezequiel.router.interfaces.JsonManager;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.RoutePoint;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

/**
 * Custom JsonManager implementation for Route serialization
 * and deserialization
 */
public class RouteJsonManager implements JsonManager<MatrixRoute> {
    private Gson gson;

    public RouteJsonManager() {
        GsonBuilder builder = new GsonBuilder();

        RuntimeTypeAdapterFactory<Route> adapterRoute = RuntimeTypeAdapterFactory.of(Route.class, "type")
                .registerSubtype(MatrixRoute.class, "MatrixRoute");

        RuntimeTypeAdapterFactory<RoutePoint> adapterRoutePoint = RuntimeTypeAdapterFactory.of(RoutePoint.class, "type")
                .registerSubtype(CoordRoutePoint.class, "CoordRoutePoint");

        builder.registerTypeAdapterFactory(adapterRoute);
        builder.registerTypeAdapterFactory(adapterRoutePoint);

        this.gson = builder.create();
    }

    @Override
    public String toJson(MatrixRoute object) {
        return this.gson.toJson(object);
    }

    public MatrixRoute fromJson(String json) {
        return this.gson.fromJson(json, MatrixRoute.class);
    }

}
