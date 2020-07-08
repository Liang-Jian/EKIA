package com.example.robot.tls;

import android.os.Process;

public class PhotoDecodeRunnable implements Runnable {
    @Override
    public void run() {
        android.os.Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);
    }
}
