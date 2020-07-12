//
// Created by robot on 7/12/20.
//

#include <jni.h>
#include <string.h>

jstring Java_com_example_robot_ndktest_MainActivity_helloWorld(JNIEnv* env,jobject obj){
    return (*env)->NewStringUTF(env,"fuck world");
}