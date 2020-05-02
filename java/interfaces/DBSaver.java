package com.ezequiel.router.interfaces;

import java.util.List;

/**
 * Interface for saving the given element to persistent storage
 */
public interface DBSaver {

    /**
     * Saves a given sets of elements to persistent storage
     * overriding the already saved ones
     *
     * @param list list of elements to be saved
     */
    void save(List<Route> list);

}
