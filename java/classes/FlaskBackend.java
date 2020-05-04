package com.ezequiel.router.classes;

import android.content.Context;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.ezequiel.router.interfaces.Backend;

import org.json.JSONObject;

public class FlaskBackend implements Backend {

    private static Context context;
    private static FlaskBackend instance;
    private RequestQueue requestQueue;

    private FlaskBackend(Context c) {
        context = c;
    }

    private static final String url = "http://192.168.0.5:5000/routing";

    public static Backend getInstance(Context context) {
        if (instance == null) {
            instance = new FlaskBackend(context);
        }
        return instance;
    }

    @Override
    public void postJson(JSONObject json, final JsonRequestListener listener) {

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.POST, url, json, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        listener.onResponse(response);
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        listener.onFailure(error);
                    }
                });

        jsonObjectRequest.setRetryPolicy(new DefaultRetryPolicy(
                0,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        this.addToRequestQueue(jsonObjectRequest);
    }

    private <T> void addToRequestQueue(Request<T> req) {
        getRequestQueue().add(req);
    }

    private RequestQueue getRequestQueue() {
        if (requestQueue == null) {
            requestQueue = Volley.newRequestQueue(context.getApplicationContext());
        }
        return requestQueue;
    }
}
