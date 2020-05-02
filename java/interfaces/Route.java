package com.ezequiel.router.interfaces;

import com.ezequiel.router.exceptions.NotFoundException;

import java.io.Serializable;
import java.util.Iterator;
import java.util.List;

/**
 * Route interface representing a route formed by RoutePoints
 * Assumes starting point is the first one
 */
public interface Route extends Iterable, Serializable {

    /**
     * Returns next point to visit, accordingly to the solved TSP
     *
     * @param r current point
     * @return the next point following r
     */
    RoutePoint getNext(RoutePoint r) throws NotFoundException;

    /**
     * Adds a route between start and end points. The list might have end point in it
     * if those points are adjacent
     *
     * @param start route's starting point
     * @param end   route's ending point
     * @param route list containing the RoutePoint forming the route
     * @throws NotFoundException if either start or end dont belong to this route
     */
    void addRouteBetween(RoutePoint start, RoutePoint end, List<RoutePoint> route) throws NotFoundException;

    /**
     * Adds a route point to this route
     *
     * @param p the RoutePoint to add
     */
    void addRoutePoint(RoutePoint p);

    /**
     * Returns iterator of this route (points)
     *
     * @return Iterator
     */
    Iterator iterator();

}
