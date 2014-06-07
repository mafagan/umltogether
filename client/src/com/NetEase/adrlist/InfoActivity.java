package com.NetEase.adrlist;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceActivity.Header;
import android.provider.MediaStore;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.View.OnClickListener;
import android.view.View.OnTouchListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;

public class InfoActivity extends Activity {
	public String contactID;
	
	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.activity_info);
		
		TextView head = (TextView) findViewById(R.id.edit_infotitle);
		head.setGravity(Gravity.CENTER);
		
		Intent intent = getIntent();
		String name = intent.getStringExtra("name");
		String phone = intent.getStringExtra("phone");
		String telephone = intent.getStringExtra("telephone");
		String email = intent.getStringExtra("email");
		String img = intent.getStringExtra("img");
		this.contactID = intent.getStringExtra("id");
		
		TextView titleTextView = (TextView) findViewById(R.id.edit_infotitle);
		titleTextView.setText(name);
		
		final Button hand = (Button) findViewById(R.id.hangphoneinput);
		hand.setText(phone);
		
		final Button teleEditText = (Button) findViewById(R.id.homephoneinput);
		teleEditText.setText(telephone);
		
		teleEditText.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				new AlertDialog.Builder(InfoActivity.this).setTitle("提示")
				.setMessage("要拨打这个号码吗").setPositiveButton("确定", new DialogInterface.OnClickListener() {
					
					@Override
					public void onClick(DialogInterface arg0, int arg1) {
						// TODO Auto-generated method stub
						Intent intent = new Intent(Intent.ACTION_CALL, Uri.parse("tel:"+teleEditText.getText().toString()));
						startActivity(intent);
					}
				})
				.setNegativeButton("取消", null)
				.show();
			}
		});
		
		
		hand.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				new AlertDialog.Builder(InfoActivity.this).setTitle("提示")
				.setMessage("要拨打这个号码吗").setPositiveButton("确定", new DialogInterface.OnClickListener() {
					
					@Override
					public void onClick(DialogInterface arg0, int arg1) {
						// TODO Auto-generated method stub
						Intent intent = new Intent(Intent.ACTION_CALL, Uri.parse("tel:"+hand.getText().toString()));
						startActivity(intent);
					}
				})
				.setNegativeButton("取消", null)
				.show();
			}
		});
		EditText emailEditText = (EditText) findViewById(R.id.emailinput);
		emailEditText.setText(email);
		
		if (img != null){
			File file = new File(img);
			if (file.exists()) {
				Uri uri = Uri.fromFile(file);
				try {
					Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), uri);
					ImageButton btn_head = (ImageButton) findViewById(R.id.btn_infoPic);
					btn_head.setImageBitmap(bitmap);
				} catch (FileNotFoundException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		this.setListener();
	}
	
	void setListener() {
		ImageButton btn_infoback = (ImageButton) findViewById(R.id.btn_infoback);
		btn_infoback.setOnTouchListener(new OnTouchListener() {

			@Override
			public boolean onTouch(View arg0, MotionEvent arg1) {
				// TODO Auto-generated method stub
				if (arg1.getAction() == MotionEvent.ACTION_DOWN)
					((ImageButton) arg0).setImageDrawable(getResources()
							.getDrawable(R.drawable.back_down));
				else {
					((ImageButton) arg0).setImageDrawable(getResources()
							.getDrawable(R.drawable.back));
				}
				return false;
			}
		});
		
		btn_infoback.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub

				Intent intent = new Intent();
				intent.setClass(InfoActivity.this, MainActivity.class);
				InfoActivity.this.startActivity(intent);
				InfoActivity.this.finish();
			}
		});
		
		ImageButton btn_delButton = (ImageButton) findViewById(R.id.btn_infodel);
		
		btn_delButton.setOnTouchListener(new OnTouchListener() {
			
			@Override
			public boolean onTouch(View arg0, MotionEvent arg1) {
				// TODO Auto-generated method stub
				if(arg1.getAction() == MotionEvent.ACTION_DOWN)
				{
					((ImageButton)arg0).setImageDrawable(getResources().getDrawable(R.drawable.del_down));
				}else if (arg1.getAction() == MotionEvent.ACTION_UP) {
					((ImageButton)arg0).setImageDrawable(getResources().getDrawable(R.drawable.del));
				}
				return false;
			}
		});
		
		btn_delButton.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				AlertDialog.Builder builder = new Builder(InfoActivity.this);
				builder.setMessage("确认删除联系人吗？");
				builder.setTitle("提示");
				builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
					
					@Override
					public void onClick(DialogInterface dialog, int which) {
						// TODO Auto-generated method stub
						SQLiteDatabase db = openOrCreateDatabase("contacts.db", Context.MODE_PRIVATE, null);
						String delSql = "delete from people where id = " + InfoActivity.this.contactID;
						db.execSQL(delSql);
						Intent intent = new Intent(InfoActivity.this, MainActivity.class);
						startActivity(intent);
						InfoActivity.this.finish();
					}
				});
				
				builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
					
					@Override
					public void onClick(DialogInterface dialog, int which) {
						// TODO Auto-generated method stub
						dialog.dismiss();
					}
				});
				
				builder.create().show();
			}
		});
	}
	
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
		// TODO Auto-generated method stub
		if (keyCode == KeyEvent.KEYCODE_BACK) {
			Intent intent = new Intent(InfoActivity.this, MainActivity.class);
			startActivity(intent);
			InfoActivity.this.finish();
		}
		return true;
		
	}
	
	
}
