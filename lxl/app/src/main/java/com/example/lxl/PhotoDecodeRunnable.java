package com.example.lxl;

import android.os.Process;

public class PhotoDecodeRunnable implements Runnable {
    @Override
    public void run() {
        Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);
    }
}
