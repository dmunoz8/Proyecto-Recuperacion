/**
 * Controlador que maneja las instrucciones a ejecutar del programa
 * 
 * @Daniel Muñoz, b24645 
 * @version 1, 6/5/16
 */

import java.lang.*;
import java.util.*;

public class Arbol {
    private HashMap<String,Map> diccionario;
    private HashMap<String,Integer> listaPosting;

    public Arbol() 
    {
        diccionario = new HashMap<String,Map>();
    }

    public Map getRaiz() 
    {
        return diccionario;
    }

    public boolean estarVacia() 
    {
        boolean resultado = diccionario.isEmpty();
        return resultado;
    }

    public void agregar(String termino, String doc) 
    {
        listaPosting = new HashMap<String,Integer>();
        listaPosting.put(doc,1);
        diccionario.put(termino,listaPosting);
    }

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

    public boolean buscar(String palabra) 
    {
        boolean buscado = false;
        if(diccionario.get(palabra) != null)
        {
            buscado = true;
        }
        return buscado;
    }

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
