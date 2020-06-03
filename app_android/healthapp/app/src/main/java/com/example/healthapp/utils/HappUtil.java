package com.example.healthapp.utils;

import android.content.Context;
import android.content.pm.PackageManager;

import com.github.florent37.materialtextfield.MaterialTextField;



public class HappUtil {
    public static int getAppVersionCode(Context context) {
        int version = -1;
        try {
            version = context.getPackageManager().getPackageInfo(context.getPackageName(), 0).versionCode;
        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();

        }

        return version;
    }
    public static String baseurl = "http://18.220.255.44:8000/p/api/v1";

    public static boolean is_empty(MaterialTextField materialTextField){
        if(materialTextField.getEditText().length() < 1){
            return true;
        }
        return false;
    }
}
