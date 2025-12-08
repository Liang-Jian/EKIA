use anyhow_ext::{anyhow, Result};
use bytes::BytesMut;
use std::env;
use std::hash::BuildHasher;
use std::time::Duration;
use tokio::io::{self, AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader};
use tokio::select;
use tokio::signal;
use tokio_serial::{DataBits, FlowControl, Parity, SerialPortBuilderExt, StopBits};

#[tokio::main]
async fn main() -> Result<()> {
    // 简单解析命令行参数：serial_async_tool /dev/ttyUSB0 115200
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("用法: {} <serial_path> <baud_rate>", args[0]);
        eprintln!("示例: {} /dev/ttyUSB0 115200", args[0]);
        return Err(anyhow!("参数不足"));
    }

    let port_path = &args[1];
    let baud: u32 = args[2].parse()?;

    println!("打开串口: {} @ {} baud", port_path, baud);
    let Builder = tokio_serial::new(port_path, baud)
        .data_bits(DataBits::Eight)
        .parity(Parity::None)
        .stop_bits(StopBits::One)
        


    let builder = tokio_serial::new(port_path, baud)
        .data_bits(DataBits::Eight)
        .parity(Parity::None)
        .stop_bits(StopBits::One)
        .flow_control(FlowControl::None)
        .timeout(Duration::from_millis(10)); // 低超时，降低阻塞感

    let mut serial_port = builder.open_native_async()?;

    // 拆成读/写两个句柄，用于异步任务
    let (mut serial_reader, mut serial_writer) = tokio::io::split(serial_port);

    // stdin 异步读取，用来往串口发数据
    let stdin = io::stdin();
    let mut stdin_reader = BufReader::new(stdin);
    let mut stdin_buf = String::new();

    // 串口读取缓冲区
    let mut serial_buf = BytesMut::with_capacity(4096);

    println!("=== 串口工具已启动 ===");
    println!("- 从串口接收的数据会打印出来");
    println!("- 输入一行按回车，会发送这一行到串口（自动附加 \\n）");
    println!("- Ctrl + C 退出\n");

    loop {
        select! {
            // 1. 从串口读数据
            read_res = serial_reader.read_buf(&mut serial_buf) => {
                match read_res {
                    Ok(0) => {
                        eprintln!("\n串口已关闭 (EOF)。");
                        break;
                    }
                    Ok(n) => {
                        if n > 0 {
                            // 这里可以按需要改成：仅 hex 打印 / 仅 utf-8 打印
                            print_serial_data(&serial_buf.split().freeze());
                        }
                    }
                    Err(e) => {
                        eprintln!("读取串口失败: {e}");
                        break;
                    }
                }
            }

            // 2. 从 stdin 读一行，发送到串口
            line_res = stdin_reader.read_line(&mut stdin_buf) => {
                match line_res {
                    Ok(0) => {
                        eprintln!("\n标准输入 EOF（可能是管道结束），不再发送数据。");
                        // 不直接 break，让串口读循环继续跑
                    }
                    Ok(_) => {
                        // 去掉末尾换行，再追加自定义结尾
                        let mut line = stdin_buf.trim_end_matches(&['\r', '\n'][..]).to_string();
                        line.push('\n'); // 按需要改为 \r\n 等协议要求
                        if let Err(e) = serial_writer.write_all(line.as_bytes()).await {
                            eprintln!("发送到串口失败: {e}");
                            break;
                        }
                        stdin_buf.clear();
                    }
                    Err(e) => {
                        eprintln!("读取 stdin 失败: {e}");
                        break;
                    }
                }
            }

            // 3. 捕获 Ctrl + C 优雅退出
            _ = signal::ctrl_c() => {
                eprintln!("\n收到 Ctrl+C，准备退出...");
                break;
            }
        }
    }

    Ok(())
}

/// 打印串口收到的数据（同时以 HEX + UTF-8 形式）
fn print_serial_data(buf: &[u8]) {
    use std::io::Write;

    if buf.is_empty() {
        return;
    }

    // HEX 输出
    print!("RX HEX: ");
    for b in buf {
        print!("{:02X} ", b);
    }
    println!();

    // 尝试 UTF-8 输出
    match std::str::from_utf8(buf) {
        Ok(s) => {
            println!("RX STR: {}", s.trim_end_matches(&['\r', '\n'][..]));
        }
        Err(_) => {
            println!("RX STR: <非 UTF-8 数据>");
        }
    }

    // 刷新 stdout，避免缓冲
    let _ = std::io::stdout().flush();
}
