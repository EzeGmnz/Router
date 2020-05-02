package com.ezequiel.router.interfaces;

import java.io.Serializable;

/**
 * Serialized and deserialized objects using json
 */
public interface JsonManager<E extends Serializable> {

    /**
     * Get json from given object
     *
     * @param object object to get its json from
     * @return json of object
     */
    String toJson(E object);

    /**
     * Get object from json
     *
     * @param json json used to retrieve the object from
     * @return deserialized object from json
     */
    E fromJson(String json);

}
