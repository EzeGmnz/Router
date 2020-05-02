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
public class MatrixRoute implements Route {

    /**
     * Timestamp of the creation of the route
     */
    private long timestamp;

    /**
     * Holds the route points on each matrix entry
     * and the route between, if exists, in each intersection, else null
     */
    private List<List<List<RoutePoint>>> route;

    /**
     * Maps RoutePoint to matrix entries using list positions
     * Needs to be reordered when TSP problem is solved
     */
    private List<RoutePoint> pointList;

    public MatrixRoute() {
        this.route = new ArrayList<>();
        this.pointList = new ArrayList<>();
        this.timestamp = new Timestamp(System.currentTimeMillis()).getTime();
    }

    @Override
    public void addRoutePoint(RoutePoint p) {
        int index = pointList.size();
        pointList.add(p);
        route.add(new ArrayList<List<RoutePoint>>());

        for (int i = 0; i < route.size(); i++) {
            route.get(index).add(new ArrayList<RoutePoint>());
        }

        for (int i = 0; i < index; i++) {
            route.get(i).add(new ArrayList<RoutePoint>());
        }
    }

    /*@Override
    public void removeRoutePoint(RoutePoint p) throws NotFoundException {
        if (!pointList.contains(p)) {
            throw new NotFoundException("Route doesn't have: " + p);
        }
        int index = pointList.indexOf(p);

        route.get(index).remove(index);
        route.remove(index);

        for (int i = 0; i < route.size(); i++) {
            route.get(i).remove(index);
        }

        pointList.remove(p);
    }*/

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
        int indexStart = pointList.indexOf(start);
        int indexEnd = pointList.indexOf(end);

        route.get(indexStart).get(indexEnd).clear();
        route.get(indexStart).get(indexEnd).addAll(r);
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
