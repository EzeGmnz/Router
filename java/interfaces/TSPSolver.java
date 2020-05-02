package com.ezequiel.router.interfaces;

import java.util.List;

/**
 * TSP solving method abstractions
 * uses Routes and RoutePoints
 */
public interface TSPSolver {

    /**
     * Solves the TSP problem using the given Route as its points
     *
     * @param addresses addresses to solve TSP for
     * @param listener  interface to be called when the route is ready (may be needed when working asynchronously)
     * @return Route with its route solved
     */
    Route solveTSP(List<String> addresses, RouteBuilderListener listener);

    public interface RouteBuilderListener {

        public void onRouteBuilt(Route r);

    }

}
