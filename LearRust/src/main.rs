use std::io;


fn main() {


//    17600810923
    let mut foo =1;
    let bar = foo; //
    println!("guess count");
    println!("这第一名到底有多强，");
    let mut guess = String::new();
    io::stdin().read_line(&mut guess).expect("no found");
    println!("you guest: {}",guess);
}
