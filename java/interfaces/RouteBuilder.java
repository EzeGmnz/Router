package com.ezequiel.router.interfaces;

import com.ezequiel.router.exceptions.NotFoundException;

public interface RouteBuilder {

    Route getRoute();

    void addRoutePart(RoutePoint p);

    void removeRoutePart(RoutePoint p) throws NotFoundException;


}
