package com.ezequiel.router.interfaces;

import org.json.JSONObject;

/**
 * Backend abstraction including basic operations
 */
public interface Backend {

    /**
     * Posts json into backend, and gets the response, if any onto the jsonRequestListener
     *
     * @param json     json to post
     * @param listener success jsonRequestListener for the backend response
     */
    void postJson(JSONObject json, final JsonRequestListener listener);

    /**
     * Listener for Json Requests
     */
    interface JsonRequestListener {

        void onResponse(JSONObject json);

        void onFailure(Exception e);
    }

}
