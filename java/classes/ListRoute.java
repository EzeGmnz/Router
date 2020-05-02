package com.ezequiel.router.classes;

import androidx.annotation.NonNull;

import com.ezequiel.router.exceptions.NotFoundException;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.RoutePoint;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Route implementation using matrix
 * Uses CoordRoutePoint to represent points
 */
public class ListRoute implements Route {

    /**
     * Timestamp of the creation of the routes
     */
    private long timestamp;

    /**
     * Each list of RoutePoints contains the routes to the
     * next routePoint according to its index
     */
    private List<List<RoutePoint>> routes;

    /**
     * Maps RoutePoint to matrix entries using list positions
     * Needs to be reordered when TSP problem is solved
     */
    private List<RoutePoint> pointList;

    public ListRoute() {
        this.routes = new ArrayList<>();
        this.pointList = new ArrayList<>();
        this.timestamp = new Timestamp(System.currentTimeMillis()).getTime();
    }

    @Override
    public void addRoutePoint(RoutePoint p) {
        pointList.add(p);
    }

    // Should this be on the implementation of the iterator?
    @Override
    public RoutePoint getNext(RoutePoint r) throws NotFoundException {
        if (!pointList.contains(r)) {
            throw new NotFoundException("Route doesn't have: " + r);
        }

        int indexLooking = pointList.indexOf(r);
        if (indexLooking == pointList.size() - 1) {
            return null;
        }
        return pointList.get(indexLooking + 1);
    }

    @Override
    public void addRouteBetween(RoutePoint start, RoutePoint end, List<RoutePoint> r) throws NotFoundException {
        if (!pointList.contains(start)) {
            throw new NotFoundException("Route doesn't have: " + start);
        }
        if (!pointList.contains(end)) {
            throw new NotFoundException("Route doesn't have: " + end);
        }

        routes.add(r);
    }

    @Override
    public Iterator iterator() {
        return new RouteIterator(this);
    }

    public List<RoutePoint> getPointList() {
        return pointList;
    }

    @NonNull
    @Override
    public String toString() {
        return super.toString();
    }
}

