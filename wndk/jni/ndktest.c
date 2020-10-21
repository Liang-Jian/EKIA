#include<jni.h>
#include<string.h>


// Java_ packageName _ activity _ String name

jstring Java_com_example_wndk_MainActivity_helloWorld(JNIEnv* env,jobject obj){

     return (*env)->NewStringUTF(env,"fuck world use ndk");
}