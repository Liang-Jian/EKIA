### 查看包名和activity名字
 robot@rob0t:~$ adb shell dumpsys window |grep mCurrent
    mCurrentAppOrientation=-1
      mCurrentRotation=0
        mCurrentUserId=0
  mCurrentFocus=Window{5ccf539 u0 com.android.calculator2/com.android.calculator2.Calculator}
*com.android.calculator2 -- packageName
*com.android.calculator2.Calculator -- activityName
