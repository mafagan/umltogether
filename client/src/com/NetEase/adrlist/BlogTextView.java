package com.NetEase.adrlist;

import java.util.Map;
import java.util.Set;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.text.Html;
import android.text.Html.ImageGetter;








   
import android.text.util.Linkify;
import android.util.AttributeSet;
import android.widget.TextView;

public class BlogTextView extends TextView {
	private static final int NAMELENGTH=10; //昵称长度小于10
	private Map<String,String> faceMap;
	private CharSequence text;
	
	private ImageGetter imageGetter = new Html.ImageGetter() {
        @Override
        public Drawable getDrawable(String source) {
              Drawable drawable = null;
              String sourceName=getContext().getPackageName()+":drawable/"+source;
              int id=getResources().getIdentifier(sourceName,null,null);
              if (id!=0){
	              drawable=getResources().getDrawable(id);
	              if (drawable!=null){
	            	  drawable.setBounds(0, 0, 
	            			  drawable.getIntrinsicWidth(), 
	            			  drawable.getIntrinsicHeight());
	              }
              }
              return drawable;
        }
	};

	public BlogTextView(Context context) {
		super(context);
		setAutoLinkMask(Linkify.ALL);
	}

	public BlogTextView(Context context, AttributeSet attrs) {
		super(context, attrs);
		setAutoLinkMask(Linkify.ALL);
	}

	public BlogTextView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
		setAutoLinkMask(Linkify.ALL);
	}
	
	public void setText(CharSequence text,Map<String,String> faceMap){
		this.faceMap=faceMap;
		setText(text);
	}

	@Override
	public CharSequence getText() {
		return text==null?"":text;
	}

	@Override
	public void setText(CharSequence text, BufferType type) {
		this.text=text;
		
		String cs=text.toString();
		String font1="<font color=#339966>";
		String font2="</font>";
		
		int start=0;
		while(true){
			start=cs.indexOf('@',start);
			if (start<cs.length() && start>=0){
				int end=cs.indexOf(' ',start);
				if (end<cs.length() && end>0 && end-start<=NAMELENGTH){
					CharSequence subcs=new String(cs.subSequence(start, end).toString());
					cs=cs.replace(subcs,font1+subcs+font2 );
					start+=font1.length()+subcs.length()+font2.length();
				}
				else{
					end=cs.indexOf(':',start);
					if (end<cs.length() && end>0 && end-start<=NAMELENGTH){
						CharSequence subcs=new String(cs.subSequence(start, end).toString());
						cs=cs.replace(subcs,font1+subcs+font2 );
						start+=font1.length()+subcs.length()+font2.length();
					}
				}
				start+=1;
			}
			else{
				break;
			}
		}
		
		if (faceMap!=null){
			
			Set<String> keys=faceMap.keySet();
			for(String key:keys){
				if (cs.contains(key)){
					cs=cs.replace(key, "<img src='"+faceMap.get(key)+"'>");
				}
			}
		}
	
		super.setText(Html.fromHtml(cs,imageGetter,null), type);
	}
}
