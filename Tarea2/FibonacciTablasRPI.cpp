#include <iostream>
#include <fstream> 
#include <thread>
#include <cstdlib> // Libreria necesaria para usar system()
#include <string>  // Libreria para manipular texto

//Se elimina librería gpiod pues la sintáxis es incorreccta debido a la versión.


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
            
            for (int k = 0; k <11; k++) {
                b = a*k;
                file << b << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));

            }
            file << "----------------------" << std::endl;
            

        }
        file << "Fin de las tablas" << std::endl;
        file.close();



    }


//Se añade función que manda comandos para ver el estado del pin al botón.
}
bool leerBotonFisico() {
    // Ejecuta el comando para leer el stado del pin 17 y lo guarda en un .txt
    system("pinctrl get 17 > estado_boton.txt");
    
    // Lee el archivo 
    std::ifstream file("estado_boton.txt");
    std::string contenido;
    
    if (file.is_open()) {
        std::getline(file, contenido);
        file.close();
        
        // terminal responde "hi" cuando hay 3.3V (boton presionado)
        if (contenido.find("hi") != std::string::npos) {
            return true;
        }
    }
    return false; // Retorna falso si lee "lo" (0V)
}

int main() {
    //Envía el comando nativo a Linux que define el pin GPIO 17 como un input.
    system("pinctrl set 17 ip");

    std::cout << "Presione el boton para comenzar..." << std::endl;

    // El programa se queda pegado aqui hasta que se presione el botón.
    while (!leerBotonFisico()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    std::cout << "Boton presionado. Iniciando..." << std::endl;

    std::cout << "Modo Secuencial" << std::endl;
    auto inicio_secuencial = std::chrono::high_resolution_clock::now();

    SecuenciaFibonacci();
    Tablas();

    auto fin_secuencial = std::chrono::high_resolution_clock::now();   
    std::chrono::duration<double> tiempo_secuencial = fin_secuencial - inicio_secuencial;
    std::cout << "Duracion de proceso secuencial: " << tiempo_secuencial.count() << " segundos" << std::endl;

    std::cout << "Modo Paralelo" << std::endl;
    auto inicio_paralelo = std::chrono::high_resolution_clock::now();

    std::thread thread1(SecuenciaFibonacci);
    std::thread thread2(Tablas);
    
    thread1.join();
    thread2.join();
    
    auto fin_paralelo = std::chrono::high_resolution_clock::now();   
    std::chrono::duration<double> tiempo_paralelo = fin_paralelo - inicio_paralelo;
    std::cout << "Duracion de proceso paralelo: " << tiempo_paralelo.count() << " segundos" << std::endl;

    // Envia el comando nativo a Linux para encender el LED.
    system("pinctrl set 27 op dh");
    std::cout << "Proceso terminado. LED encendido" << std::endl;

    // Mantiene el LED encendido X segundos
    std::this_thread::sleep_for(std::chrono::seconds(20));
    
    // Envia el comando nativo a Linux para apagar el LED.
    system("pinctrl set 27 op dl"); 
    std::cout << "LED apagado. Fin del programa." << std::endl;

    return 0;
}
