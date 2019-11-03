### package name && activity name
joker@centos:~$ adb shell dumpsys window |grep mCurrent
    mCurrentAppOrientation=-1
      mCurrentRotation=0
        mCurrentUserId=0
  mCurrentFocus=Window{5ccf539 u0 com.android.calculator2/com.android.calculator2.Calculator}
*com.android.calculator2 -- packageName
*com.android.calculator2.Calculator -- activityName


### cpu version unstandard
joker@centos:~/minicap$ adb shell getprop ro.product.cpu.abi | tr -d '\r'
arm64-v8a


###  sdk version
adb shell getprop ro.build.version.sdk | tr -d '\r'
24