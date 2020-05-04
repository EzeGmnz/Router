package com.ezequiel.router.classes;

import com.ezequiel.router.exceptions.NotFoundException;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.RoutePoint;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Iterates each SECTION of the route, that is
 * returns the route between the next set of points
 */
public class RouteIterator implements Iterator<RoutePoint> {

    private Route route;
    private RoutePoint current;

    public RouteIterator(Route r) {
        this.route = r;
        this.current = route.getRoutePoints().get(0);
    }

    @Override
    public boolean hasNext() {
        return current != null;
    }

    @Override
    public RoutePoint next() throws NoSuchElementException {
        try {
            RoutePoint output = current;
            current = this.route.getNext(current);
            return output;
        } catch (NotFoundException e) {
            throw new NoSuchElementException("Iterator out of bounds");
        }
    }
}
