/**
 * Controlador que maneja las instrucciones a ejecutar del programa
 * 
 * @Daniel Muñoz, b24645, jeffrey venegas
 * @version 1, 6/5/16
 */

import java.lang.Object;
import java.io.Writer;
import java.io.PrintWriter;
import javax.swing.*;
import java.util.*;
import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.io.*;

import java.io.IOException;

public class Controlador
{
    /**
     * Constructor for objects of class Controlador
     */
    public Controlador()
    {}

    /**
     * Se conecta a las paginas que lee del archivo Urls.txt y trae el body, el cual usa para crear un archivo de texto basado en el contenido de la pagina
     * 
     * @param: String args[]
     * @return: N/A
     */   
    public static void main(String args[]) throws IOException
    {
        BufferedReader input =  new BufferedReader(new FileReader("Urls.txt")); //lector de urls
        int nombre = 0;
        String line = null;
		//Medicion de tiempo
        // double inicio = System.currentTimeMillis();
        while (( line = input.readLine()) != null) //lee mientras haya contenido, si es nulo llego al final del archivo
        {
            try{
                Document doc = Jsoup.connect(line)
                        //Se elige el agente a utilizar para hacer la recolección de datos
						//.userAgent("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
                    .get(); //conecta con la pagina
                //String title = doc.title(); //trae el titulo
                String body = doc.body().text(); //trae el body en formato de texto sin tags htmls
                StringBuilder sb = new StringBuilder(body);

                int i = 0;
                while ((i = sb.indexOf(" ", i + 1)) != -1) 
                {
                    sb.replace(i, i + 1, "\n"); //escribe una palabra por renglon
                }
                PrintWriter writer = new PrintWriter("Texto" + nombre + ".txt", "UTF-8"); //crea el archivo segun cada url
                writer.println(sb.toString());
                writer.close();
                nombre++;
            }
            catch(Exception e){
                e.printStackTrace();
            }   
        }
		/*Para medicion de tiempo del programa
		
                    double fin = System.currentTimeMillis();
                    double tiempo = fin - inicio;
                    FileWriter arch = null;
                    PrintWriter writer = null;
                    try{
                        arch = new FileWriter("TiemposChrome.txt",true);
                        writer = new PrintWriter(arch);
                        writer.println(tiempo);
                    }catch(Exception e){
                        e.printStackTrace();
                    }
                    finally {
                        try {
                            if (null != arch){
                                arch.close();
                            }
                        } catch (Exception e2) {
                            e2.printStackTrace();
                        }
                    }
					*/
    }
}
