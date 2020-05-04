package com.ezequiel.router.interfaces;

import androidx.annotation.Nullable;

import com.ezequiel.router.exceptions.NotFoundException;

import java.io.Serializable;
import java.util.Iterator;
import java.util.List;

/**
 * Route interface representing a route formed by RoutePoints
 * Assumes starting point is the first one
 */
public interface Route extends Iterable<RoutePoint>, Serializable {

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
     * @throws NotFoundException if either start or end dont belong to this route or if route
     *                           DOES NOT starts or end with start and end respectively
     */
    void addRouteBetween(RoutePoint start, RoutePoint end, List<RoutePoint> route) throws NotFoundException;

    /**
     * Returns List<RoutePoint> between given start and end point
     *
     * @param start starting RoutePoint
     * @param end   ending RoutePoint, when null the route between start and its next will be returned
     * @return List<RoutePoint> with the route between the given points, null if no route exists
     * @throws NotFoundException if either start or end weren't found
     */
    List<RoutePoint> getRouteBetween(RoutePoint start, @Nullable RoutePoint end) throws NotFoundException;

    /**
     * Adds a stop route point to this route
     *
     * @param p the RoutePoint to add
     */
    void addRoutePoint(RoutePoint p);

    /**
     * Return list of all stop RoutePoints
     *
     * @return List<RoutePoint>
     */
    List<RoutePoint> getRoutePoints();

    /**
     * Returns iterator of this route (points)
     *
     * @return Iterator
     */
    Iterator<RoutePoint> iterator();

}
