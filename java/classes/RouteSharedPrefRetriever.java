package com.ezequiel.router.classes;

import android.content.Context;
import android.content.SharedPreferences;

import com.ezequiel.router.VALUES;
import com.ezequiel.router.interfaces.DBRetriever;
import com.ezequiel.router.interfaces.Route;

import java.util.ArrayList;
import java.util.List;

/**
 * DBRetriever implementation using sharedPreferences as persistent storage
 */
public class RouteSharedPrefRetriever implements DBRetriever {

    private SharedPreferences sharedPreferences;
    private RouteJsonManager routeJsonManager;

    public RouteSharedPrefRetriever(Context context) {
        this.routeJsonManager = new RouteJsonManager();
        this.sharedPreferences = context.getSharedPreferences(VALUES.SHARED_PREFERENCES_NAME, Context.MODE_PRIVATE);
    }

    @Override
    public List<Route> get() {
        int number = sharedPreferences.getInt(VALUES.SAVED_ROUTES_COUNT, 0);
        List<Route> output = new ArrayList<>();

        for (int i = 0; i < number; i++) {
            String json = sharedPreferences.getString(VALUES.SAVE_ROUTE_NAME + i, null);
            output.add(routeJsonManager.fromJson(json));
        }
        return output;
    }
}
