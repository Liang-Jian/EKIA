package com.example.lexue;

import android.os.Process;

public class PhotoDecodeRunnable implements Runnable {
    @Override
    public void run() {
        Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);
    }
}
