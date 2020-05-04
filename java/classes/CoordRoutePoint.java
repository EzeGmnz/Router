package com.ezequiel.router.classes;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.ezequiel.router.interfaces.RoutePoint;

/**
 * RoutePoint implementations using coordinates
 */
public class CoordRoutePoint extends RoutePoint {

    /**
     * Lattitude and Longitude
     */
    private double lat;
    private double lon;

    public CoordRoutePoint(@Nullable String address, double lat, double lon) {
        super(address);
        this.lat = lat;
        this.lon = lon;
    }

    public double getLat() {
        return this.lat;
    }

    public double getLon() {
        return this.lon;
    }

    public boolean equals(Object obj) {
        try {
            return ((CoordRoutePoint) obj).getLat() == this.lat && ((CoordRoutePoint) obj).getLon() == this.lon;
        } catch (ClassCastException e) {
            e.printStackTrace();
        }
        return false;
    }

    @NonNull
    @Override
    public String toString() {
        return super.toString() + " lat:" + lat + " lon:" + lon;
    }
}
