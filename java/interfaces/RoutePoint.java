package com.ezequiel.router.interfaces;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.io.Serializable;

/**
 * RoutePoint Interface
 * Representing a point in a route
 */
public class RoutePoint implements Serializable {

    private String address;

    public RoutePoint(@Nullable String address) {
        this.address = address;
    }

    public String getAddress() {
        return this.address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    @NonNull
    @Override
    public String toString() {
        return address == null ? "" : this.address;
    }
}
