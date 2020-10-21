#include<jni.h>
#include<string.h>

jstring Java_com_wndk_MainActivity_helloWorld(JNIEnv* env, jobject obj){

    return (*env)->NewStringUTF(env,"fuck world use ndk");
}