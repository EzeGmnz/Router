package com.ezequiel.router;

import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.ezequiel.router.classes.TSPJson;
import com.ezequiel.router.interfaces.Route;
import com.ezequiel.router.interfaces.TSPSolver;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        List<String> addresses = new ArrayList<>();

        addresses.add("Paraguay 555, Bahia Blanca, Argentina");
        addresses.add("Zapiola 100, Bahia Blanca, Argentina");
        addresses.add("Alem 1000, Bahia Blanca, Argentina");
        addresses.add("Horneros 20, Bahia Blanca, Argentina");

        TSPSolver solver = new TSPJson(this);
        solver.solveTSP(addresses, new TSPSolver.RouteBuilderListener() {
            @Override
            public void onRouteBuilt(Route r) {
                Log.e("ASDASDASD", r.toString());
            }
        });

    }
}
