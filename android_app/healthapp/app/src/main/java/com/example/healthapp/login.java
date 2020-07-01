package com.example.healthapp;

//import androidx.appcompat.app.AppCompatActivity;
//
//import android.os.Bundle;
//
//public class login extends AppCompatActivity {
//
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_login);
//    }
//}



import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.content.Intent;
import android.content.pm.PackageManager;
import androidx.annotation.Nullable;
//import android.support.design.widget.Snackbar;
import androidx.appcompat.app.AppCompatActivity;
import android.app.LoaderManager.LoaderCallbacks;

import android.content.CursorLoader;
import android.content.Loader;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;

import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.text.TextUtils;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.github.florent37.materialtextfield.MaterialTextField;
import com.nihaskalam.progressbuttonlibrary.CircularProgressButton;

import com.example.healthapp.utils.HappUtil;
import com.example.healthapp.utils.PrefConstants;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static android.Manifest.permission.READ_CONTACTS;

/**
 * A login screen that offers login via username/password.
 */
public class login extends AppCompatActivity  {
    MaterialTextField username,password;
    CircularProgressButton loginbut;
    RequestQueue queue ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        if(PrefConstants.getAppPrefString(getApplicationContext(),"user_id")!=null){
            startActivity(new Intent(getApplicationContext(),MainActivity.class));
            finish();
        }
        queue =  Volley.newRequestQueue(getApplicationContext());

        TextView registerText = (TextView)findViewById(R.id.register);
        username = (MaterialTextField)findViewById(R.id.usernamefield);
        password = (MaterialTextField)findViewById(R.id.passwordfield);

        loginbut = (CircularProgressButton)findViewById(R.id.loginBut);

        loginbut.setProgress(0);



        loginbut.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                if(HappUtil.is_empty(username) || HappUtil.is_empty(password)){
                    Toast.makeText(getApplicationContext(),"Username or password is empty",Toast.LENGTH_SHORT).show();
                }
                else {
                    loginbut.setIndeterminateProgressMode(true);

                    loginbut.showProgress();
                    login_check();

                }


            }
        });

        registerText.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(getApplicationContext(),Register.class));
            }
        });
    }

    public void login_check(){
        String url = HappUtil.baseurl+"";
        Log.d("Url",url);
        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        try {

                            Log.d("Response", response);

                            loginbut.setProgress(0);
                            JSONObject login_detail = new JSONObject(response);

                            Log.d("Responsed", login_detail.getString("status"));


                            if(login_detail.opt("status").toString().equals("ok")){
                                PrefConstants.putAppPrefString(getApplicationContext(),"user_id",login_detail.getString("user_id"));
                                startActivity(new Intent(getApplicationContext(),MainActivity.class));
                                finish();
                            }
                            else if(login_detail.opt("status").toString().equals("error")){
                                Toast.makeText(getApplicationContext(),login_detail.getString("result"),Toast.LENGTH_SHORT).show();
                                loginbut.showIdle();
                                loginbut.showIdle();

                            }


                        }
                        catch (JSONException v){
                            v.printStackTrace();
                        }
                    }
                },

                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Log.d("Error.Response", error.toString());
                        Toast.makeText(getApplicationContext(),"Error",Toast.LENGTH_SHORT).show();
                        loginbut.setProgress(0);

                    }

                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String>  params = new HashMap<String, String>();


                params.put("username", username.getEditText().getText().toString());
                params.put("password", password.getEditText().getText().toString());
                Log.d("Post", String.valueOf(params));
                return params;
            }
        };
        queue.add(postRequest);



    }

}

