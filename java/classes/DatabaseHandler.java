package com.ezequiel.router.classes;

import com.ezequiel.router.interfaces.DBRetriever;
import com.ezequiel.router.interfaces.DBSaver;
import com.ezequiel.router.interfaces.Route;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Saving and retrieveing from database handler
 */
public class DatabaseHandler {

    private static DatabaseHandler instance;

    /**
     * Retriever strategy
     */
    private DBRetriever retriever;

    /**
     * Saver strategy
     */
    private DBSaver saver;


    /**
     * Float to Route map for database administration
     * Ids change between sessions
     * Used for data consistency
     */
    private Map<Float, Route> idMap;

    /**
     * Last id used
     */
    private Float lastId;

    private DatabaseHandler() {
        // Singleton
        this.idMap = new HashMap<>();
        this.lastId = 0f;
    }

    /**
     * Singleton
     *
     * @return singleton instance
     */
    public static DatabaseHandler getInstance() {
        if (instance == null) {
            instance = new DatabaseHandler();
        }
        return instance;
    }

    /**
     * Gets all the user saved elements from database
     * Strategy method used for retrieving the elements
     * And assigns map to idMap for consistency check
     *
     * @return list of elements saved in persistent storage
     * using the saver method
     */
    public List<Route> get() {
        List<Route> output = this.retriever.get();
        this.idMap = new HashMap<>();
        for (Route e : output) {
            idMap.put(generateId(), e);
        }
        return this.retriever.get();
    }

    /**
     * Saves a given set of element into the database
     *
     * @param list elemento to be saved
     */
    public void save(List<Route> list) {
        for (Route e : list) {
            this.idMap.put(generateId(), e);
        }
        this.saver.save(list);
    }

    /**
     * Returns next id to be used
     * Method: successor of current maximum inter
     *
     * @return next identifier for idMap
     */
    public float generateId() {
        return ++this.lastId;
    }

    public void setRetriever(DBRetriever retriever) {
        this.retriever = retriever;
    }

    public void setSaver(DBSaver saver) {
        this.saver = saver;
    }

}
