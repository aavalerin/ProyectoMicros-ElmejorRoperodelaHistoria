#include <iostream>
#include <fstream> 
#include <thread>
//#include <mutex>
#include <chrono>

//std::mutex mtx; // Mutex para proteger el acceso a la tabla de Fibonacci

void SecuenciaFibonacci() {
    std::ofstream file("Fibonacci.txt");
    if (file.is_open()) {
        file << "Números en la Secuencia después del 0, 1" << std::endl;
        int a=0, b=1, c; //Se establecen los números iniciales para comenzar la secuencia. 
        for (int i = 1; i <31; i++) { 
            c = a + b; //El resultado es la suma de los dos números "anteriores"
            a = b; 
            b = c;//El resultado para a la fila de los números "anteriores" para hacer la siguiente suma y continuar la secuencia.
            file << i << "." << b << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));//Tiempo de espera entre cálculos
        
        }
        file << "Fin" << std::endl;
        file.close();
    }


}

void Tablas(){
    std::ofstream file("Tablas.txt");
    if (file.is_open()) {
        int a, b;
        for (int i = 1; i <11; i++ ) {//Ciclo para determinar a qué número se le genera la tabla
            a=i;
            file << "Tabla del " << a << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            for (int k = 0; k <11; k++) {//Se multiplica el número por otro que irá aumentando del 0 al 10. 
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

    std::cout <<"Presione para Iniciar" << std::endl;
    std::cin.get();


    //Se comienza a contar la duración al ejecutar las funciones de forma secuencial
    std::cout << "Modo Secuencial" << std::endl;
    auto inicio_secuencial =  std::chrono::high_resolution_clock::now();

    SecuenciaFibonacci();
    Tablas();

    auto fin_secuencial = std::chrono::high_resolution_clock::now();//Se detiene el contador 

    std::chrono::duration<double> tiempo_secuencial = fin_secuencial - inicio_secuencial;//Se calcula el tiempo total

    std::cout << "Duracion de proceso secuencial:" << tiempo_secuencial.count() << std::endl;


//Se comienza a contar la duración al ejecutar las funciones de forma paralela
    std::cout << "Modo Paralelo" << std::endl;

    auto inicio_paralelo =  std::chrono::high_resolution_clock::now();

    //Se le asigna una función a cada hilo

    std::thread thread1 (SecuenciaFibonacci);
    std::thread thread2 (Tablas);
    
    //Se comienza la ejecución en paralelo
    thread1.join();
    thread2.join();
    
    auto fin_paralelo = std::chrono::high_resolution_clock::now();   

    std::chrono::duration<double> tiempo_paralelo = fin_paralelo - inicio_paralelo;//Se calcula el tiempo total

    std::cout << "Duracion de proceso paralelo:" << tiempo_paralelo.count() << std::endl;

    std::cout << "\n LED ENCENDIDO" << std::endl;
    return 0;


}
