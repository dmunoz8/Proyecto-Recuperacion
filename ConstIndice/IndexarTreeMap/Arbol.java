/**
 * Controlador que maneja las instrucciones a ejecutar del programa
 * Implementación del inidice con TreeMap para mantener los elementos ordenados
 * 
 * @Daniel Muñoz, b24645 
 * @version 1, 6/5/16
 */

import java.lang.*;
import java.util.*;

public class Arbol {
    private TreeMap<String,Map> diccionario;  //contiene el termino como llave y un conjunto de pares de valores {documento, frecuencia] de ese termino
    private TreeMap<String,Integer> listaPosting;

    public Arbol() 
    {
        diccionario = new TreeMap<String,Map>();
    }

    public Map getRaiz() 
    {
        return diccionario;
    }

    
    /**
     * @brief: Verifica si hay elementos en el diccionario
     * @params: N/A
     * @return: estado del diccionario
     */
    public boolean estarVacia() 
    {
        boolean resultado = diccionario.isEmpty();
        return resultado;
    }

    /**
     * @brief: Agrega un termino nuevo al diccionario
     * @params: termino a agregar y el documento donde se encuentra.
     * @return: N/A
     */
    public void agregar(String termino, String doc) 
    {
        listaPosting = new TreeMap<String,Integer>();
        listaPosting.put(doc,1);
        diccionario.put(termino,listaPosting);
    }

    
    /**
     * @brief: Devuelve la cantidad de elementos en el diccionario
     * @params: N/A
     * @return: cantidad de elementos en el diccionario
     */
    public int contar() 
    {
        if(this.estarVacia()) 
        {
            return 0; 
        } 
        else 
        {
            return diccionario.size();
        }
    }

    
    /**
     * @brief: Revisa si ya existe el termino en el diccionario.
     * @params: termino a buscar
     * @return: verdadero si esta en el diccionario, falso si no
     */
    public boolean buscar(String palabra) 
    {
        boolean buscado = false;
        if(diccionario.get(palabra) != null)
        {
            buscado = true;
        }
        return buscado;
    }

    
    /**
     * @brief: Agrega una nueva aparicion del termino en el documento, en el diccionario, si el documento no existe lo agrega.
     * @params: termino a agregar y el documento donde se encuentra.
     * @return: N/A
     */
    public void sumar(String termino,String doc)
    {
        Map lista = diccionario.get(termino);
        if(lista.containsKey(doc) == true)
        {
            //             if(doc.equals("texto1.txt"){
            //                 System.out.println(doc);
            //             }
            int tf = (Integer) lista.get(doc);
            tf++;
            lista.put(doc,tf);
        }
        else{
            lista.put(doc,1);
        }
    }

}
