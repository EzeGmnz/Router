package com.ezequiel.router.interfaces;

import java.util.List;

/**
 * Handles the iteration through a Route for navigation
 */
public interface RouteInteractor {

    /**
     * Returns next list of RoutePoints starting from end
     *
     * @param end starting point of the next section
     * @return list of RoutePoints conforming the route
     */
    List<RoutePoint> getNextSection(RoutePoint end);

}
