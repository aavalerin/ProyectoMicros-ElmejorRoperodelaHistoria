#include <iostream>
#include <fstream> 
#include <thread>
//#include <mutex>
#include <chrono>
//#include <gpiod.hpp> 

//std::mutex mtx; //mutex en caso de usar el mismo archivo para ambos

void SecuenciaFibonacci() {
    std::ofstream file("Fibonacci.txt");
    if (file.is_open()) {
        file << "Números en la Secuencia después del 0, 1" << std::endl;
        int a=0, b=1, c;
        for (int i = 1; i <31; i++) {
            c = a + b;
            a = b; 
            b = c;
            file << i << "." << b << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        }
        file << "Fin" << std::endl;
        file.close();
    }


}

void Tablas(){
    std::ofstream file("Tablas.txt");
    if (file.is_open()) {
        int a, b;
        for (int i = 1; i <11; i++ ) {
            a=i;
            file << "Tabla del " << a << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            for (int k = 0; k <11; k++) {
                b = a*k;
                file << b << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));

            }
            file << "----------------------" << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

        }
        file << "Fin de las tablas" << std::endl;
        file.close();



    }



}

int main() {

    // gpiod::chip ("gpiochip4");
    // gpiod::line linea= chip.get.line (17);
    // linea.boton.request({"FibonacciTablasRPI", gpiod::line_request:DIRECTION_INPUT, 0});

    std::cout <<"Presion el botón para comenzar" << std::endl;

    // while (linea_boton.get_value() == 0) {
    //     std::this_thread::sleep_for(std::chrono::milliseconds(50));
    // }

    std::cout << "Boton presionado. Iniciando procesos..." << std::endl;

    std::cout << "Modo Secuencial" << std::endl;
    auto inicio_secuencial =  std::chrono::high_resolution_clock::now();

    SecuenciaFibonacci();
    Tablas();

    auto fin_secuencial = std::chrono::high_resolution_clock::now();   

    std::chrono::duration<double> tiempo_secuencial = fin_secuencial - inicio_secuencial;

    std::cout << "Duracion de proceso secuencial:" << tiempo_secuencial.count() << std::endl;

    std::cout << "Modo Paralelo" << std::endl;

    auto inicio_paralelo =  std::chrono::high_resolution_clock::now();

    std::thread thread1 (SecuenciaFibonacci);
    std::thread thread2 (Tablas);
    
    thread1.join();
    thread2.join();
    
    auto fin_paralelo = std::chrono::high_resolution_clock::now();   

    std::chrono::duration<double> tiempo_paralelo = fin_paralelo - inicio_paralelo;

    std::cout << "Duracion de proceso paralelo:" << tiempo_paralelo.count() << std::endl;

    //Configura el pin del LED como salida

    // gpiod::line linea_led = chip.get_line(27); // GPIO 27
    // linea_led.request({"mi_programa", gpiod::line_request::DIRECTION_OUTPUT, 0});

    // Envia la senal para encender el LED 

    // linea_led.set_value(1);
    std::cout << "Proceso terminado. LED encendido en GPIO 27." << std::endl;

    // Opcional: Mantener el LED encendido  antes de que  programa termine y lo apagué

    std::this_thread::sleep_for(std::chrono::seconds(5));
    // linea_led.set_value(0); // Apagar

    return 0;


}