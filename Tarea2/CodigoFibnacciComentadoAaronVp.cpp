// ===== LIBRERÍAS =====
#include <iostream>   // Entrada/salida por consola (std::cout)
#include <fstream>    // Manejo de archivos (std::ofstream, std::ifstream)
#include <thread>     // Manejo de hilos (std::thread)
#include <chrono>     // Manejo de tiempo y pausas
#include <cstdlib>    // Ejecutar comandos del sistema (system())
#include <string>     // Manejo de strings (std::string)


// ===== FUNCIÓN FIBONACCI =====
void SecuenciaFibonacci() {
    std::ofstream file("Fibonacci.txt"); // <fstream>

    if (file.is_open()) { // <fstream>
        file << "Números en la Secuencia después del 0, 1" << std::endl; // <fstream>

        int a=0, b=1, c;

        for (int i = 1; i <31; i++) {
            c = a + b;

            a = b;
            b = c;

            file << i << "." << b << std::endl; // <fstream>

            std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
            // <thread> + <chrono>
        }

        file << "Fin" << std::endl; // <fstream>
        file.close(); // <fstream>
    }
}


// ===== FUNCIÓN TABLAS =====
void Tablas(){
    std::ofstream file("Tablas.txt"); // <fstream>

    if (file.is_open()) { // <fstream>
        int a, b;

        for (int i = 1; i <11; i++ ) {
            a=i;

            file << "Tabla del " << a << std::endl; // <fstream>

            std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
            // <thread> + <chrono>

            for (int k = 0; k <11; k++) {
                b = a*k;

                file << b << std::endl; // <fstream>

                std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
                // <thread> + <chrono>
            }

            file << "----------------------" << std::endl; // <fstream>

            std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
            // <thread> + <chrono>
        }

        file << "Fin de las tablas" << std::endl; // <fstream>
        file.close(); // <fstream>
    }
}


// ===== FUNCIÓN PARA LEER BOTÓN =====
bool leerBotonFisico() {
    system("pinctrl get 17 > estado_boton.txt"); // <cstdlib>

    std::ifstream file("estado_boton.txt"); // <fstream>
    std::string contenido; // <string>

    if (file.is_open()) { // <fstream>
        std::getline(file, contenido); // <fstream> + <string>
        file.close(); // <fstream>

        if (contenido.find("hi") != std::string::npos) { // <string>
            return true;
        }
    }
    return false;
}


// ===== FUNCIÓN PRINCIPAL =====
int main() {

    system("pinctrl set 17 ip"); // <cstdlib>

    std::cout << "Presione el boton para comenzar..." << std::endl; // <iostream>

    while (!leerBotonFisico()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(50)); 
        // <thread> + <chrono>
    }

    std::cout << "Boton presionado. Iniciando..." << std::endl; // <iostream>

    // ===== MODO SECUENCIAL =====
    std::cout << "Modo Secuencial" << std::endl; // <iostream>

    auto inicio_secuencial = std::chrono::high_resolution_clock::now(); // <chrono>

    SecuenciaFibonacci();
    Tablas();

    auto fin_secuencial = std::chrono::high_resolution_clock::now(); // <chrono>

    std::chrono::duration<double> tiempo_secuencial = fin_secuencial - inicio_secuencial; 
    // <chrono>

    std::cout << "Duracion de proceso secuencial: " 
              << tiempo_secuencial.count() << " segundos" << std::endl; // <iostream>


    // ===== MODO PARALELO =====
    std::cout << "Modo Paralelo" << std::endl; // <iostream>

    auto inicio_paralelo = std::chrono::high_resolution_clock::now(); // <chrono>

    std::thread thread1(SecuenciaFibonacci); // <thread>
    std::thread thread2(Tablas); // <thread>

    thread1.join(); // <thread>
    thread2.join(); // <thread>

    auto fin_paralelo = std::chrono::high_resolution_clock::now(); // <chrono>

    std::chrono::duration<double> tiempo_paralelo = fin_paralelo - inicio_paralelo; 
    // <chrono>

    std::cout << "Duracion de proceso paralelo: " 
              << tiempo_paralelo.count() << " segundos" << std::endl; // <iostream>


    // ===== CONTROL LED =====
    system("pinctrl set 27 op dh"); // <cstdlib>
    std::cout << "Proceso terminado. LED encendido" << std::endl; // <iostream>

    std::this_thread::sleep_for(std::chrono::seconds(20)); // <thread> + <chrono>

    system("pinctrl set 27 op dl"); // <cstdlib>
    std::cout << "LED apagado. Fin del programa." << std::endl; // <iostream>

    return 0;
}