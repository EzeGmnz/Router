package com.ezequiel.router.interfaces;

import java.util.List;

/**
 * Retrieving functionality
 */
public interface DBRetriever {

    /**
     * Get from storage all the elements saved of type <E>
     *
     * @return List of elements of type <E>
     */
    List<Route> get();

}
