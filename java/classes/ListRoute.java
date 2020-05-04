package com.ezequiel.router.classes;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.ezequiel.router.exceptions.NotFoundException;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.RoutePoint;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Route implementation using a list
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
     * Maps RoutePoint to lists positions
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
        routes.add(null);
    }

    @Override
    public List<RoutePoint> getRoutePoints() {
        return this.pointList;
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
        if (!r.get(0).equals(start) || !r.get(r.size() - 1).equals(end)) {
            throw new NotFoundException("Route doesnt start or end with the given coordinates");
        }

        routes.add(pointList.indexOf(start), r);
    }

    @Override
    public List<RoutePoint> getRouteBetween(RoutePoint start, @Nullable RoutePoint end) throws NotFoundException {
        if (!pointList.contains(start)) {
            throw new NotFoundException("Route doesn't have: " + start);
        }
        if (end != null && !pointList.contains(end)) {
            throw new NotFoundException("Route doesn't have: " + end);
        }

        if (end == null || end.equals(this.getNext(start))) {
            return this.routes.get(pointList.indexOf(start));
        }

        int indexStart, indexEnd;
        indexStart = pointList.indexOf(start);
        indexEnd = pointList.indexOf(end);
        if (indexEnd <= indexStart) {
            return null;
        }

        List<RoutePoint> output = new ArrayList<>();
        for (int i = indexStart; i < indexEnd; i++) {
            output.addAll(routes.get(i));
        }

        return output;
    }

    @Override
    public Iterator<RoutePoint> iterator() {
        return new RouteIterator(this);
    }

    @NonNull
    @Override
    public String toString() {
        return super.toString();
    }
}

