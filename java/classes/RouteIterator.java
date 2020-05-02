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
public class RouteIterator implements Iterator {

    private Route route;
    private RoutePoint current;

    public RouteIterator(Route r) {
        this.route = r;
    }

    @Override
    public boolean hasNext() {
        try {
            return this.route.getNext(current) != null;
        } catch (NotFoundException e) {
            return false;
        }
    }

    @Override
    public Object next() throws NoSuchElementException {
        try {
            RoutePoint output = this.route.getNext(current);
            current = output;
            return output;
        } catch (NotFoundException e) {
            throw new NoSuchElementException("Iterator out of bounds");
        }
    }
}
