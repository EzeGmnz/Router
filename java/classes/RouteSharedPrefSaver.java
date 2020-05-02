package com.ezequiel.router.classes;

import android.content.Context;
import android.content.SharedPreferences;

import com.ezequiel.router.VALUES;
import com.ezequiel.router.interfaces.DBSaver;
import com.ezequiel.router.interfaces.JsonManager;
import com.ezequiel.router.interfaces.Route;

import java.util.List;

/**
 * DBSaver implementation using SharedPreferences
 */
public class RouteSharedPrefSaver implements DBSaver {

    private SharedPreferences sharedPreferences;
    private JsonManager routeJsonManager;

    public RouteSharedPrefSaver(Context context) {
        this.routeJsonManager = new RouteJsonManager();
        this.sharedPreferences = context.getSharedPreferences(VALUES.SHARED_PREFERENCES_NAME, Context.MODE_PRIVATE);
    }

    @Override
    public void save(List<Route> list) {
        SharedPreferences.Editor editor = sharedPreferences.edit();

        editor.putInt(VALUES.SAVED_ROUTES_COUNT, list.size());
        for (int i = 0; i < list.size(); i++) {
            editor.putString(VALUES.SAVE_ROUTE_NAME + i, routeJsonManager.toJson(list.get(i))).apply();
        }
        editor.apply();
    }

}
